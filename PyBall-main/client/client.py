import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))


import pygame as pg
import socket
import pickle

from server.network import Network
from client.ui.screens import GameLobby
from gameClient.game import Game

#pygame.font.init()

width = 700
height = 700
#win = pygame.display.set_mode((width, height))
#pygame.display.set_caption("pyBall-Client")




"""
sendingData = {
    "team" : userinfo["team"],

}
"""

class Client:
    def __init__(self,screen,userinfo,serverIp,port=5555):
        self.serverIp = serverIp
        self.port = port

        self.transferMode = "lobby"
        self.focus = "GameLobby"
        self.newFocus = "GameLobby"
        self.current = GameLobby(screen,userinfo)

        self.networkInterface = Network(self.serverIp,self.port,userinfo["name"])
        self.screen = screen
        self.userinfo = userinfo
        self.sendingData = { "team" : self.userinfo["team"] }
        self.receivingData = None

        
        
        

    #at the start, send username to the server, receive data in return, which will be used to edit lobby. When the server says that the game has started, start the game and start looping that
    #once the game has started, send the server the normalised direction the player wishes to move in, and receive the game data in return. This will then be used to draw the game
 
    def main(self,info):
        if self.focus != self.newFocus:
            match self.newFocus:
                case "GameLobby":
                    self.focus = self.newFocus
                    self.transferMode = "lobby"
                    self.current = GameLobby(self.screen,self.userinfo)
                case "Game":
                    self.focus = self.newFocus
                    self.transferMode = "game"
                    #FIX THIS LATER-------------------------------------------------------------------------------------------------------------------------------============
                    self.current = Game(self.screen,self.initialGameData["gameData"]["players"],self.initialGameSettings)


                
        match self.transferMode:
            case "lobby":
                self.sendingData = self.current.getData()
                #if lobby, send a dictionary with the team the player wishes to be on. This value changes when the player changes it in the lobby, if the player is the admin, they can change any players team
                print("sending data: ",self.sendingData)
                ReceivingDataLoad = self.networkInterface.sendData(self.sendingData)
                
                if "transferMode" in ReceivingDataLoad:
                    if ReceivingDataLoad["transferMode"] == "game":
                        self.newFocus = "Game"
                        self.initialGameSettings = ReceivingDataLoad["gameSettings"].copy()
                        return
                self.current.main(info,ReceivingDataLoad)

                


            case "game":
                #data transfer shenanigans
                self.game()

            
            

#newclient = Client("localhost","damn","sonderistic")
#while True:
#    newclient.main()
