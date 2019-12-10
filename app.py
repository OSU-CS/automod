"""Main application that subscribes to events."""

import os
import slack

from emoji_message import EmojiMessage
from new_channel_message import NewChannelMessage


@slack.RTMClient.run_on(event='emoji_changed')
def emoji_callback(**payload) -> None:
    """Catch emoji_changed event.

    Triggered when an emoji is added, removed, or when a new alias has been created.
    """
    web_client = payload['web_client']
    event_type = payload['data']['subtype']
    emoji_name = payload['data']['name'] if event_type == 'add' else payload['data']['names'][0]

    send_emoji_message(web_client, 'admin', emoji_name, event_type)


@slack.RTMClient.run_on(event='channel_created')
def new_channel_callback(**payload) -> None:
    """Catch channel_created event.

    Triggered when a channel has been created.
    """
    web_client = payload['web_client']
    new_channel_name = payload['data']['channel']['name']

    send_new_channel_message(web_client, 'admin', new_channel_name)


def send_emoji_message(web_client: slack.WebClient, report_channel: str, emoji_name: str, event_type: str) -> None:
    """Send a message to a channel about an emoji event.

    :param web_client: The client to respond on
    :param report_channel: The channel to send the message to
    :param emoji_name: The name of the emoji
    :param event_type: The event that has happened, 'add' or 'remove'
    """
    emoji_message = EmojiMessage(report_channel, emoji_name, event_type)
    message = emoji_message.get_message_payload()

    web_client.chat_postMessage(**message)

    message.update({'channel': 'emoji_meta', 'post_at': emoji_message.next_release_date()})
    web_client.chat_scheduleMessage(**message)


def send_new_channel_message(web_client: slack.WebClient, report_channel: str, new_channel_name: str) -> None:
    """Send a message to a channel about a new channel event.

    :param web_client: The client to respond on
    :param report_channel: The channel to send the message to
    :param new_channel_name: The name of the created channel
    """
    new_channel_message = NewChannelMessage(report_channel, new_channel_name)
    message = new_channel_message.get_message_payload()

    web_client.chat_postMessage(**message)


if __name__ == '__main__':
    SLACK_TOKEN = os.environ['SLACK_BOT_TOKEN']
    rtm_client = slack.RTMClient(token=SLACK_TOKEN)
    rtm_client.start()
