import pusher
import os


pusher_client = pusher.Pusher(
        app_id=os.environ["PUSHER_APP_ID"],
        key=os.environ["PUSHER_KEY"],
        secret=os.environ["PUSHER_SECRET"],
        cluster='ap1',
        ssl=True)

def trigger(event, message):
    pusher_client.trigger(
            'autobot',
            event,
            {'message': message})
