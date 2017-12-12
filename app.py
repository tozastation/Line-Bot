from flask import Flask, request, abort, jsonify, g
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import settings
import model
import psycopg2
import requests
import json

app = Flask(__name__)

line_bot_api = LineBotApi(settings.YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNEL_SECRET)
g.context = ""

@app.route('/')
def hello_world():
    return 'Hello World!'


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

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # connect to database
    try:
        model.db.create_tables([model.Get_Text], safe=True)
        with model.db.transaction():
            model.Get_Text.create(body=event.message.text)
        model.db.commit()
    except Exception as e:
        print(e)
    # send a message
    payload = {
        "utt": event.message.text,
        "context": g.context,
        "nickname": event.source.type,
        "birthdateY": "1997",
        "birthdateM": "11",
        "birthdateD": "5",
        "age": "20",
        "constellations": "蠍座",
        "place": "北海道",
        "mode": "srtr"
    }
    KEY = '2f42326a4d52784249447133356f656338317a3373464a4c4d6c73506a462f72574331687568694a637641'
    endpoint = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=REGISTER_KEY'
    url = endpoint.replace('REGISTER_KEY', KEY)
    s = requests.session()
    r = s.post(url, data=json.dumps(payload))
    res_json = json.loads(r.text)
    g.context = res_json['context']
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(res_json['utt']))
    )



if __name__ == '__main__':
    app.run(debug=True)