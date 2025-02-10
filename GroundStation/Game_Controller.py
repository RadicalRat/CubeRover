import sys
import os
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1' #hides welcome prompt
import pygame


os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = '1' #allows events to be updated when window not in focus
pygame.init() #initialize pygame class
pygame.joystick.init() #initialize joystick class

found_mess_printed = False #to keep track of if the no joystick message was printed once already
run = True

while run:
    time.sleep(.1)
    if pygame.joystick.get_count() == 0: #if joystick not connected
        found = False

        if not found_mess_printed:
            print("No joystick found... Waiting...")
            found_mess_printed = True

        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED: #if controlled connected
                print("Controller connected!")
                controller = pygame.joystick.Joystick(0) #only registers the first on connected
                controller.init() #initialize controller
                found = True

            elif event.type == pygame.JOYDEVICEREMOVED: #if controller uninitialized or removed
                print("Controller disconnected...")

            elif event.type == pygame.QUIT: #if program exited
                run = False
                pygame.quit()
                sys.exit
                break

            elif found:
                break

    else:
        found_mess_printed = False
        controller = pygame.joystick.Joystick(0)
        controller.init()
        #left_xaxis, left_yaxis, right_xaxis, right_yaxis, left_trig, right_trig = [controller.get_axis(i) for i in range(controller.get_numaxes())]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            elif event.type == pygame.JOYAXISMOTION:
                axis_index = event.axis
                val = event.value
                if axis_index == 2:
                    print(val)
                    time.sleep(.3)
                #print(f"axis: {axis_index}, pos: {val}")
  

pygame.quit()


