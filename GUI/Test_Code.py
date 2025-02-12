
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage


motion_command_tuple = (0.0, 0.0, 0.0, 0.0)
tab_num = 1

#This will get the inputs from the GUI and convert them into a tuple of floats
def get_input():
    global motion_command_tuple

    velocity = float(velocity_input.get())  # Gets velocity as a string
    position = float(position_input.get())  # Gets position as a string
    time = float(time_input.get())   #Gets time as a string
    dist_ang_select = dist_or_ang.get()  #Gets distance method as a string


    #motion_command_tuple(velocity,distance,angle,time)
    #if the user enters a distance, then angle will be 0
    #if the user enters an angle, then distance will be 0
    if dist_ang_select == "Distance":
        output_label.config(text=f"Current Command:\nVelocity: {velocity} m/s\nPosition: {position} m\n Time: {time} s")
        motion_command_tuple = (velocity, position, 0, time)
    else:
        output_label.config(text=f"Current Command:\nVelocity: {velocity} m/s\nPosition: {position} rad\n Time: {time} s")
        motion_command_tuple = (velocity, 0, position, time)
    
    return motion_command_tuple


#Will reset the tuple values to 0 and will immediatly be sent to rover
def stop():
    global motion_command_tuple

    motion_command_tuple = (0.0, 0.0, 0.0, 0.0)
    output_label.config(text="Current Command:\nSTOP!!!!!")

    return motion_command_tuple

#Detects if what tab the user is currently on and will return a value to disable all other tabs
def detect_current_tab(event):
    global tab_num

    current_tab = event.widget.select()
    tab_text = event.widget.tab(current_tab, "text")
    
    if tab_text == "Testing":
        tab_num = 1
        print(tab_num)
    if tab_text == "Game Controller":
        tab_num = 2
        print(tab_num)



def send_to_rover():
    print("This does nothing right now")


#This will create a drop down box of the input containing the input labels
def select_box(labels,gui):
    combo_box = ttk.Combobox(gui, values=labels)
    combo_box.set(labels[0])
    
    return combo_box


#Print the tuple to the console to make sure its values are updating
def print_to_console():
    print(motion_command_tuple)



gui = tk.Tk()
gui.title("Super Advanced GUI")
tab_control = ttk.Notebook(gui)

testing_tab = tk.Frame(tab_control)
game_controller_tab = tk.Frame(tab_control)

tab_control.bind("<<NotebookTabChanged>>", detect_current_tab)

tab_control.add(testing_tab, text="Testing")
tab_control.add(game_controller_tab, text="Game Controller")

tab_control.pack(expand=1, fill="both")


#Code for the TESTING TAB

#Velocity Input
velocity_title = tk.Label(testing_tab, text="Velocity (m/s): ")
velocity_title.grid(row=1, column=0, pady = 10)
velocity_input = tk.Entry(testing_tab)
velocity_input.grid(row=1, column=1, pady = 10)

#Position Input
position_title = tk.Label(testing_tab, text="Position (m or rad): ")
position_title.grid(row=2, column=0, pady = 10)    #Place in GUI
position_input = tk.Entry(testing_tab)
position_input.grid(row=2, column=1, pady = 10)
dist_or_ang = select_box(['Distance', 'Angle'], testing_tab)
dist_or_ang.grid(row=2, column=2, pady=10)

#Time Input
time_title = tk.Label(testing_tab, text="Time (s): ")
time_title.grid(row=3, column=0, pady = 10)
time_input = tk.Entry(testing_tab)
time_input.grid(row=3, column=1, pady = 10)

#Button to send input values
enter_button = tk.Button(testing_tab, text="ENTER", width=10, command=get_input)
enter_button.grid(row=4, column=0, pady=10)

#Stop Button
stop_button = tk.Button(testing_tab, text="STOP", width = 10, command=stop)
stop_button.grid(row=4, column=1, pady=10)

#Print Button to make sure the tuple is updating with each button press
print_button = tk.Button(testing_tab, text="Print", width = 10, command=print_to_console)
print_button.grid(row=4, column=2, pady=10)

#Send button that will send the test inputs to the pi
send_button = tk.Button(testing_tab, text="Send", width = 10, command=send_to_rover)
send_button.grid(row=5, column=2, pady=10)

#Output Label
output_label = tk.Label(testing_tab, text="Current Command: None")
output_label.grid(row=5, column=1, pady=10)


#Code for the GAME CONTROLLER TAB

#Also a print button for the game controller tab
print_button = tk.Button(game_controller_tab, text="Print", width = 10, command=print_to_console)
print_button.grid(row=4, column=2, pady=10)

funny_label = tk.Label(game_controller_tab, text="Nothing to see here, will prob show the user what their inputs are\nWould be cool if we could show this on a digital controller")
funny_label.grid(row=0, column=0, pady=10)



gui.mainloop()   #Run GUI until closed

'''What it does right now
-Saves new input values to the tuple each time a button is pressed
-Print button can be used to show that a new command was successfully save to the tuple

What I need to still do
-Where does it go after I click the button
    -Needs I think it would be smart to have a seperate send button
     that allows the user to send the command to where ever it needs to go
-Make it look better
-Might need to make some error messages if an incorrect input is recieved
-Add some plots because thats cool'''