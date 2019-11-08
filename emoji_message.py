"""Constructs emoji report message."""

import datetime


class EmojiMessage:
    """Constructs emoji report message."""

    def __init__(self, channel, icon_emoji, event_type):
        """Initialize EmojiMessage.

        Created with the channel to send the message to, the event type that triggered the callback and the emoji to
        report on.

        :param channel: The channel to send the emoji message to
        :param icon_emoji: The name of the emoji
        :param event_type: The event that has happened, 'add' or 'remove'
        """
        self.channel = channel
        self.username = 'automod'
        self.icon_emoji = icon_emoji
        self.event_type = event_type
        self.timestamp = ''

    def get_message_payload(self):
        """Format and returns information to post slack message.

        :return: Formatted information for slack
        """
        return {
            'ts': self.timestamp,
            'channel': self.channel,
            'username': self.username,
            'icon_emoji': self.icon_emoji,
            'blocks': [self._get_message_block()],
        }

    def _get_past_tense_event(self):
        """Format the event type into past tense.

        :return: Past tense event type
        """
        return f'{self.event_type}d' if self.event_type[-1] == 'e' else f'{self.event_type}ed'

    def _get_message_block(self):
        """Create and returns formatted message block to send.

        :return: Formatted message block
        """
        return {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f':{self.icon_emoji}:  ({self.icon_emoji}) has been {self._get_past_tense_event()}',
            },
        }

    @staticmethod
    def next_release_date() -> str:
        """Get release time as Unix EPOCH timestamp"""
        utc_time = datetime.datetime.utcnow()
        days = 1 if utc_time.hour >= 3 else 0
        offset_time = utc_time + datetime.timedelta(days=days)
        send_timestamp = offset_time.replace(hour=3, minute=0, second=0, microsecond=0,
                                             tzinfo=datetime.timezone.utc).timestamp()
        return str(send_timestamp)
