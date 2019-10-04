"""Main application that subscribes to events."""

import os
import ssl as ssl_lib
import certifi
import slack
from emoji_message import EmojiMessage


@slack.RTMClient.run_on(event='emoji_changed')
def onboarding_message(**payload):
    """Catch emoji_changed event.

    Triggered when an emoji is added, removed, or when a new alias has been created.
    """
    web_client = payload['web_client']

    emoji_name = payload['data']['name']
    event_type = payload['data']['subtype']

    send_emoji_message(web_client, 'admin', emoji_name, event_type)


def send_emoji_message(web_client: slack.WebClient, channel: str, emoji_name: str, event_type: str):
    """Send a message to a channel about an emoji event.

    Arguments:
        web_client {slack.WebClient} -- The client to respond on
        channel {str}                -- The channel to send the message to
        emoji_name {str}             -- The name of the emoji
        event_type {str}             -- The event that has happened, 'add' or 'remove'
    """
    emoji_message = EmojiMessage(channel, emoji_name, event_type)
    message = emoji_message.get_message_payload()

    web_client.chat_postMessage(**message)


if __name__ == '__main__':
    SSL_CONTEXT = ssl_lib.create_default_context(cafile=certifi.where())
    SLACK_TOKEN = os.environ['SLACK_BOT_TOKEN']
    RTM_CLIENT = slack.RTMClient(token=SLACK_TOKEN, ssl=SSL_CONTEXT)
    RTM_CLIENT.start()
