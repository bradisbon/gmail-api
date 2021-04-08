import base64, os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from httplib2shim import Http
from oauth2client import file
from email.mime.text import MIMEText

creds = Credentials.from_authorized_user_file(os.path.expanduser('~/.credentials/gmail_api_token.json'))
service = build('gmail', 'v1', credentials=creds)
user_id='me'


def get_token(credentials_path):
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path,
        scopes = ['https://mail.google.com/']
    )
    token = flow.run_local_server(port=0)
    return token.to_json()


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def create_html_message(sender, to, subject, message_text, bcc=None):
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['bcc'] = bcc
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(message):
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    print(f'Message Id: {message["id"]}')
    return message
