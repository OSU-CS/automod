"""Constructs emoji report message."""
class EmojiMessage:
    """Constructs emoji report message."""

    def __init__(self, channel, icon_emoji, event_type):
        """Initializes EmojiMessage with the channel to send the message to and the emoji to report on

        Arguments:
            channel {string}    -- The channel to send the emoji message to
            icon_emoji {string} -- The name of the emoji
            event_type {str}    -- The event that has happened, either 'add' or 'remove'
        """
        self.channel = channel
        self.username = "automod"
        self.icon_emoji = icon_emoji
        self.event_type = event_type
        self.timestamp = ""


    def get_message_payload(self):
        """Formats and returns information to post slack message

        Returns:
            object -- Formatted information for slack
        """
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                *self._get_message_block()
            ],
        }


    def _get_past_tense_event(self):
        """Formats the event type into past tense

        Returns:
            str -- The past tense event type
        """

        return f"{self.event_type}d" if self.event_type[-1] == 'e' else f"{self.event_type}ed"


    def _get_message_block(self):
        """Creates and returns formatted message block to send

        Returns:
            object -- The formatted message block
        """
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":{self.icon_emoji}: ({self.icon_emoji}) has been {self._get_past_tense_event()}"
                }
            }
