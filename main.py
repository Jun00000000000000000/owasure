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
    print("accept_"+str(tmp))
    line_bot_api.push_message("user_id",TextSendMessage(text="accept_"+str(tmp)))

    return str(tmp)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global state
    notes = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='部屋の電気が付けっぱなしになっていませんか?照明のON/OFFを選択してください',
                actions=[
                    URIAction(
                        type="uri",
                        label='ON',
                        uri='192.168.10.130'
                    ),
                    URIAction(
                        type="uri",
                        label='OFF',
                        uri='eromanga-select.com/%E6%B0%B4%E5%B9%B3%E7%B7%9A/%E3%80%90%E3%82%A8%E3%83%AD%E6%BC%AB%E7%94%BB%E3%80%91%E5%B7%A8%E4%B9%B3%E5%B9%BC%E3%81%AA%E3%81%98%E3%81%BF%E3%81%8B%E3%82%89%E9%A0%BC%E3%81%BE%E3%82%8C%E3%81%A6%E3%82%AA%E3%83%8A%E3%83%8B%E3%83%BC/'
                    )
                ]
            )
    )
    line_bot_api.reply_message(
        event.reply_token,
        messages)

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
