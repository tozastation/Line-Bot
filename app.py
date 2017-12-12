from flask import Flask, request, abort, jsonify
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


app = Flask(__name__)

line_bot_api = LineBotApi(settings.YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNEL_SECRET)


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
    sentence = event.message.text
    try:
        model.db.create_tables([model.Get_Text], safe=True)
        with model.db.transaction():
            model.Get_Text.create(sentence_id=1, sentence=sentence)
        model.db.commit()
    except Exception as e:
        print(e)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))



if __name__ == '__main__':
    app.run(debug=True)