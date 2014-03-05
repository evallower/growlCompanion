from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import json
import gntp.notifier

growl = gntp.notifier.GrowlNotifier(
    applicationName = "Music Companion",
    notifications = ["New Updates","New Messages"],
    defaultNotifications = ["New Messages"],
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
            songTitle = jsonData[0]['title']
            songArtist = jsonData[0]['artist']
            songAlbum = jsonData[0]['album']
            songDuration = jsonData[0]['duration']
            playingStatus = jsonData[1]['playBackState']
            print songArtist
            print songAlbum
            print songTitle
            print songDuration
            songInfo = (songArtist, songTitle, songAlbum)
            songInfoDecoded = [x.encode('UTF-8') for x in songInfo]

            if (playingStatus == "Pause"):
                playingTitle = "Now Playing"
            elif (playingStatus == "Play"):
                playingTitle = "Paused"

         # Send one message
            growl.notify(
                noteType = "New Messages",
                title = playingTitle,
                description = songInfoDecoded,
                icon = "http://example.com/icon.png",
                sticky = False,
                priority = 1,
            )

factory = Factory()
factory.protocol = Iphone
factory.clients = []
reactor.listenTCP(8080, factory)
print "Server started"
reactor.run()
