from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, VideoMessage,
    FollowEvent, UnfollowEvent, PostbackEvent, TemplateSendMessage,
    ButtonsTemplate, CarouselTemplate, CarouselColumn, PostbackTemplateAction
)
from linebot.exceptions import LineBotApiError

import urllib3.request
import os
import sc

app = Flask(__name__)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['x-line-signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  text = event.message.text
  if '位置情報' in text:
    line_bot_api.reply_message(
      event.reply_token,
      [
      TextSendMessage(text='位置情報を教えてください。'),
      TextSendMessage(text='line://nv/location')
      ]
    )

@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    text = event.message.address
    print(text)
    result = sc.get_weather_from_location(text)
    line_bot_api.reply_message(
        event.reply_token,
        [
        TextSendMessage(text=result)
        ]
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
