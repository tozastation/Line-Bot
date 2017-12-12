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


@app.route('/send')
def send_morning():
    API_KEY = "b658161bac2942afc45703a43ff1b362"
    api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
    city_name = 'Hakodate'
    url = api.format(city=city_name, key=API_KEY)
    print(url)
    response = requests.get(url)
    data = json.loads(response.text)
    K = 273.15
    city = data['name']
    temp = round(data['main']['temp'] - K, 2)
    weather = data["weather"][0]["main"]
    sentence1 = "おはよううさ。今日の天気うさ!!今日も一日頑張るうさ!!!!\nうるさ!!!!\n"
    sentence2 = 'City : ' + str(city) + '\n'
    sentence3 = 'Temp : ' + str(temp) + '\n'
    sentence4 = 'Weather : ' + str(weather)
    sentence = sentence1 + sentence2 + sentence3 + sentence4
    with model.db.transaction():
        for user in model.get_user_id.select():
            try:
                line_bot_api.push_message(user.user_id,
                                          TextSendMessage(text=sentence)
                                          )
            except LineBotApiError as e:
                    print(e)
    model.db.commit()





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
    flag = False
    try:
        model.db.create_tables([model.get_user_id], safe=True)
        with model.db.transaction():
            for user in model.get_user_id.select():
                if user.user_id == event.source.user_id:
                    flag = True
            if flag==False:
                model.get_user_id.create(user_id=event.source.user_id)
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