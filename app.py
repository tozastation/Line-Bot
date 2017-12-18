import json
import datetime
import pycurl
import requests
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

import bus_information
import information
import model
import nikonikodouga

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
info = information.Info()
YOUR_CHANNEL_ACCESS_TOKEN = info.get_ycat()
YOUR_CHANNEL_SECRET = info.get_ycs()
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


# index
@app.route('/')
def hello_world():
    return 'Hello World!'


# send a bus data
@app.route('/bus')
def send_bus():
    bus = bus_information.BusInfo()
    datas = bus.send_info()
    with model.db.transaction():
        for user in model.UserInfomation.select():
            if user.user_name == 'りょう':
                for data in datas:
                    late = data[0]
                    type = data[1]
                    end = data[2]
                    time = data[3]
                    if not(late in '無し'):
                        line1 = '予定 : '+late+'\n'
                        line2 = '系統 : '+type
                        line3 = '終点 : '+end+'\n'
                        line4 = '時刻 : '+time+'\n'
                        sentence = line3 + line4 + line1 + line2
                        try:
                            line_bot_api.push_message(user.user_id,
                                                      TextSendMessage(text=sentence))
                        except LineBotApiError as e:
                            print(e)
    model.db.commit()
    return 'OK\n'


@app.route('/send')
def send_morning():
    sentence = g.info.morning_information()
    with model.db.transaction():
        for user in model.get_user_id.select():
            try:
                line_bot_api.push_message(user.user_id,
                                          TextSendMessage(text=sentence))
            except LineBotApiError as e:
                    print(e)
    model.db.commit()
    return 'Complete to Send\n'


@app.route('/nikoniko/news')
def send_nikoniko_news():
    niko = nikonikodouga.Niko()
    titles = niko.send_niko_list('title')
    links = niko.send_niko_list('link')
    with model.db.transaction():
        for user in model.UserInfomation.select():
            line_bot_api.push_message(user.user_id,
                                      TextSendMessage(text='この時間のニュースうさ。'))
            for i in range(0, 5):
                try:
                    line_bot_api.push_message(user.user_id,
                                              TextSendMessage(text=titles[i] + '\n' + links[i]))
                except LineBotApiError as e:
                    print(e)
    model.db.commit()
    return 'Complete to Send\n'


# send a today's ranking
@app.route('/nikoniko/douga')
def send_nikoniko_douga():
    niko = nikonikodouga.Niko()
    titles = niko.send_send_list('title')
    links = niko.send_ranking_link('link')
    with model.db.transaction():
        for user in model.UserInfomation.select():
            line_bot_api.push_message(user.user_id,
                                      TextSendMessage(text='この時間の動画うさ。'))
            for i in range(0,10):
                try:
                    line_bot_api.push_message(user.user_id,
                                              TextSendMessage(text=titles[i]+'\n'+links[i]))
                except LineBotApiError as e:
                    print(e)
    model.db.commit()
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
    user_name_flag = '@name:'
    bus_flag = '@bus'
    model.db.create_tables([model.UserInfomation], safe=True)
    model.db.create_tables([model.LogInfomation], safe=True)
    user_id = event.source.user_id
    user_text = event.message.text
    # Insert User_ID
    with model.db.transaction():
        for user in model.UserInfomation.select():
            if user.user_id in user_id:
                duplication_flag = True

        if duplication_flag is False:
            model.UserInfomation.create(user_id=user_id)

    model.db.commit()
    # add user_name
    if user_name_flag in user_text:

        with model.db.transaction():
            user_name = user_text.replace(user_name_flag, '')
            query = model.UserInfomation.update(user_name=user_name).where(model.UserInfomation.user_id == user_id)
            query.execute()
        model.db.commit()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='登録したうさよ')
        )
    # activate curl command
    elif bus_flag in user_text:
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, 'https://damp-shelf-47440.herokuapp.com/bus')
        curl.perform()
    # reply a message
    # Docomo APIへ送信
    else:
        payload = {
            "utt": user_text,
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
        KEY = info.get_key() # API KEY
        url = endpoint + KEY
        s = requests.session()
        r = s.post(url, data=json.dumps(payload))
        res_json = json.loads(r.text)
        user = model.UserInfomation.get(model.UserInfomation.user_id == user_id)
        dear = 'なんだうさ。'+user.user_name+'さん。\n'
        reply = dear+str(res_json['utt'])

        with model.db.transaction():
            model.LogInfomation.create(log_text=user_text,
                                       log_owner=user_id,
                                       log_status='Receive',
                                       log_time=datetime.datetime.today())
            model.LogInfomation.create(log_text=reply,
                                       log_owner='Bot',
                                       log_status='Reply',
                                       log_time=datetime.datetime.today())
        model.db.commit()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))


if __name__ == '__main__':
    app.run(debug=True)