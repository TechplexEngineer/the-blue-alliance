from tbans.models.notifications.notification import Notification


class VerificationNotification(Notification):
    """ Verification notification - used for webhooks to ensure the proper people are in control

    Attributes:
        url (string): The URL to send the notification payload to.
        secret (string): The secret to calculate the payload checksum with.
        verification_key (string): SHA1 of url + secret
    """

    def __init__(self, url, secret):
        """
        Args:
            url (string): The URL to send the notification payload to.
            secret (string): The secret to calculate the payload checksum with.
        """
        from tbans.utils.validation_utils import validate_is_string, validate_is_type
        # Check url
        validate_is_string(url=url)

        # Check secret
        validate_is_type(basestring, not_empty=False, secret=secret)

        self.url = url
        self.secret = secret
        self._generate_key()

    def _generate_key(self):
        import hashlib
        ch = hashlib.sha1()
        import time
        ch.update(str(time.time()))
        ch.update(self.url)
        ch.update(self.secret)
        self.verification_key = ch.hexdigest()

    @staticmethod
    def _type():
        from consts.notification_type import NotificationType
        return NotificationType.VERIFICATION

    # Only webhook payload is defined - because we'll only ever send verification to webhooks
    @property
    def webhook_payload(self):
        return {'verification_key': self.verification_key}

    def _additional_logging_values(self):
        return [(self.verification_key, 'verification_key')]
