
import os

import firebase_admin
from firebase_admin import credentials, messaging


class CloudMessaging:
    def __init__(self, base_dir):
        path = f"{base_dir}/main/whispersms-firebase-adminsdk-e9ml9-bf5fbf7400.json"
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)

    def send_broadcast(self, token, title, body):
        # See documentation on defining a message payload.

        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title="Whisper Mobile",
                    body="You have a notification"
                ),
                data={"title": title, "body": body},
                token=token,
            )

            # Send a message to the device corresponding to the provided
            # registration token.
            response = messaging.send(message)
            # Response is a message ID string.
            print('Successfully sent message:', response)
        except Exception as e:
            print(e)

    @staticmethod
    def send_beep_to_buddy(token, name):
        message = messaging.Message(
            notification=messaging.Notification(
                title="Beeep Alert",
                body="Beeep alert sent from {}".format(name)
            ),
            data={"name": name},
            token=token,
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
