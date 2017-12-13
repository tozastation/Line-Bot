from flask import Flask, request, abort, g
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import settings
import model
import requests
import json


app = Flask(__name__)
g.info = settings.Info()
YOUR_CHANNEL_ACCESS_TOKEN = g.info.get_YCAT()
YOUR_CHANNEL_SECRET = g.info.get_YCS()
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/send')
def send_morning():
    push_man = settings.Push()
    sentence = push_man.morning_information()

    with model.db.transaction():
        for user in model.get_user_id.select():
            try:
                line_bot_api.push_message(user.user_id,
                                          TextSendMessage(text=sentence)
                                          )
            except LineBotApiError as e:
                    print(e)
    model.db.commit()
    return 'Complete to Send'

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
    # connect to database
    # insert user_id
    duplication_flag = False
    try:
        model.db.create_tables([model.UserInfomation], safe=True)
        with model.db.transaction():
            for user in model.UserInfomation.select():
                if user.user_id in event.source.user_id:
                    duplication_flag = True
            if duplication_flag is False:
                model.UserInfomation.create(user_id=event.source.user_id)
        model.db.commit()
    except Exception as e:
        print(e)
    # send a message
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
    endpoint = g.info.get_endpoint()
    KEY = g.info.get_KEY()
    url = endpoint+KEY
    s = requests.session()
    r = s.post(url, data=json.dumps(payload))
    res_json = json.loads(r.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(res_json['utt']))
    )


if __name__ == '__main__':
    app.run(debug=True)