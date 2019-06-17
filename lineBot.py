import requests
from bs4 import BeautifulSoup
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

line_bot_api = LineBotApi('a4XnVnNOME2FAOkNrWWi1ixaQTopLbelJmPjo4E31Ex7Qs1XVpTld0lgV9IAt3Uv0eaNygTVU2R5uLblIL/FhUskyKPQusj5cBAyxkgzdaq41UnYx41kDODtfv/icw2gRxm9qi117UHfEV3TWnZXHwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c96255a9b07b5b5f22ef450f32710210')


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
    text=event.message.text
    if text[0] == '@':
        response = requests.get('https://www.youtube.com/results?search_query={}'.format(text[1:]))
        soup = BeautifulSoup(response.text, 'html.parser')
        watch_list = []
        for link in soup.findAll('a'):
            if '/watch?v='in link.get('href'):
                watch_list.append(link.get('href'))
        return_text = 'https://www.youtube.com'+watch_list[0]
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text='This is your YouTube video.'))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=return_text))


if __name__ == "__main__":
    app.run()
