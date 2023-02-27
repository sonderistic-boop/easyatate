import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))


import pygame as pg
from client.ui.button import *
from shared.themeColours import *
# set up a menu class, with a themeColours green background, and a join server, host server, settings, credits, and exit button


class Menu:
    def __init__(self,surface):
        
        
        self.surface = surface
        self.background = pg.transform.scale((pg.image.load("../shared/assets/background/background.png")),(120,120))
        self.logo = pg.image.load("../shared/assets/background/pyballlogo.png")
        self.backgroundX = []
        
       

        
        for i in range(-120,self.surface.get_width()+120,120):
            self.backgroundX.append(i)
        
        
        
        
        self.buttons = {}
        self.buttons["Join Game"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),300),(200,50),"Join Game","JoinGame")
        self.buttons["Host Game"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),400),(200,50),"Host Game","HostGame")
        self.buttons["Settings"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),500),(200,50),"Settings","Settings")             
        self.buttons["Exit"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),600),(200,50),"Exit","Exit")
    
    
    
    
        
    
    def eventHandler(self,info):
        for button in self.buttons:
            checker = self.buttons[button].eventHandler(info)
            if checker != None:
                return checker




    def renderSlidingBackground(self):
        for i in range(0,len(self.backgroundX)):
            if self.backgroundX[i] <= -120:
                self.backgroundX[i] = self.surface.get_width() + 120
            for j in range(0,(self.surface.get_height()+120),120):
                
                self.surface.blit(self.background,(self.backgroundX[i],j))
                
            self.backgroundX[i] -= 1


      
    def renderLogo(self):
        self.surface.blit(self.logo,(((self.surface.get_width()/2)-(self.logo.get_width()/2)),100))
        
    
    def renderButtons(self):
        for button in self.buttons:
            self.buttons[button].render()
        
        
    
    def render(self):
       self.renderSlidingBackground()
       self.renderLogo()
       self.renderButtons()


    def main(self,events):
        checker = self.eventHandler(events)
        if checker != None:
            return checker
        self.render()



class JoinGame(Menu):
    def __init__(self,surface):
        self.surface = surface
        self.background = pg.transform.scale((pg.image.load("../shared/assets/background/background.png")),(120,120))
        self.backgroundX = []
        
        for i in range(-120,self.surface.get_width()+120,120):
            self.backgroundX.append(i)
        
        self.buttons = {}
        self.buttons["Back"] = MenuButton(self.surface,(((150),150)),(200,50),"Back","Menu")
        self.buttons["Join"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),700),(200,50),"Join","Game")
        self.buttons["Username"] = InputButton(self.surface,(((self.surface.get_width()/2)-100),300),(200,50))
        self.buttons["IP"] = InputButton(self.surface,(((self.surface.get_width()/2)-100),400),(200,50))
        self.buttons["Port"] = InputButton(self.surface,(((self.surface.get_width()/2)-100),500),(200,50))


        self.texts = {
            "IP" : {
                    "text":"IP:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.buttons["IP"].position[0]-100,400),
                    "textSize" : 30
                    },

            "Port" : {
                    "text":"Port:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.buttons["Port"].position[0]-100,500),
                    "textSize" : 30
                    },
            
            "Username" : {
                    "text":"Username:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.buttons["Username"].position[0]-200,300),
                    "textSize" : 30
                    }

            }
        

    def renderTexts(self):
        for text in self.texts:
            font = pg.font.SysFont(self.texts[text]["font"],self.texts[text]["textSize"])
            rendertext = font.render(self.texts[text]["text"],1,self.texts[text]["textColour"])
            self.surface.blit(rendertext,(self.texts[text]["position"]))

    
    
        
    def eventHandler(self,info):
        for button in self.buttons:
            checker = self.buttons[button].eventHandler(info)
            if checker != None:
                return checker
            


    def renderSlidingBackground(self):
        for i in range(0,len(self.backgroundX)):
            if self.backgroundX[i] <= -120:
                self.backgroundX[i] = self.surface.get_width() + 120
            for j in range(0,(self.surface.get_height()+120),120):
                
                self.surface.blit(self.background,(self.backgroundX[i],j))
                
            self.backgroundX[i] -= 1


      
    def renderLogo(self):
        self.surface.blit(self.logo,(((self.surface.get_width()/2)-(self.logo.get_width()/2)),100))

    def renderButtons(self):
        for button in self.buttons:
            self.buttons[button].render()
    
    def render(self):
        self.renderSlidingBackground()
        s = pg.Surface((self.surface.get_width()-200,self.surface.get_height()-200))
        s.set_alpha(220)                
        s.fill((0,0,0))
        self.surface.blit(s,(100,100))
        self.renderTexts()

        self.renderButtons()

    def main(self,events):
        checker = self.eventHandler(events)
        if checker == "Game":
            clientSettings = {
                "username" : self.buttons["Username"].text,
                "ip" : self.buttons["IP"].text,
                "port" : self.buttons["Port"].text
            }
            return clientSettings, checker
        elif checker != None:
            return checker
        self.render()
    















class GameLobby(Menu):
    def __init__(self,surface,clientSettings):
        self.surface = surface
        self.background = pg.transform.scale((pg.image.load("../shared/assets/background/background.png")),(120,120))
        self.backgroundX = []
        self.clientSettings = clientSettings

        
        for i in range(-120,self.surface.get_width()+120,120):
            self.backgroundX.append(i)
        
        self.buttons = {}
        self.buttons["Start"] = MenuButton(self.surface,((self.surface.get_width()-350),800),(200,50),"Start","startGame")
        self.lists = {}
        self.lists["team1"] = ListButton(self.surface,((400,175)),(200,500),[])
        self.lists["team2"] = ListButton(self.surface,(((self.surface.get_width()-600),175)),(200,500),[])
        self.lists["neutral"] = ListButton(self.surface,(((self.surface.get_width()/2)-100),175),(200,500),[self.clientSettings["name"]])
        self.datatoSend = {}


        self.texts = {
            "team1" : {
                    "text":"Red Team:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (400,125),
                    "textSize" : 30
                    },
            "team2" : {
                    "text":"Blue Team:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()-600,125),
                    "textSize" : 30
                    },
            "neutral" : {
                    "text":"Neutral:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : ((self.surface.get_width()/2)-100,125),
                    "textSize" : 30
            }
        }   

    def renderSlidingBackground(self):

        for i in range(0,len(self.backgroundX)):
            if self.backgroundX[i] <= -120:
                self.backgroundX[i] = self.surface.get_width() + 120
            for j in range(0,(self.surface.get_height()+120),120):
                
                self.surface.blit(self.background,(self.backgroundX[i],j))
                
            self.backgroundX[i] -= 1
    
    def eventHandler(self,info):
        for button in self.buttons:
            checker = self.buttons[button].eventHandler(info)
            if checker == "startGame":
                self.datatoSend["transferMode"] = "game"
        for listButton in self.lists:
            checker = self.lists[listButton].eventHandler(info,self.lists)
            if checker != None:
                print(checker)
                return checker
        
            

    

    def renderTexts(self):
        for text in self.texts:
            font = pg.font.SysFont(self.texts[text]["font"],self.texts[text]["textSize"])
            rendertext = font.render(self.texts[text]["text"],1,self.texts[text]["textColour"])
            self.surface.blit(rendertext,(self.texts[text]["position"]))

    def renderButtons(self):
        for button in self.buttons:
            self.buttons[button].render()
        for listButton in self.lists:
            self.lists[listButton].render()


    def render(self):
        self.renderSlidingBackground()
        
        s = pg.Surface((self.surface.get_width()-200,self.surface.get_height()-200))
        s.set_alpha(220)                
        s.fill((0,0,0))
        self.surface.blit(s,(100,100))
        self.renderTexts()

        self.renderButtons()
    
    def updateLists(self,newLists):
        for listButton in self.lists:
            self.lists[listButton].updateItems(newLists[listButton])

    def getData(self):
        sendingData = {}
        # gets the team of the player who matches the username in the client settings
        for team in self.lists:
            for player in self.lists[team].list:
                if player == self.clientSettings["name"]:
                    sendingData["team"] = team
        
        if self.datatoSend != {}:
            for data in self.datatoSend:
                sendingData[data] = self.datatoSend[data]
            self.datatoSend = {}
        return sendingData

        

    def main(self,info,receivingData):
        #receivingData will contain a "players" key which contains a "team1", "team2" and "neutral" key
        
        self.updateLists(receivingData["players"])
        self.eventHandler(info)
        self.render()
        
