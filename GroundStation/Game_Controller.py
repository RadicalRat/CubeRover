import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick connected!")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick name:", joystick.get_name())
    print("Number of axes:", joystick.get_numaxes())

    # Example event loop:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                x_axis = joystick.get_axis(0)
                y_axis = joystick.get_axis(1)
                print("Axes:", x_axis, y_axis)
            if event.type == pygame.QUIT:
                running = False

pygame.quit()
