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
import settings
import model
import requests
import json


app = Flask(__name__)
line_bot_api = LineBotApi(settings.YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNEL_SECRET)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/send', methods=['GET'])
def send_morning():
    user_ids = []
    for user_id in model.Get_Text.select():
        user_ids.append(user_id.user_id)

    try:
        line_bot_api.push_message(user_ids,
                                  TextSendMessage(text='Hello World!')
                                  )
    except LineBotApiError as e:
        print(e)


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
    try:
        model.db.create_tables([model.Get_Text], safe=True)
        with model.db.transaction():
            model.Get_Text.create(user_id=event.source.user_id)
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
    url = settings.endpoint+settings.KEY
    s = requests.session()
    r = s.post(url, data=json.dumps(payload))
    res_json = json.loads(r.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(res_json['utt']))
    )


if __name__ == '__main__':
    app.run(debug=True)