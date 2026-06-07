import os
import csv
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
OUTPUT_FILE = 'gocchin_mail_list.csv'
SEARCH_QUERY = 'from:info@gocchin056.com'


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
        date_str = headers.get('Date', '')

        try:
            dt = parsedate_to_datetime(date_str)
            date_full = dt.strftime('%Y-%m-%d')
        except Exception:
            date_full = ''

        body = get_plain_text(detail['payload'])
        # 本文が長すぎる場合は先頭2000文字に絞る（分析用途）
        body_trimmed = body[:2000].strip()

        rows.append({
            '日付': date_full,
            '件名': subject,
            '本文': body_trimmed,
        })

    rows.sort(key=lambda x: x['日付'])

    output_path = os.path.join(parent_dir, OUTPUT_FILE)
    fieldnames = ['日付', '件名', '本文']
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'\n完了！{len(rows)}件を {output_path} に保存しました。')


if __name__ == '__main__':
    main()
