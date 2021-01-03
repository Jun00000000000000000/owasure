from flask import Flask, request, abort
import os
import requests

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,CarouselTemplate, CarouselColumn, ConfirmTemplate, PostbackAction, MessageAction, URIAction
    )

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

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

global state
state=0
@app.route("/ToI", methods=["GET"])
def handle_get_request():
    global state

    tmp = state
    state = 0
    if tmp!=0:
        print("accept_"+str(tmp))
        #line_bot_api.push_message("Ufe327b70ea9290e56a4a2e7fabd00165",TextSendMessage(text="accept_"+str(tmp)))

    return str(tmp)

@app.route("/Sensor",methods=["GET"])
def handle_get_request2():
    line_bot_api.push_message("Ufe327b70ea9290e56a4a2e7fabd00165",TextSendMessage(text="test"))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text=event.message.text
    global state
    confirm_template_message = TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text='部屋の電気が付けっぱなしになっていませんか？照明のON/OFFを選択してください',
            actions=[
                MessageAction(
                    label='ON',
                    text='消しません'
                ),
                MessageAction(
                    label='OFF',
                    text='消します'
                )
            ]
        )
    )
    if text == "消します":
        line_bot_api.reply_message(event.reply_token,messages=TextSendMessage(text="部屋の電気はOFFの状態です！"))
        state = 1
    elif text=="test":
        line_bot_api.reply_message(event.reply_token,messages=confirm_template_message)
        state = 0
    elif text == "消しません":
        line_bot_api.reply_message(event.reply_token,messages=TextSendMessage(text="部屋の電気はONの状態です！"))
        state = 2
    else:
        state = 0

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
