from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import json
import gntp.notifier

growl = gntp.notifier.GrowlNotifier(
    applicationName = "Music Companion",
    notifications = ["Music Status"],
    defaultNotifications = ["Music Status"],
    # hostname = "computer.example.com", # Defaults to localhost
    # password = "abc123" # Defaults to a blank password
)
growl.register()

class Iphone(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        print "Client connected", self.factory.clients

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print "Client disconnected"

    def dataReceived(self, data):
        print data
        if (data.startswith ('[')):
            jsonData = json.loads(data)
            print jsonData
            songTitle = jsonData[0]['title'].encode('UTF-8')
            songArtist = jsonData[0]['artist'].encode('UTF-8')
            songAlbum = jsonData[0]['album'].encode('UTF-8')
            songDuration = jsonData[0]['duration']
            playingStatus = jsonData[1]['playBackState']
            print songArtist
            print songAlbum
            print songTitle
            print songDuration
            songInfo = songArtist + " - " + songAlbum

            if (playingStatus == "Pause"):
                playingTitle = songTitle
            elif (playingStatus == "Play"):
                playingTitle = songTitle + " (Paused)"

         # Send one message
            growl.notify(
                noteType = "Music Status",
                title = playingTitle,
                description = songInfo,
                icon = "none",
                sticky = False,
                priority = 1,
            )

factory = Factory()
factory.protocol = Iphone
factory.clients = []
reactor.listenTCP(8080, factory)
print "Server started"
reactor.run()
