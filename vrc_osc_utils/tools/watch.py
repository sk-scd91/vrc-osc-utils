from datetime import datetime
from time import sleep
from vrc_osc_utils import avatar_params

from vrc_osc_utils.avatar_params import AvatarParamFactory

def send_datetime(client, avatar_params, time):
    bundle = avatar_params.bundle(Hour=time.hour, Minute=time.minute, Second=time.second)
    client.send(bundle)

def run_sync(client, delay = 60.0, avatar_schema = None):
    print("Starting watch service...")
    avatar_params = AvatarParamFactory(avatar_schema)
    try:
        while True:
            now = datetime.utcnow()
            print(f"Sending time... {now.hour}:{now.minute}:{now.second}")
            send_datetime(client, avatar_params, now)
            print("Time successfully sent.")
            sleep(delay)
    except KeyboardInterrupt:
        print("Ending watch service...")