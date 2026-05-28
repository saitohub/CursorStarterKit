import os
import csv
import re
import base64
import glob
from email.utils import parsedate_to_datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SECRETS_DIR = os.path.expanduser('~/secrets/gmail_api')
TOKEN_FILE = os.path.join(SECRETS_DIR, 'token.json')
OUTPUT_FILE = 'ichimaiworks_list.csv'
SEARCH_QUERY = 'subject:イチゼミ OR subject:アカデミア OR subject:イチトレ OR subject:イチヘリ after:2019/01/01'

THEME_PREFIXES = ['イチゼミ', 'アカデミア', 'イチトレ', 'イチヘリ']


def get_credentials_file():
    for name in ['credentials.json', 'client_secret_*.json']:
        matches = glob.glob(os.path.join(SECRETS_DIR, name))
        if matches:
            return matches[0]
    raise FileNotFoundError(f'認証ファイルが見つかりません。client_secret_*.json を {SECRETS_DIR} に置いてください。')


def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_file = get_credentials_file()
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


def decode_body(data):
    return base64.urlsafe_b64decode(data + '==').decode('utf-8', errors='ignore')


def get_plain_text(payload):
    if payload.get('mimeType') == 'text/plain':
        data = payload.get('body', {}).get('data', '')
        return decode_body(data) if data else ''
    for part in payload.get('parts', []):
        text = get_plain_text(part)
        if text:
            return text
    return ''


def extract_urls(text):
    pattern = r'https?://[^\s　<>\"\'「」（）【】]+'
    return list(dict.fromkeys(re.findall(pattern, text)))


def extract_password(text):
    patterns = [
        r'(?:パスワード|ぱすわーど|PW|pw|password|Password|PASS|pass)[：:\s　]+([a-zA-Z0-9!@#$%^&*_\-]+)',
        r'(?:視聴|閲覧)[^\n]{0,10}(?:パスワード|PW)[：:\s　]+([a-zA-Z0-9!@#$%^&*_\-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return ''


def extract_theme(subject):
    for prefix in THEME_PREFIXES:
        if subject.startswith(prefix):
            return prefix
    return ''


def fetch_all_messages(service, query):
    messages = []
    page_token = None
    while True:
        result = service.users().messages().list(
            userId='me', q=query, pageToken=page_token, maxResults=500
        ).execute()
        messages.extend(result.get('messages', []))
        page_token = result.get('nextPageToken')
        if not page_token:
            break
    return messages


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    os.chdir(parent_dir)

    print('Gmail APIに接続中...')
    service = get_gmail_service()

    print(f'メールを検索中: {SEARCH_QUERY}')
    messages = fetch_all_messages(service, SEARCH_QUERY)
    print(f'{len(messages)}件のメールが見つかりました\n')

    rows = []
    for i, msg in enumerate(messages):
        print(f'処理中... {i + 1}/{len(messages)}', end='\r', flush=True)
        detail = service.users().messages().get(
            userId='me', id=msg['id'], format='full'
        ).execute()

        headers = {h['name']: h['value'] for h in detail['payload']['headers']}
        subject = headers.get('Subject', '（件名なし）')
        sender = headers.get('From', '')
        date_str = headers.get('Date', '')

        try:
            dt = parsedate_to_datetime(date_str)
            year = dt.strftime('%Y')
            year_month = dt.strftime('%Y-%m')
            date_short = dt.strftime('%m/%d')
        except Exception:
            year = ''
            year_month = ''
            date_short = ''

        body = get_plain_text(detail['payload'])
        urls = extract_urls(body)
        password = extract_password(body)
        theme = extract_theme(subject)

        rows.append({
            '配信年': year,
            '配信年月': year_month,
            '日付': date_short,
            '差出人': sender,
            'テーマ': theme,
            '件名': subject,
            'URL': urls[0] if urls else '',
            'その他URL': '\n'.join(urls[1:]) if len(urls) > 1 else '',
            'パスワード': password,
        })

    rows.sort(key=lambda x: (x['配信年'], x['配信年月'], x['日付']))

    output_path = os.path.join(parent_dir, OUTPUT_FILE)
    fieldnames = ['配信年', '配信年月', '日付', '差出人', 'テーマ', '件名', 'URL', 'その他URL', 'パスワード']
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'\n完了！{len(rows)}件を {output_path} に保存しました。')


if __name__ == '__main__':
    main()
