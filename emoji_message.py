"""Constructs emoji report message."""

import datetime


class EmojiMessage:
    """Constructs emoji report message."""

    def __init__(self, report_channel, icon_emoji, event_type):
        """Initialize EmojiMessage.

        Created with the channel to send the message to, the event type that triggered the callback and the emoji to
        report on.

        :param report_channel: The channel to send the emoji message to
        :param icon_emoji: The name of the emoji
        :param event_type: The event that has happened, 'add' or 'remove'
        """
        self.report_channel = report_channel
        self.username = 'automod'
        self.icon_emoji = icon_emoji
        self.event_type = event_type
        self.timestamp = ''

    def get_message_payload(self) -> dict:
        """Format and returns information to post slack message.

        :return: Formatted information for slack
        """
        return {
            'ts': self.timestamp,
            'channel': self.report_channel,
            'username': self.username,
            'icon_emoji': self.icon_emoji,
            'text': self._get_message_text(),
        }

    def _get_past_tense_event(self) -> str:
        """Format the event type into past tense.

        :return: Past tense event type
        """
        return f'{self.event_type}d' if self.event_type[-1] == 'e' else f'{self.event_type}ed'

    def _get_message_text(self) -> str:
        """Create and returns formatted message text to send.

        :return: Formatted message text
        """
        return f':{self.icon_emoji}:  ({self.icon_emoji}) has been {self._get_past_tense_event()}'

    @staticmethod
    def next_release_date(release_hour: int = 3) -> int:
        """Get release time as Unix EPOCH timestamp"""
        utc_time = datetime.datetime.utcnow()
        if utc_time.hour >= release_hour:
            utc_time += datetime.timedelta(days=1)
        send_timestamp = utc_time.replace(hour=release_hour, minute=0, second=0, microsecond=0,
                                          tzinfo=datetime.timezone.utc).timestamp()
        return int(send_timestamp)
