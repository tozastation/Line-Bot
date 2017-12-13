from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from settings import Info, Push
from model import *
import requests
import json


app = Flask(__name__)
info = Info()
YOUR_CHANNEL_ACCESS_TOKEN = info.get_YCAT()
YOUR_CHANNEL_SECRET = info.get_YCS()
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/send')
def send_morning():
    push_man = Push()
    sentence = push_man.morning_information()
    with db.transaction():
        for user in get_user_id.select():
            try:
                line_bot_api.push_message(user.user_id,
                                          TextSendMessage(text=sentence)
                                          )
            except LineBotApiError as e:
                    print(e)
    db.commit()
    return 'Complete to Send\n'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK\n'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Create Table
    duplication_flag = False
    db.create_tables([UserInfomation], safe=True)
    db.create_tables([LogInfomation], safe=True)
    try:
        # Insert User_ID
        with db.transaction():
            for user in UserInfomation.select():
                if user.user_id in event.source.user_id:
                    duplication_flag = True
            if duplication_flag is False:
                UserInfomation.create(user_id=event.source.user_id)
        db.commit()
    except Exception as e:
        print(e)
    # reply a message
    payload = {
        "utt": event.message.text,
        "context": "",
        "nickname": "",
        "nickname_y": "",
        "sex": "",
        "bloodtype": "",
        "birthdateY": "",
        "birthdateM": "",
        "birthdateD": "",
        "age": "",
        "constellations": "",
        "place": "北海道",
        "mode": "dialog"
    }
    endpoint = info.get_endpoint() # API EndPoint
    KEY = info.get_KEY() # API KEY
    url = endpoint+KEY
    s = requests.session()
    r = s.post(url, data=json.dumps(payload))
    res_json = json.loads(r.text)
    try:
        with db.transaction():
            LogInfomation.create(log_text=event.message.text, log_owner=event.source.user_id, log_status='Receive')
            LogInfomation.create(log_text=str(res_json['utt']), log_owner='Bot', log_status='Reply')
        db.commit()
    except Exception as e:
        return e
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(res_json['utt']))
    )


if __name__ == '__main__':
    app.run(debug=True)