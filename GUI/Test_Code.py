
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from Controller_Input import ControllerReader
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



controller = ControllerReader() #initiliaze instance of class
controller.connect() #connect controller

#Global Variables
motion_command_tuple = (0.0, 0.0, 0.0, 0.0)
tab_num = 1

#Get controller inputs and print them to the terminal
def update_controller_input():
    input_data = controller.get_input()
    if input_data:
        leftx, lefty = input_data['left_stick']
        rightx, righty = input_data['right_stick']
        
        left_stick_plot.set_xdata([leftx])
        left_stick_plot.set_ydata([lefty])
        canvas_left.draw()

        right_stick_plot.set_xdata([rightx])
        right_stick_plot.set_ydata([righty])
        canvas_right.draw()

    gui.after(10,update_controller_input)  #Reruns the function every 100 ms


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


#Set tab state as normal(on) or disable(off)
def set_tab_state(tab, state):
    for widget in tab.winfo_children():
        try:
            widget.configure(state=state)
        except tk.TclError:
            pass #Some widgets (like labels) might not support state changes 


#Detects if what tab the user is currently on and will return a value to disable all other tabs
def detect_current_tab(event):
    global tab_num

    current_tab = event.widget.select()
    tab_text = event.widget.tab(current_tab, "text")
    
    if tab_text == "Testing":
        tab_num = 1
        set_tab_state(game_controller_tab, "disable")
        set_tab_state(testing_tab, "normal")
        print(tab_num)
        stop()
        
    elif tab_text == "Game Controller":
        tab_num = 2
        set_tab_state(game_controller_tab, "normal")
        set_tab_state(testing_tab, "disable")
        print(tab_num)
        stop()
        


#GUI
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
print_button.grid(row=0, column=0, pady=10)

'''controller_png = PhotoImage(file="xbox_controller.png")
image_label = tk.Label(game_controller_tab, image=controller_png)
image_label.grid(row=1,column=0)'''


# Make a plot for the left stick
fig_left, ax_left = plt.subplots()
ax_left.set_xlim(-1.2,1.2)
ax_left.set_ylim(1.2,-1.2)
ax_left.set_title("Left Stick Position")
left_stick_plot, = ax_left.plot([0],[0],'bo')  # Make Blue Dot
canvas_left = FigureCanvasTkAgg(fig_left, master=game_controller_tab)
canvas_left.get_tk_widget().grid(row=1, column=1)

#Make a plot for the right stick
fig_right, ax_right = plt.subplots()
ax_right.set_xlim(-1.2,1.2)
ax_right.set_ylim(1.2,-1.2)
ax_right.set_title("Right Stick Position")
right_stick_plot, = ax_right.plot([0],[0],'bo')  # Make Blue Dot
canvas_right = FigureCanvasTkAgg(fig_right, master=game_controller_tab)
canvas_right.get_tk_widget().grid(row=1, column=2)

# Start the controller input loop
update_controller_input()


gui.mainloop()   #Run GUI until closed


'''What it does right now
-Saves new input values to the tuple each time a button is pressed
-Print button can be used to show that a new command was successfully save to the tuple

Once pygame is used in this code, we will need to import and use threading in to run 
the gui and controller code at the same time to prevent freezing'''