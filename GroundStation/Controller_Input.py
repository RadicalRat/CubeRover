import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1' #hides welcome prompt
import pygame

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = '1' #allows events to be updated when window not in focuse

class ControllerReader:
    def __init__(self): #initialize
        pygame.init() # initializes pygame class
        pygame.joystick.init() #initialize joystick class
        self.controller = None
        self.found_Message = False


    def _string_(self):
        return f"The {self.stick} is in position {self.pos}"

    def connecct(self):
        if pygame.joystick.get_count() == 0:
            if not self.found_Message:
                print("No controller found... Waiting...")
                self.found_Message = True
        
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                print("Controller Connected!")
                self.controller = pygame.joystick.Joystick(0) #only registers the first on connected
                self.controller.init() #initialize controller
        return

    def get_input(self): #read and returns controller input
        #assigning axis'
        left_Xaxis, left_Yaxis, right_Xaxis, right_Yaxis, left_Trig, right_Trig = [self.controller.get_axis(i) for i in range (self.controller.get_numaxes())]
        pygame.event.pump() #update 
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                #assigning index and position propoerties
                axis = event.axis 
                pos = event.value
        return (axis, pos)

    def check_quit(self): #check to see if controller is disconnected
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEREMOVED: #if controller disconnected
                print("Controller Disconnected")
                self.controller = None

    def close(): #closes program
        pygame.quit()




    

    
