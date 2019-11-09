"""Main application that subscribes to events."""

import os
import slack
from emoji_message import EmojiMessage


@slack.RTMClient.run_on(event='emoji_changed')
def emoji_callback(**payload) -> None:
    """Catch emoji_changed event.

    Triggered when an emoji is added, removed, or when a new alias has been created.
    """
    web_client = payload['web_client']

    event_type = payload['data']['subtype']
    emoji_name = payload['data']['name'] if event_type == 'add' else payload['data']['names'][0]

    send_emoji_message(web_client, 'admin', emoji_name, event_type)


def send_emoji_message(web_client: slack.WebClient, channel: str, emoji_name: str, event_type: str) -> None:
    """Send a message to a channel about an emoji event.

    :param web_client: The client to respond on
    :param channel: The channel to send the message to
    :param emoji_name: The name of the emoji
    :param event_type: The event that has happened, 'add' or 'remove'
    """
    emoji_message = EmojiMessage(channel, emoji_name, event_type)
    message = emoji_message.get_message_payload()

    web_client.chat_postMessage(**message)

    message.update({'channel': 'emoji_meta',
                    'post_at': emoji_message.next_release_date(),
                    'text': message.get('blocks')[0].get('text').get('text')})
    web_client.chat_scheduleMessage(**message)


if __name__ == '__main__':
    SLACK_TOKEN = os.environ['SLACK_BOT_TOKEN']
    rtm_client = slack.RTMClient(token=SLACK_TOKEN)
    rtm_client.start()
