#make game class, with a run method, and a main method
#game should be 810x770
#game will have a stadium, a ball, and two teams
#game will have a run method, which will run the game
#game 
import pygame as pg
import math
import sys


from gameClient.entities.pawn import Pawn
from gameClient.entities.ball import Ball
import gameClient.entities.stadium.stadiums as stadiums


class Game():
    def __init__(self,parentScreen,players,gameSettings):
        self.size = (1920,1080)
        #declares the parent screen, which is the screen that the game surface will be drawn on
        self.parentScreen = parentScreen
        #declares which stadium the game will be played on
        self.stadium = gameSettings["stadium"]

        #declares how long the game will last
        self.time = gameSettings["time"]
        #declares the maximum score the game will be played to
        self.maxScore = gameSettings["maxScore"]

        self.colours = {
            "team1" : "red",
            "team2" : "blue"
        }

        self.leftTeam = {}
        self.rightTeam = {}

        self.leftTeamScore = 0
        self.rightTeamScore = 0

        
        
        
        #load game surface, load players, load ball, load stadium
        

        self.screen = pg.Surface((self.size),pg.SRCALPHA)
        
        self.stadium = getattr(stadiums,stadium)
        self.stadium = self.stadium(self.screen,(100,100),[self.colours["team1"],self.colours["team2"]])
        
        
        self.ball = Ball(self.screen,(self.stadium.bounds["middle"][0],self.stadium.bounds["middle"][1]),(30,30))
        
        #load players, and add them to the left and right team dictionaries. initial position will be the middle-left of the stadium for the left team, and the middle-right of the stadium for the right team
        for i in players["team1"]:
            self.leftTeam[i] = Pawn(i,self.colours["team1"],False,self.screen,(400,400),(70.3,70.3))          
        
        for i in players["team2"]:
            self.rightTeam[i] = Pawn(i,self.colours["team2"],False,self.screen,(400,400),(70.3,70.3))   

        
        
        
        #add sprite groups for ball, players, stadium parts

        #self.ballGroup = pg.sprite.GroupSingle(self.ball)


        


       

        
           


    def render(self):
        #draw the stadium, draw the ball, draw the players
        self.stadium.render()
        for i in self.playerGroup:
            i.render()
        self.ball.render()
        
        
        self.parentScreen.blit(self.screen,(0,50))

    

    
    
    #main function, takes the receivingData as a parameter, and then renders the items based on this
    # another function as well, getData() which getData() returns the position of the isMe player.
    
    def main(self):
        #check for collisions, check for goals, check for time, check for score
        #update the ball, update the players
        #render the stadium, render the ball, render the players


        self.render()
        
    
        
        
     
        
     

    




        
        

        
    