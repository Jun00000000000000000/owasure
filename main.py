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

global state
state=0
@app.route("/IoT", methods=["GET"])
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
                    PostbackAction(
                        label='ON',
                        display_text='電気を付けました',
                        data='action=buy&itemid=1',
                        uri='https://192.168.10.130'
                    ),
                    MessageAction(
                        label='OFF',
                        text='電気を消しました',
                        uri='https://192.168.10.130/L/'
                    )
                ]
            )
    )
    if text == "ToI! ON!":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=dry[np.random.randint(2)]))
        state = 1

    elif text == "ToI! OFF!":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=cool[np.random.randint(2)]))
        state = 2
    
    line_bot_api.reply_message(
        event.reply_token,
        notes)

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
