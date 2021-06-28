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
ld_sdk_key = "sdk-204e704c-35b7-4b99-95e3-522a58d5151c"
ldclient.set_config(Config(ld_sdk_key))
ld_client = ldclient.get()


###### LaunchDarkly Initialization Context ######
init_context = {
    "key" : "test",
    "ip" : "192.168.1.1",
    "country" : "USA",
    "custom" : {
        "group" : "beta",
        "serviceType" : "staging"
    }
}


###### LaunchDarkly Feature Flag Goes HERE ######
def get_variation(init_context={"key":"test"}):
    return ld_client.variation("stringFlag", init_context, "Not Set Up") # Add your flag here!



###### Websockets for updates #######
@socketio.on('connect')
def connected():
    send("%s-%s" % (init_context['key'], get_variation(init_context)), broadcast=True)

@socketio.on('disconnect')
def disconnected():
    print('Disconnected')

@socketio.on("message")
def handleMessage(msg): 
    print("handling message")
    init_context.update({"key": msg})




















###### Helper Code ######
class FlagPoller(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            
        thread.start()                                  

    def run(self):
        current_variation = get_variation(init_context)
        current_key = init_context['key']
        print("CURRENT VARIATION IS %s" % current_variation)

        while True:
            if current_variation != get_variation(init_context) or current_key != init_context['key']:
                print("variation changed")
                print("current_variation: %s" % current_variation)
                print("get_variation(init_context): %s" % get_variation(init_context))
                socketio.send("%s-%s" % (init_context['key'], get_variation(init_context)), broadcast=True)
                current_variation = get_variation(init_context)
                current_key = init_context['key']
            else:
                pass
            time.sleep(self.interval)

flag_poller = FlagPoller()

if __name__ == '__main__':
    socketio.run(app, debug=True) 