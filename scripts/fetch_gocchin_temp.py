import os
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

SEARCH_QUERY = 'from:info@gocchin056.com after:2026/06/08 before:2026/06/15'


def get_credentials_file():
    for name in ['credentials.json', 'client_secret_*.json']:
        matches = glob.glob(os.path.join(SECRETS_DIR, name))
        if matches:
            return matches[0]
    raise FileNotFoundError(f'認証ファイルが見つかりません。{SECRETS_DIR} を確認してください。')


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


def main():
    print('Gmail APIに接続中...')
    service = get_gmail_service()

    print(f'検索: {SEARCH_QUERY}')
    result = service.users().messages().list(
        userId='me', q=SEARCH_QUERY, maxResults=20
    ).execute()
    messages = result.get('messages', [])
    print(f'{len(messages)}件のメールが見つかりました\n')

    emails = []
    for msg in messages:
        detail = service.users().messages().get(
            userId='me', id=msg['id'], format='full'
        ).execute()
        headers = {h['name']: h['value'] for h in detail['payload']['headers']}
        subject = headers.get('Subject', '（件名なし）')
        date_str = headers.get('Date', '')
        body = get_plain_text(detail['payload'])

        try:
            dt = parsedate_to_datetime(date_str)
            date_fmt = dt.strftime('%m/%d %H:%M')
            sort_key = dt.strftime('%Y%m%d%H%M')
        except Exception:
            date_fmt = date_str
            sort_key = date_str

        emails.append((sort_key, date_fmt, subject, body))

    emails.sort(key=lambda x: x[0])

    for sort_key, date_fmt, subject, body in emails:
        print(f'\n{"=" * 70}')
        print(f'日付: {date_fmt}')
        print(f'件名: {subject}')
        print(f'{"=" * 70}')
        print(body)


if __name__ == '__main__':
    main()
