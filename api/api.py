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


###### LaunchDarkly Initialization Context ######
astronaut = {
    "key" : "Toggle",
    "country" : "USA",
    "email" : "Toggle_the_astronaut@nasa.gov",
    "privateAttributes" : ["email"],
    "custom" : {
        "spaceStation" : "ISS",
        "employer" : "NASA",
        "visitedPlanets": ["earth", "mars"]
    }
}


###### LaunchDarkly Feature Flag Goes HERE ######
def get_variation(astronaut={"key":"test"}):
    return ld_client.variation("FEATURE-FLAG-HERE", astronaut, "somewhere") # Add your flag here!



###### Websockets for updates #######
@socketio.on('connect')
def connected():
    send("%s-%s" % (astronaut['key'], get_variation(astronaut)), broadcast=True)

@socketio.on('disconnect')
def disconnected():
    print('Disconnected')

@socketio.on("message")
def handleMessage(msg): 
    print("handling message")
    astronaut.update({"key": msg})




















###### Helper Code ######
class FlagPoller(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            
        thread.start()                                  

    def run(self):
        current_variation = get_variation(astronaut)
        current_key = astronaut['key']
        print("CURRENT VARIATION IS %s" % current_variation)

        while True:
            if current_variation != get_variation(astronaut) or current_key != astronaut['key']:
                print("variation changed")
                print("current_variation: %s" % current_variation)
                print("get_variation(astronaut): %s" % get_variation(astronaut))
                socketio.send("%s-%s" % (astronaut['key'], get_variation(astronaut)), broadcast=True)
                current_variation = get_variation(astronaut)
                current_key = astronaut['key']
            else:
                pass
            time.sleep(self.interval)

flag_poller = FlagPoller()

if __name__ == '__main__':
    socketio.run(app, debug=True) 