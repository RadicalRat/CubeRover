import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1' #hides welcome prompt
import pygame

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = '1' #allows events to be updated when window not in focus

class ControllerReader:
    def __init__(self): #initialize
        pygame.init() # initializes pygame class
        pygame.joystick.init() #initialize joystick class
        self.controller = None
        self.found_Message = False

        self.left_stick = [0.0,0.0]
        self.right_stick = [0.0,0.0]
        self.left_trigger = 0
        self.right_trigger = 0

    def _string_(self):
        return f"The {self.stick} is in position {self.pos}"

    def connect(self):
        if pygame.joystick.get_count() == 0:
            if not self.found_Message:
                print("No controller found... Waiting...")
                self.found_Message = True
            self.controller = None
            return
        
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                print("Controller Connected!")
                self.controller = pygame.joystick.Joystick(0) #only registers the first on connected
                self.controller.init()
            return

    def get_input(self): #read and returns controller input
        #assigning axis'
        if self.controller is None:
            return None
        
        #left_Xaxis, left_Yaxis, right_Xaxis, right_Yaxis, left_Trig, right_Trig = [self.controller.get_axis(i) for i in range (self.controller.get_numaxes())]
        pygame.event.pump() #update 
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                #assigning index and position propoerties
                axis = event.axis 
                pos = event.value

                if axis == 0:  #Left Stick X-axis
                    self.left_stick[0] = pos
                elif axis == 1:   #Left Stick Y-axis
                    self.left_stick[1] = pos
                elif axis == 2:   #Right Stick X-axis
                    self.right_stick[0] = pos
                elif axis == 3:   #Right Stick Y-axis
                    self.right_stick[1] = pos
                elif axis == 4:   #Left Trigger
                    self.left_trigger = pos
                elif axis == 5:   #Right Trigger
                    self.right_trigger = pos

            
            if event.type == pygame.JOYDEVICEREMOVED:
                print("Controller Disconnected...")
                self.controller = None
                self.left_stick = [0.0,0.0]
                self.right_stick = [0.0,0.0]
                self.left_trigger = 0
                self.right_trigger = 0
                return
            
        return{"left_stick": self.left_stick, "right_stick": self.right_stick, "left_trigger": self.left_trigger, "right_trigger": self.right_trigger}

    def close(self): #closes program
        pygame.quit()




    

    
