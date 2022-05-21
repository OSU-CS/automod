"""Main application that subscribes to events."""

import logging
import os
from time import sleep

from fastapi import FastAPI, Request
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_sdk import WebClient, errors

from emoji_message import EmojiMessage
from new_channel_message import NewChannelMessage
from new_user_message import NewUserMessage

logger = logging.getLogger(__name__)

app = App(
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET')
)

app_handler = SlackRequestHandler(app)


@app.event('emoji_changed')
def emoji_callback(client, event) -> None:
    """Catch emoji_changed event.

    Triggered when an emoji is added, removed, or when a new alias has been created.
    """
    event_type = event['subtype']
    emoji_name = event['name'] if event_type == 'add' else event['names'][0]

    send_emoji_message(client, 'admin', emoji_name, event_type)


@app.event('channel_created')
def new_channel_callback(client, event) -> None:
    """Catch channel_created event.

    Triggered when a channel has been created.
    """
    new_channel_name = event['channel']['name']

    send_new_channel_message(client, 'admin', new_channel_name)


@app.event('team_join')
def new_user_callback(client, event):
    """Catch team_join event.

    Triggered when a user has joined the workspace.
    """
    new_user = event['user']

    send_new_user_message(client, 'admin_logs', new_user)


def send_emoji_message(web_client: WebClient, report_channel: str, emoji_name: str, event_type: str) -> None:
    """Send a message to a channel about an emoji event.

    :param web_client: The client to respond on
    :param report_channel: The channel to send the message to
    :param emoji_name: The name of the emoji
    :param event_type: The event that has happened, 'add' or 'remove'
    """
    emoji_message = EmojiMessage(report_channel, emoji_name, event_type)
    message = emoji_message.get_message_payload()
    try:
        web_client.chat_postMessage(**message)
    except errors.SlackApiError:
        # probably failed on auto-retry from slack client library, which will crash the app
        logger.error('Failed to post message to channel %s: %s', message.get('channel'), message.get('text'),
                     exc_info=True)
        logger.debug(message)

    # delay next request by 1.25 seconds for rate limited API
    sleep(1.25)

    message.update({'channel': 'emoji_meta', 'post_at': emoji_message.next_release_date()})
    try:
        web_client.chat_scheduleMessage(**message)
    except errors.SlackApiError:
        # probably failed on auto-retry from slack client library, which will crash the app
        logger.error('Failed to schedule message to channel %s: %s', message.get('channel'), message.get('text'),
                     exc_info=True)
        logger.debug(message)

    # delay next request by 1.25 seconds for rate limited API
    sleep(1.25)


def send_new_channel_message(web_client: WebClient, report_channel: str, new_channel_name: str) -> None:
    """Send a message to a channel about a new channel event.

    :param web_client: The client to respond on
    :param report_channel: The channel to send the message to
    :param new_channel_name: The name of the created channel
    """
    new_channel_message = NewChannelMessage(report_channel, new_channel_name)
    message = new_channel_message.get_message_payload()

    web_client.chat_postMessage(**message)


def send_new_user_message(web_client: WebClient, report_channel: str, new_user: str) -> None:
    """Send a message to a channel about a new user event. Automatically pins the message.

    :param web_client: The client to respond on
    :param report_channel: The channel to send the message to
    :param new_user: The new slack user object
    """
    new_user_message = NewUserMessage(report_channel, new_user)
    message = new_user_message.get_message_payload()

    response = web_client.chat_postMessage(**message)

    # Pin this message to the channel
    web_client.pins_add(channel=response['channel'], timestamp=response['ts'])


api = FastAPI()


@api.post('/slack/events')
async def endpoint(req: Request):
    return await app_handler.handle(req)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
    app.start(port=int(os.environ.get("PORT", 3000)))
