import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))





import socket
import pickle
from _thread import *
from network import get_ip
import gameMultiplayer.game as gameMultiplayer



class pyBallServer:
    
    def __init__(self):
        
        self.port = 5555
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIP = get_ip()
        self.transferMode = "lobby"
        self.gameBuffer = False
        #two transferModes, "lobby" and "game". While lobby is active, client will send team to server, and server will send back-
        #teams of all players, and gamesettings in a pickle dump object with two dictionaries
        #admin can change any clients team, this request will take precedent over any other.
        #when joining, client will send their name, and receive, their stuff
        
        self.gameSettings = {
            "stadium" : "smallStadium",
            "time" : 300,
            "maxScore": 3 
            
        }
            
        self.players = {
            "team1" : {},
            "team2" : {},
            "neutral" : {}


        }
       
        #player should have name,address,
      
        try:
            self.serverSocket.bind((self.serverIP, self.port))
        except socket.error as e:

            str("Error")





        print("Server IP:", self.serverIP)
        self.serverSocket.listen()
        print("Waiting for a connection, Server Started")

   


    def newClient(self,connection, address):
        
        player = connection.recv(4096)
        player = pickle.loads(player)
        
        
        self.players["neutral"][str(player)] = {"address": address}
        adminPrivilege = True
        data = {"team" : "neutral"}
        
        
        sendingData = {"gameSettings" : self.gameSettings,
                       "players" : self.players
                      }
        sendingDataLoad = pickle.dumps(sendingData)
        connection.send(sendingDataLoad)
        
        
        #while true, receive data, which includes team of player
        #send data load, containing the aforementioned player and gamesettings. When a change in the transferMode occurs,
        #start transferring in gamestyle synchronous transmission, containing gameState, score, time remaining, and positions of ball and player

        
        
        while True:
            
            
            match self.transferMode:
                
                case "lobby":
                    try:
                        #error occurs here, receivingData
                        receivingDataLoad = connection.recv(4096)
                        
                        receivingData = pickle.loads(receivingDataLoad)
                    
                        
                        

                    except Exception as e:
                        print(e)
                        break

                    if receivingData["team"] != data["team"]:
                        #change has occured in players selected team, rectify by deleting record of player in previous team and adding to new team
                        N = (self.players[(data["team"])][str(player)]).copy()
                        del self.players[(data["team"])][str(player)]
                        self.players[(receivingData["team"])][str(player)] = N

                    #additional checks, if player is an admin, if they made any changes to server

                    if adminPrivilege:
                        if "gameSettings" in receivingData:
                            if receivingData["gameSettings"] != self.gameSettings:
                                self.gameSettings = receivingData["gameSettings"]
                        
                        if "transferMode" in receivingData:
                            if receivingData["transferMode"] == "game":
                                self.transferMode = receivingData["transferMode"]
                                sendingData["transferMode"] = self.transferMode
                                self.game = gameMultiplayer.Game(self.players,self.gameSettings["time"],self.gameSettings["maxScore"],self.gameSettings["stadium"])
                                sendingData["gameData"] = self.game.getData()





                    data = receivingData.copy()

                    #new initial data
                    if self.transferMode != None:
                        sendingData["gameSettings"] = self.gameSettings
                        sendingData["players"] = self.players
                    sendingDataLoad = pickle.dumps(sendingData)
                    connection.send(sendingDataLoad)
                    #send data
                    
                    
                case "game":
                    #if game, then try and receuve
                    try:
                        receivingDataLoad = connection.recv(4096)
                        receivingData = pickle.loads(receivingDataLoad) 
                    except:
                        break

                    #receivingData should include direction the player moved in, the game will then update the position of the player depending on the direction
                    #moved, wait for the game buffer to be true and then send the gameState, score, time remaining, and positions of ball and player

                    if receivingData["direction"] != 0:
                        self.game.players[player].move(receivingData["direction"])
                    
                    

                    data = receivingDataLoad.copy()

                    sendingData = {"gameData" : self.game.getData(),
                                   "transferMode" : self.transferMode
                                     }
                    sendingDataLoad = pickle.dumps(sendingData)


                    connection.send(sendingDataLoad)
                        
 
        print("Lost connection")
        print("deleting", player)
        deletionSequence = [self.players[data["team"]][str(player)],
                            self.game.players[data["team"]][str(player)],
                            getattr(self.game, data["team"])[str(player)],
                            self.game.playerGroup[str(player)]
                            ]
        
        for command in deletionSequence:
            try:
                del command
            except:
                continue
        
        

        connection.close()


    def connectionChecker(self):
        
        connection, address = self.serverSocket.accept()
        print("connected to:", address)
        


        start_new_thread(self.newClient, (connection,address))


        
        
        
        
        
#main    
 
server = pyBallServer()
 
while True:
    server.gameBuffer = False
    if server.transferMode == "lobby":
        
        server.connectionChecker()
    
    if server.transferMode == "game":
        server.game.run()
        server.gameBuffer = True
                     
                                                 
                               
                     
                     
        
