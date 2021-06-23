import time
import ldclient
import threading


from ldclient.config import Config
from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123456789$"

socketio = SocketIO(app, cors_allowed_origins="*")

app.host = 'localhost'

###### LaunchDarkly SDK Key Goes HERE ######
ld_sdk_key = ""
ldclient.set_config(Config(ld_sdk_key))
ld_client = ldclient.get()


###### LaunchDarkly User Context ######
user = {
    "key" : "test",
    "firstName" : "Space",
    "lastName" : "Camp",
    "email" : "spacecamp@launchdarkly.com"
}


###### LaunchDarkly Feature Flag Goes HERE ######
def get_variation(user={"key":"test"}):
    return ld_client.variation("my-feature-flag", user, "Not Set Up") # Add your flag here!



###### Websockets for updates #######
@socketio.on('connect')
def connected():
    send("%s-%s" % (user['key'], get_variation(user)), broadcast=True)

@socketio.on('disconnect')
def disconnected():
    print('Disconnected')

@socketio.on("message")
def handleMessage(msg): 
    print("handling message")
    user.update({"key": msg})




















###### Helper Code ######
class FlagPoller(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            
        thread.start()                                  

    def run(self):
        current_variation = get_variation(user)
        current_user_key = user['key']
        print("CURRENT VARIATION IS %s" % current_variation)

        while True:
            if current_variation != get_variation(user) or current_user_key != user['key']:
                print("variation changed")
                print("current_variation: %s" % current_variation)
                print("get_variation(user): %s" % get_variation(user))
                socketio.send("%s-%s" % (user['key'], get_variation(user)), broadcast=True)
                current_variation = get_variation(user)
                current_user_key = user['key']
            else:
                pass
            time.sleep(self.interval)

flag_poller = FlagPoller()

if __name__ == '__main__':
    socketio.run(app, debug=True) 