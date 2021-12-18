"""Main application that subscribes to events."""

import logging
import os
import slack
from time import sleep

from emoji_message import EmojiMessage
from new_channel_message import NewChannelMessage
from new_user_message import NewUserMessage


logger = logging.getLogger(__name__)


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


@slack.RTMClient.run_on(event='team_join')
def new_user_callback(**payload) -> None:
    """Catch team_join event.

    Triggered when a user has joined the workspace.
    """
    web_client = payload['web_client']
    new_user = payload['data']['user']

    send_new_user_message(web_client, 'admin_logs', new_user)


def send_emoji_message(web_client: slack.WebClient, report_channel: str, emoji_name: str, event_type: str) -> None:
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
    except slack.errors.SlackApiError:
        # probably failed on auto-retry from slack client library, which will crash the app
        logger.error('Failed to post message to channel %s: %s', message.get('channel'), message.get('text'),
                     exc_info=True)
        logger.debug(message)

    # delay next request by 1.25 seconds for rate limited API
    sleep(1.25)

    message.update({'channel': 'emoji_meta', 'post_at': emoji_message.next_release_date()})
    try:
        web_client.chat_scheduleMessage(**message)
    except slack.errors.SlackApiError:
        # probably failed on auto-retry from slack client library, which will crash the app
        logger.error('Failed to schedule message to channel %s: %s', message.get('channel'), message.get('text'),
                     exc_info=True)
        logger.debug(message)

    # delay next request by 1.25 seconds for rate limited API
    sleep(1.25)


def send_new_channel_message(web_client: slack.WebClient, report_channel: str, new_channel_name: str) -> None:
    """Send a message to a channel about a new channel event.

    :param web_client: The client to respond on
    :param report_channel: The channel to send the message to
    :param new_channel_name: The name of the created channel
    """
    new_channel_message = NewChannelMessage(report_channel, new_channel_name)
    message = new_channel_message.get_message_payload()

    web_client.chat_postMessage(**message)

def send_new_user_message(web_client: slack.WebClient, report_channel: str, new_user: str) -> None:
    """Send a message to a channel about a new channel event.

    :param web_client: The client to respond on
    :param report_channel: The channel to send the message to
    :param new_user: The new slack user object
    """
    new_user_message = NewUserMessage(report_channel, new_user)
    message = new_user_message.get_message_payload()

    web_client.chat_postMessage(**message)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
    SLACK_TOKEN = os.environ['SLACK_BOT_TOKEN']
    rtm_client = slack.RTMClient(token=SLACK_TOKEN)
    rtm_client.start()
