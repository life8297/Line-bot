from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('X0gP+cWBHE6WbHfl9YDcYWnUx5/J6Ox+mn0L5OxsPKtu4l3KxTSi8XdHYkzkR2rXdYCsUR61m43zwI2A8RPCQUBeh23KVK2R8mX8uBlbVxtTPp+lZZjtp/pilmRniFLDi4AG5cv3Zp25SfLRR3Z8zgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5b40fa88ea63178ae5a49c26a098bb7b')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()