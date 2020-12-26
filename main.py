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
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,CarouselTemplate, CarouselColumn, ConfirmTemplate, PostbackAction, MessageAction
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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    notes = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='部屋の電気が付けっぱなしになっていませんか?照明のON/OFFを選択してください',
                actions=[
                    PostbackAction(
                        label='ON',
                        display_text='電気を付けました',
                        data='action=buy&itemid=1',
                        requests.get('https://192.168.10.130/H')
                    ),
                    MessageAction(
                        label='OFF',
                        text='電気を消しました',
                        requests.get('https://192.168.10.130/L')
                    )
                ]
            )
    )

    line_bot_api.reply_message(
        event.reply_token,
        notes)

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
