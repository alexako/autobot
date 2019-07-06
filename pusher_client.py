import pusher

pusher_client = pusher.Pusher(
        app_id='817105',
        key='e9edd41d83c667edc487',
        secret='aded452ee915e13181cf',
        cluster='ap1',
        ssl=True)

def trigger(event, message):
    pusher_client.trigger(
            'autobot',
            event,
            {'message': message})
