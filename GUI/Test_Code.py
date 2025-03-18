
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from Controller_Input import ControllerReader
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

controller = ControllerReader() #initiliaze instance of class
controller.connect() #connect controller

#Global Variables
motion_command_tuple = (0.0, 0.0, 0.0, 0.0, "None", 0.0)
tab_num = 1
row = 1
column = 0
font_size = 25

'''#Get controller inputs and print them to the terminal
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

    gui.after(10,update_controller_input)  #Reruns the function every 10 ms'''


#Will send a command to the rover
def send_to_rover():
    #Right Idea, but only one command per packet thing
    global motion_command_tuple
    command = None

    
    if motion_command_tuple[0] != 0:
        output_label.config(text=f"Current Command - Speed Test:\nVelocity: {motion_command_tuple[0]} cm/s\nTime: {motion_command_tuple[1]} s")
        command = f'V{round(motion_command_tuple[0])};{round(motion_command_tuple[1])}'
    elif motion_command_tuple[2] != 0:
        output_label.config(text=f"Current Command - Distance Test: Test:\nPosition: {motion_command_tuple[2]} m\nVelocity: {motion_command_tuple[3]} cm/s")
        command = f'P{motion_command_tuple[2]};{motion_command_tuple[3]}'
    elif motion_command_tuple[4] == 'Left':
        output_label.config(text=f"Current Command - Turning Test:\nDirection: {motion_command_tuple[4]}\nTurning Radius: {motion_command_tuple[5]} m")
        command = f'L{motion_command_tuple[5]}' #Need to determine how the turning will work (0-turn, velocity determined by radius?)
    elif motion_command_tuple[4] == 'Right':
        output_label.config(text=f"Current Command - Turning Test:\nDirection: {motion_command_tuple[4]}\nTurning Radius: {motion_command_tuple[5]} m")
        command = f'R{motion_command_tuple[5]}'
    print(command)



#This will get the inputs from the GUI and convert them into a tuple of floats
def get_input():
    global motion_command_tuple
    #Need to include error cases if no input is detected

    try:
        #Retrieve all input values and return 0 if one is not given
        speed_velocity = int(speed_velocity_input.get()) if speed_velocity_input.get() else 0   #Need to be updated with the new GUI layout
        speed_time = int(speed_time_input.get()) if speed_time_input.get() else 0 
        distance_position = int(distance_position_input.get()) if distance_position_input.get() else 0
        distance_velocity = int(distance_velocity_input.get()) if distance_velocity_input.get() else 0
        turning_direction = direction_select.get()
        turning_radius = int(radius_input.get()) if radius_input.get() else 0  
        
        #Prevent negative turning radius from being input
        if turning_radius < 0:
            output_label.config(text='Error: Negative turning radius not allowed')
            return
        
        if (speed_velocity != 0 and distance_position != 0) or (speed_velocity != 0 and distance_velocity != 0) or (speed_time != 0 and distance_position != 0) or (speed_time != 0 and distance_velocity != 0):
            output_label.config(text='Error: Only one command can be executed at a time')
            return
        
        if (speed_velocity != 0 and turning_direction != 'None') or (speed_velocity != 0 and turning_radius != 0) or (speed_time != 0 and turning_direction != 'None') or (speed_time != 0 and turning_radius != 0):
            output_label.config(text='Error: Only one command can be executed at a time')
            return
        
        if (distance_position != 0 and turning_direction != 'None') or (distance_position != 0 and turning_radius != 0) or (distance_velocity != 0 and turning_direction != 'None') or (distance_velocity != 0 and turning_radius != 0):
            output_label.config(text='Error: Only one command can be executed at a time')
            return

        motion_command_tuple = (speed_velocity,speed_time,distance_position,distance_velocity,turning_direction,turning_radius)

        send_to_rover()

    except ValueError:
        output_label.config(text='Error: please enter a valid integer value for all inputs')



#Will reset the tuple values to 0 and will immediatly be sent to rover
def stop():  #Need to add the send feature into this
    global motion_command_tuple

    motion_command_tuple = (0.0, 0.0, 0.0, 0.0, "None", 0.0)
    output_label.config(text=f"Current Command:\nVelocity: 0 cm/s\nPosition: 0 m\nTime: 0 s\nTurning Direction: None\nTurning Radius: 0 m")

    return motion_command_tuple


#This will create a drop down box of the input containing the input labels
def select_box(labels,gui):
    combo_box = ttk.Combobox(gui, values=labels, font=("Arial", font_size), width=15)
    combo_box.set(labels[0])
    
    return combo_box


#Print the tuple to the console to make sure its values are updating
def print_to_console():
    print(motion_command_tuple)


'''#Set tab state as normal(on) or disable(off)
def set_tab_state(tab, state):
    for widget in tab.winfo_children():
        try:
            widget.configure(state=state)
        except tk.TclError:
            pass #Some widgets (like labels) might not support state changes '''


'''#Detects if what tab the user is currently on and will return a value to disable all other tabs
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
        stop()'''


def create_plot(gui, title, x_label, y_label, xrange=None, yrange=None):
 
    fig, ax = plt.subplots(figsize=(9,9), dpi=100)  #Create the figure and axis

    #Axis titles and labels
    ax.set_title(title, fontsize=20)
    ax.set_xlabel(x_label, fontsize=15)
    ax.set_ylabel(y_label, fontsize=15)

    #Set x and y limits
    if xrange:
        ax.set_xlim(xrange)
    if yrange:
        ax.set_ylim(yrange)

    canvas = FigureCanvasTkAgg(fig, master=gui)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)

    return ax, canvas

        

#GUI
gui = tk.Tk()
gui.title("Super Advanced GUI")

speed_test_frame = tk.Frame(gui, bg="lightblue")
speed_test_frame.place(x=10, y=10)

distance_test_frame = tk.Frame(gui, bg="lightblue")
distance_test_frame.place(x=510, y=10)

turning_frame = tk.Frame(gui, bg="lightblue")
turning_frame.place(x=10, y=220)

current_command_frame = tk.Frame(gui, bg="lightblue")
current_command_frame.place(x=10, y=430)

send_inputs_frame = tk.Frame(gui, bg="lightblue")
send_inputs_frame.place(x=10, y=585)

black_line = tk.Canvas(gui, bg="black", height=10, width=1000, highlightthickness=0)
black_line.place(x=10, y=700)

pid_gains_frame = tk.Frame(gui, bg="lightblue")
pid_gains_frame.place(x=10, y=900)

PID_plot_frame = tk.Frame(gui, bg="lightblue")
PID_plot_frame.place(x=10, y=1200)

black_line_vertical = tk.Canvas(gui, bg="black", height=4000, width=10, highlightthickness=0)
black_line_vertical.place(x=1000, y=10)

position_data_frame = tk.Frame(gui, bg="lightblue")
position_data_frame.place(x=1100, y=10)

velocity_data_frame = tk.Frame(gui, bg="lightblue")
velocity_data_frame.place(x=2000, y=10)

accel_data_frame = tk.Frame(gui, bg="lightblue")
accel_data_frame.place(x=2900, y=10)

angle_data_frame = tk.Frame(gui, bg="lightblue")
angle_data_frame.place(x=1100, y=1010)

angular_vel_data_frame = tk.Frame(gui, bg="lightblue")
angular_vel_data_frame.place(x=2000, y=1010)


# Motion Commands Code

#Speed Test Frame Widgets
speed_velocity_label = tk.Label(speed_test_frame, text="Speed Test: ", font=("Arial", font_size, 'bold'))
speed_velocity_label.grid(row=row, column=column, pady = 10, padx=5, sticky='w')
speed_velocity_title = tk.Label(speed_test_frame, text="Velocity (cm/s): ", font=("Arial", font_size))
speed_velocity_title.grid(row=row+1, column=column, pady = 10, padx=5)
speed_velocity_input = tk.Entry(speed_test_frame, width = 12, font=("Arial", font_size))
speed_velocity_input.grid(row=row+1, column=column+1, pady = 10, padx=5)

speed_time_title = tk.Label(speed_test_frame, text="Time (s): ", font=("Arial", font_size))
speed_time_title.grid(row=row+2, column=column, pady = 10, padx=5)
speed_time_input = tk.Entry(speed_test_frame, width = 12, font=("Arial", font_size))
speed_time_input.grid(row=row+2, column=column+1, pady = 10, padx=5)

#Distance Test Frame Widgets
distance_position_label = tk.Label(distance_test_frame, text="Distance Test: ", font=("Arial", font_size, 'bold'))
distance_position_label.grid(row=row, column=column, pady = 10, padx=5, sticky='w')
distance_position_title = tk.Label(distance_test_frame, text="Position (m): ", font=("Arial", font_size))
distance_position_title.grid(row=row+1, column=column, pady = 10, padx=5)
distance_position_input = tk.Entry(distance_test_frame, width=12, font=("Arial", font_size))
distance_position_input.grid(row=row+1, column=column+1, pady = 10, padx=5)

distance_velocity_title = tk.Label(distance_test_frame, text="Velocity (cm/s): ", font=("Arial", font_size))
distance_velocity_title.grid(row=row+2, column=column, pady = 10, padx=5)
distance_velocity_input = tk.Entry(distance_test_frame, width = 12, font=("Arial", font_size))
distance_velocity_input.grid(row=row+2, column=column+1, pady = 10, padx=5)


#Turning Test Frame Widgets
turning_label = tk.Label(turning_frame, text="Turning Test:", font=("Arial", font_size, 'bold'))
turning_label.grid(row=row, column=column, pady=10, padx=5, sticky="w")

turning_direction = tk.Label(turning_frame, text="Turning Direction:", font=("Arial", font_size))
turning_direction.grid(row=row+1, column=column, pady=10, padx=5)

direction_select = select_box(['None', 'Left', 'Right'], turning_frame)
direction_select.grid(row=row+1, column=column+1, pady=10, padx=5)

turning_radius = tk.Label(turning_frame, text="Turning Radius (m):", font=("Arial", font_size))
turning_radius.grid(row=row+2, column=column, pady=10, padx=5, sticky="w")

radius_input = tk.Entry(turning_frame, width=15, font=("Arial", font_size))
radius_input.grid(row=row+2, column=column+1, pady = 10, padx=5)

#Send Commands Frame Widgets
go_button = tk.Button(send_inputs_frame, text="GO", width=23, command=get_input, font=("Arial", font_size))
go_button.grid(row=row, column=column, pady=10, padx=10)

stop_button = tk.Button(send_inputs_frame, text="STOP", width = 23, command=stop, font=("Arial", font_size))
stop_button.grid(row=row, column=column+1, pady=10, padx=10)

'''#Print Button to make sure the tuple is updating with each button press
print_button = tk.Button(send_inputs_frame, text="Print", width = 10, command=print_to_console, font=("Arial", font_size))
print_button.grid(row=row, column=column+2, pady=10)'''

#Output Label
output_label = tk.Label(current_command_frame, font=("Arial", font_size), text=f"Current Command: None")
output_label.grid(row=row, column=column, pady=10, padx=10)

# PID Tuning Code

#Gains
gains_label = tk.Label(pid_gains_frame, text="Gains:", font=("Arial", font_size))
gains_label.grid(row=row, column=column, pady=10)

#P
p_gain_label = tk.Label(pid_gains_frame, text="P:", font=("Arial", font_size))
p_gain_label.grid(row=row+1, column=column, pady=10, padx=10, sticky="w")
p_gain = tk.Entry(pid_gains_frame, width=10, font=("Arial", font_size))
p_gain.grid(row=row+1, column=column+1, pady = 10, padx=10)

#I
I_gain_label = tk.Label(pid_gains_frame, text="I:", font=("Arial", font_size))
I_gain_label.grid(row=row+2, column=column, pady=10, padx=10, sticky="w")
I_gain = tk.Entry(pid_gains_frame, width=10, font=("Arial", font_size))
I_gain.grid(row=row+2, column=column+1, pady = 10, padx=10)

#D
D_gain_label = tk.Label(pid_gains_frame, text="D:", font=("Arial", font_size))
D_gain_label.grid(row=row+3, column=column, pady=10, padx=10, sticky="w")
D_gain = tk.Entry(pid_gains_frame, width=10, font=("Arial", font_size))
D_gain.grid(row=row+3, column=column+1, pady = 10, padx=10)

#Create PID plot
# Im probably going to need ot change the y ranges to be a set amount above the set point
PID_plot, canvas = create_plot(PID_plot_frame, "PID tuning", "Time (s)", "Position (m)", xrange=(0,10), yrange=(0,100))

#Position Plot (Data will come from encoder)
position_vs_time_plot = create_plot(position_data_frame, "Position vs. Time", "Time (s)", "Position (m)", xrange=(0,10), yrange=(0,100))

#Velocity Plot (dp/dt)
velocity_vs_time_plot = create_plot(velocity_data_frame, "Velocity vs. Time", "Time (s)", "Velocity (cm/s)", xrange=(0,10), yrange=(0,100))

#Acceleration Plot (Data will come from IMU)
acceleration_vs_time_plot = create_plot(accel_data_frame, "Acceleration vs. Time", "Time (s)", "Acceleration (cm/s^2)", xrange=(0,10), yrange=(0,100))

#Angle Plot (Data will come from IMU)
angle_vs_time_plot = create_plot(angle_data_frame, "Angle vs. Time", "Time (s)", "Angle (rad)", xrange=(0,10), yrange=(0,100))

#Angular Velocity Plot (Data will come from IMU)
angular_velocity_vs_time_plot = create_plot(angular_vel_data_frame, "Angular Velocity vs. Time", "Time (s)", "Angular Velocity (rad/s)", xrange=(0,10), yrange=(0,100))


'''#Code for the GAME CONTROLLER TAB

#Also a print button for the game controller tab
print_button = tk.Button(game_controller_tab, text="Print", width = 10, command=print_to_console, font=("Arial", font_size))
print_button.grid(row=0, column=0, pady=10)


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
#LT_progressbar["minimum"] = -1

#Right Trigger Progress Bar
RT_progressbar = ttk.Progressbar(game_controller_tab, orient="vertical", length=400, mode="determinate")
RT_progressbar.grid(row=1, column=4, padx = 10)
RT_progressbar["maximum"] = 1
#RT_progressbar["minimum"] = -1

# Start the controller input loop
update_controller_input()'''


gui.mainloop()   #Run GUI until closed


'''What it does right now
-Saves new input values to the tuple each time a button is pressed
-Print button can be used to show that a new command was successfully save to the tuple

Once pygame is used in this code, we will need to import and use threading in to run 
the gui and controller code at the same time to prevent freezing

Need to make it switch the controller function off whenever the user is on the
testing tab'''