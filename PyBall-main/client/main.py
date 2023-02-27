import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))


import pygame as pg
import client.ui.screens as screens
from client.client import Client

# design a pygame window, and set the window title as pyBall
pg.init()
pg.display.set_caption("pyBall")
screen = pg.display.set_mode((1600, 1000),pg.SRCALPHA)

# set up the clock
clock = pg.time.Clock()
# set up the main function for the game

def main():
    running = True
    focus = "Menu"
    newFocus= "Menu"
    current = screens.Menu(screen)
    while running:
        clock.tick(60)
        if focus != newFocus:
            match newFocus:
                case newFocus if newFocus[1] == "Game":
                    #if not others, then must be containing gamesettings as well as the checker from joinGame
                    focus = newFocus[1]
                    
                    current = Client(screen,{"name" : newFocus[0]["username"],"team" : "neutral"},newFocus[0]["ip"],newFocus[0]["port"])
                    newFocus = newFocus[1]
                case newFocus if newFocus != "Exit" and isinstance(newFocus,str):
                    focus = newFocus
                    current = getattr(screens,newFocus)(screen)
                case "Exit":
                    running = False
                    pg.quit()
                    sys.exit()
                
            

        info = {
            "mouse" : pg.mouse.get_pos(),
            "events" : pg.event.get(),
            "focus" : focus
            }
        # set the maximum FPS
        
                      
        # get all the events
        for event in info["events"]:
            # if the event is to quit the game, then set running as False
            if event.type == pg.QUIT:
                running = False
        
        output = current.main(info)
        if output is not None:
            newFocus = output



        pg.display.flip()
            
        
        
        
        # if the focus is on the menu, then run the menu

main()

