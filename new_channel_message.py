"""Constructs new channel report message."""


class NewChannelMessage:
    """Constructs new channel report message."""

    def __init__(self, report_channel, new_channel):
        """Initialize NewChannelMessage.

        Created with the channel to send the message to and the channel that was created
        :param report_channel: The channel to send the new channel message to
        :param new_channel: The name of the newly created channel
        :param event_type: The event that has happened, 'add' or 'remove'
        """
        self.report_channel = report_channel
        self.username = 'automod'
        self.new_channel = new_channel
        self.timestamp = ''

    def get_message_payload(self) -> dict:
        """Format and returns information to post slack message.

        :return: Formatted information for slack
        """
        return {
            'ts': self.timestamp,
            'channel': self.report_channel,
            'username': self.username,
            'text': self._get_message_text(),
            'link_names': True,
        }

    def _get_message_text(self) -> str:
        """Create and returns formatted message text to send.

        :return: Formatted message text
        """
        return f'The channel #{self.new_channel} has been created'
