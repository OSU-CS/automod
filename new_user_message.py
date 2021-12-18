"""Constructs user report message."""

class NewUserMessage:
    """Constructs user report message."""

    def __init__(self, report_channel, new_user):
        """Initialize UserMessage.

        Created with the channel to send the message to and the new.

        :param report_channel: The channel to send the user message to
        :param user: The new user
        """
        self.report_channel = report_channel
        self.username = 'automod'
        self.new_user_id = new_user['id']
        self.new_user_display_name = new_user['name']
        self.new_user_real_name = new_user['real_name']
        self.new_user_email = new_user['profile']['email']
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
        return (
            f'New user has joined the workspace: @{self.new_user_display_name}\n'
            f'Email: {self.new_user_email}\n'
            f'Full Name: {self.new_user_real_name}\n'
            f'UID: {self.new_user_id}'
        )
