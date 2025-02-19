
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
    if tab_num == 2:
        input_data = controller.get_input()
        if input_data:
            leftx, lefty = input_data['left_stick']
            rightx, righty = input_data['right_stick']
            left_trigger = input_data['left_trigger']
            right_trigger = input_data['right_trigger']
            
            left_stick_plot.set_xdata([leftx])
            left_stick_plot.set_ydata([lefty])
            canvas_left.draw()

            right_stick_plot.set_xdata([rightx])
            right_stick_plot.set_ydata([righty])
            canvas_right.draw()

            LT_progressbar["value"] = left_trigger
            RT_progressbar["value"] = right_trigger

            print(f"LX={leftx}, LY={lefty}, RX={rightx}, RY={righty}, LT={left_trigger}, RT={right_trigger}")

    gui.after(10,update_controller_input)  #Reruns the function every 10 ms


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
    combo_box = ttk.Combobox(gui, values=labels, font=("Arial", 25), width=15)
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

#Scale the size of the widgets
'''def change_widget_size(value):
    new_size = int(value)
    
    for tab in [testing_tab, game_controller_tab]:
        for widget in tab.winfo.children():
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, ttk.Progressbar)):
                widget.config(font=("Arial", new_size))
            if isinstance(widget, (tk.Button, tk.Entry, ttk.Progressbar)):
                widget.config(width=new_size, height=new_size)'''


        

#GUI
gui = tk.Tk()
gui.title("Super Advanced GUI")
style = ttk.Style()
style.configure('TNotebook.Tab', font=("Arial",25))
tab_control = ttk.Notebook(gui)

testing_tab = tk.Frame(tab_control)
game_controller_tab = tk.Frame(tab_control)

tab_control.bind("<<NotebookTabChanged>>", detect_current_tab)

tab_control.add(testing_tab, text="Testing")
tab_control.add(game_controller_tab, text="Game Controller")


tab_control.pack(expand=1, fill="both")

'''#Slider to allow user to change widget size
widget_size_Test = tk.Scale(testing_tab, from_=0.5, to=2, orient="horizontal", label="Adjust Widget Size", command=change_widget_size)
widget_size_Test.set(1.0)
widget_size_Test.grid(row=0, column=10)
widget_size_Controller = tk.Scale(game_controller_tab, from_=0.5, to=2, orient="horizontal", label="Adjust Widget Size", command=change_widget_size)
widget_size_Controller.set(1.0)
widget_size_Controller.grid(row=0, column=10)'''



#Code for the TESTING TAB

#Velocity Input
velocity_title = tk.Label(testing_tab, text="Velocity (m/s): ", font=("Arial", 25))
velocity_title.grid(row=1, column=0, pady = 10)
velocity_input = tk.Entry(testing_tab, width = 15, font=("Arial", 25))
velocity_input.grid(row=1, column=1, pady = 10)

#Position Input
position_title = tk.Label(testing_tab, text="Position (m or rad): ", font=("Arial", 25))
position_title.grid(row=2, column=0, pady = 10)    #Place in GUI
position_input = tk.Entry(testing_tab, width=15, font=("Arial", 25))
position_input.grid(row=2, column=1, pady = 10)
dist_or_ang = select_box(['Distance', 'Angle'], testing_tab)
dist_or_ang.grid(row=2, column=2, pady=10) 

#Time Input
time_title = tk.Label(testing_tab, text="Time (s): ", font=("Arial", 25))
time_title.grid(row=3, column=0, pady = 10)
time_input = tk.Entry(testing_tab, width=15, font=("Arial", 25))
time_input.grid(row=3, column=1, pady = 10)

#Button to send input values
enter_button = tk.Button(testing_tab, text="ENTER", width=10, command=get_input, font=("Arial", 25))
enter_button.grid(row=4, column=0, pady=10)

#Stop Button
stop_button = tk.Button(testing_tab, text="STOP", width = 10, command=stop, font=("Arial", 25))
stop_button.grid(row=4, column=1, pady=10)

#Print Button to make sure the tuple is updating with each button press
print_button = tk.Button(testing_tab, text="Print", width = 10, command=print_to_console, font=("Arial", 25))
print_button.grid(row=4, column=2, pady=10)

#Send button that will send the test inputs to the pi
send_button = tk.Button(testing_tab, text="Send", width = 10, command=send_to_rover, font=("Arial", 25))
send_button.grid(row=5, column=2, pady=10)

#Output Label
output_label = tk.Label(testing_tab, text="Current Command: None", font=("Arial,", 25))
output_label.grid(row=5, column=1, pady=10)


#Code for the GAME CONTROLLER TAB

#Also a print button for the game controller tab
print_button = tk.Button(game_controller_tab, text="Print", width = 10, command=print_to_console, font=("Arial", 25))
print_button.grid(row=0, column=0, pady=10)

'''controller_png = PhotoImage(file="xbox_controller.png")
image_label = tk.Label(game_controller_tab, image=controller_png)
image_label.grid(row=1,column=0)'''


# Make a plot for the left stick
fig_left, ax_left = plt.subplots(figsize=(10,10))
ax_left.set_xlim(-1.2,1.2)
ax_left.set_ylim(1.2,-1.2)
ax_left.set_title("Left Stick Position", fontsize=20)
left_stick_plot, = ax_left.plot([0],[0],'bo', markersize=20)  # Make Blue Dot
canvas_left = FigureCanvasTkAgg(fig_left, master=game_controller_tab)
canvas_left.get_tk_widget().grid(row=1, column=2)

#Make a plot for the right stick
fig_right, ax_right = plt.subplots(figsize=(10,10))
ax_right.set_xlim(-1.2,1.2)
ax_right.set_ylim(1.2,-1.2)
ax_right.set_title("Right Stick Position", fontsize=20)
right_stick_plot, = ax_right.plot([0],[0],'bo', markersize=20)  # Make Blue Dot
canvas_right = FigureCanvasTkAgg(fig_right, master=game_controller_tab)
canvas_right.get_tk_widget().grid(row=1, column=3)

#Left Trigger Progress Bar
LT_progressbar = ttk.Progressbar(game_controller_tab, orient="vertical", length=400, mode="determinate")
LT_progressbar.grid(row=1, column=1, padx = 10)
LT_progressbar["maximum"] = 1
LT_progressbar["minimum"] = -1

#Right Trigger Progress Bar
RT_progressbar = ttk.Progressbar(game_controller_tab, orient="vertical", length=400, mode="determinate")
RT_progressbar.grid(row=1, column=4, padx = 10)
RT_progressbar["maximum"] = 1
RT_progressbar["minimum"] = -1

# Start the controller input loop
update_controller_input()


gui.mainloop()   #Run GUI until closed


'''What it does right now
-Saves new input values to the tuple each time a button is pressed
-Print button can be used to show that a new command was successfully save to the tuple

Once pygame is used in this code, we will need to import and use threading in to run 
the gui and controller code at the same time to prevent freezing

Need to make it switch the controller function off whenever the user is on the
testing tab'''