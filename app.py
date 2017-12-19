import json
import datetime
import requests
import bus_information
import information
import model
import nikonikodouga
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


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
info = information.Info()
YOUR_CHANNEL_ACCESS_TOKEN = info.get_ycat()
YOUR_CHANNEL_SECRET = info.get_ycs()
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


# バス接近情報
@app.route('/bus')
def send_bus():
    bus = bus_information.BusInfo()
    data_list = bus.send_info()

    with model.db.transaction():
        for user in model.UserInfomation.select():
            for data in data_list:
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


# 天気予報
@app.route('/weather')
def send_morning():
    text = info.morning_information()

    with model.db.transaction():
        for user in model.get_user_id.select():
            try:
                line_bot_api.push_message(user.user_id,
                                          TextSendMessage(text=text))
            except LineBotApiError as e:
                    print(e)
    model.db.commit()
    return 'Complete to Send\n'


# ニコニコ動画「ニュース」
@app.route('/nikoniko/news')
def send_nikoniko_news():
    niko = nikonikodouga.Niko()
    titles = niko.send_niko_list('title', 'news')
    links = niko.send_niko_list('link', 'news')

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


# ニコニコ動画「ランキング」
@app.route('/nikoniko/ranking')
def send_nikoniko_douga():
    niko = nikonikodouga.Niko()
    titles = niko.send_niko_list('title', 'ranking')
    links = niko.send_niko_list('link', 'ranking')

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

    # Check Duplication
    duplication_flag = False

    # コマンド @name
    user_name_flag = '@name'
    # コマンド @bus
    bus_flag = '@bus'
    # コマンド @help
    get_command_flag = '@help'
    # コマンド @help
    get_weather_flag = '@weather'
    # コマンド @course
    get_course_flag = '@course'
    # コマンド @course
    get_no_class_flag = '@noclass'

    # テーブル作成
    model.db.create_tables([model.UserInfomation], safe=True)
    model.db.create_tables([model.LogInfomation], safe=True)
    # 送信元ユーザID取得
    user_id = event.source.user_id
    # 送信元テキスト取得
    user_text = event.message.text

    # ユーザID取得
    with model.db.transaction():
        for user in model.UserInfomation.select():
            if user.user_id in user_id:
                duplication_flag = True

        if duplication_flag is False:
            model.UserInfomation.create(user_id=user_id)

    model.db.commit()
    # ユーザ名登録
    if user_name_flag in user_text:

        with model.db.transaction():
            user_name = user_text.replace(user_name_flag, '')
            query = model.UserInfomation.update(user_name=user_name).where(model.UserInfomation.user_id == user_id)
            query.execute()
        model.db.commit()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='登録したうさ。'))

    # コース登録
    elif get_course_flag in user_text:

        with model.db.transaction():
            user_course = user_text.replace(get_course_flag, '')
            query = model.UserInfomation.update(user_course=user_course).where(model.UserInfomation.user_id == user_id)
            query.execute()
        model.db.commit()

    # 休講情報Push
    elif get_no_class_flag in user_text:

        with model.db.transaction():
            for user in model.UserInfomation.select():
                for no_class in model.NoClass.select():
                    if not(user.user_course is None):
                        if user.user_course in no_class.class_target:
                            line_one = no_class.status
                            line_two = '曜日 : ' + no_class.class_date + '(' + no_class.class_day + ')' + no_class.class_time
                            line_three = '授業名 : ' + no_class.class_name
                            line_four = '担当教員 : ' + no_class.class_teacher
                            line_five = '該当コース : ' + no_class.class_target
                            text = line_one + '\n' + line_two + '\n' + line_three + '\n' + line_four + '\n' + line_five
                            line_bot_api.push_message(user.user_id,
                                                      TextSendMessage(text=text))
                    else:
                        text = '登録してないうさ。'
                        line_bot_api.push_message(user.user_id,
                                                  TextSendMessage(text=text))

    # @bus
    elif bus_flag in user_text:
        r = requests.get('https://damp-shelf-47440.herokuapp.com/bus')
        r.json()

    # @help
    elif get_command_flag in user_text:
        func_name = '@name : ユーザー名の追加\n(ex.@nameRabbit)\n'
        func_course = '@course : コースの登録\n(ex.@name2-ABCD)\n'
        func_bus = '@bus : バス接近情報の取得\n'
        func_no_class = '@noclass : 休講情報の取得\n'
        func_weather = '@weather : 天気の取得'
        text = func_name + func_course + func_no_class + func_bus + func_weather

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))

    # @weather
    elif get_weather_flag in user_text:
        r = requests.get('https://damp-shelf-47440.herokuapp.com/weather')
        r.json()
    else:
        # ドコモAPI
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

        # API EndPoint
        endpoint = info.get_endpoint()
        # API KEY
        KEY = info.get_key()
        url = endpoint + KEY
        s = requests.session()
        r = s.post(url, data=json.dumps(payload))
        res_json = json.loads(r.text)

        user = model.UserInfomation.get(model.UserInfomation.user_id == user_id)
        dear = ''
        if not(user.user_name is None):
            dear = 'なんだうさ。'+user.user_name+'さん。\n'
        text = dear + str(res_json['utt'])

        with model.db.transaction():
            model.LogInfomation.create(log_text=user_text,
                                       log_owner=user_id,
                                       log_status='Receive',
                                       log_time=datetime.datetime.today())
            model.LogInfomation.create(log_text=text,
                                       log_owner='Bot',
                                       log_status='Reply',
                                       log_time=datetime.datetime.today())
        model.db.commit()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))


if __name__ == '__main__':
    app.run(debug=True)