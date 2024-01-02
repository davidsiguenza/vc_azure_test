from flask import Flask, render_template, request, redirect, url_for
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)

# Your Slack bot token
slack_token = 'xoxb-2323574213729-6434802430400-Gy0e8s1zoQ5DRdSAW33qtJz3'
client = WebClient(token=slack_token)

# ID of the user you want to monitor
user_id = 'U029UHX5ZBJ'

# Channel ID where you want to send notifications
channel_id = 'C06C6FLSR6G'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notify', methods=['POST'])
def notify():
    if is_user_online(user_id):
        send_notification(channel_id, f"User {get_user_name(user_id)} is online!")
    return redirect(url_for('index'))

def get_user_name(user_id):
    try:
        response = client.users_info(user=user_id)
        if response and response['user']:
            return response['user']['name']
    except SlackApiError as e:
        print(f"Error fetching user's information: {e}")
    return None

def is_user_online(user_id):
    try:
        response = client.users_getPresence(user=user_id)
        return response['presence'] == 'active'
    except SlackApiError as e:
        print(f"Error fetching user's presence: {e}")
        return False

def send_notification(channel, message):
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        print(f"Notification sent: {response['message']['text']}")
    except SlackApiError as e:
        print(f"Error sending notification: {e}")

if __name__ == '__main__':
    app.run(debug=True)