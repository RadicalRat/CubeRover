import tkinter as tk
from tkinter import ttk
#from Controller_Input import ControllerReader #(Might be useful later)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Network.TCP_Send import sendTCP
import time
import random

class CubeRoverGUI:

    def __init__(self):

        #Global Variables
        self.motion_command_tuple = (0.0, 0.0, 0.0, 0.0, "None", 0.0)
        self.PID_tuple = (0.0, 0.0, 0.0)

        #Initialize GUI
        self.gui = tk.Tk()
        self.gui.title("CubeRover GUI")

        #Creates the GUI when an object is initialized
        self.create_frames()
        self.create_widgets()
        self.create_separating_lines()

        #These variables will store feedback data
        self.position_data = []
        self.velocity_data = []
        self.acceleration_data = []
        self.angle_data = []
        self.angular_velocity_data = []
        self.time_data = []

        #Start plotting the random telemetry(this will need to be changed to only happen when a button is pressed)
        #threading.Thread(target=self.plot_data, daemon=True).start()
        self.gui.after(100, self.plot_data)

    def create_frames(self):
        #Creates all the frames used in the GUI
        self.speed_test_frame = tk.Frame(self.gui, bg="lightblue")
        self.speed_test_frame.place(x=10, y=10)

        self.distance_test_frame = tk.Frame(self.gui, bg="lightblue")
        self.distance_test_frame.place(x=510, y=10)

        self.turning_frame = tk.Frame(self.gui, bg="lightblue")
        self.turning_frame.place(x=10, y=220)

        self.current_command_frame = tk.Frame(self.gui, bg="lightblue")
        self.current_command_frame.place(x=10, y=430)

        self.send_inputs_frame = tk.Frame(self.gui, bg="lightblue")
        self.send_inputs_frame.place(x=10, y=585)

        self.pid_gains_frame = tk.Frame(self.gui, bg="lightblue")
        self.pid_gains_frame.place(x=10, y=740)

        self.pid_send_frame = tk.Frame(self.gui, bg="lightblue")
        self.pid_send_frame.place(x=10, y=900)

        self.PID_plot_frame = tk.Frame(self.gui, bg="lightblue")
        self.PID_plot_frame.place(x=10, y=1025)

        self.position_data_frame = tk.Frame(self.gui, bg="lightblue")
        self.position_data_frame.place(x=1025, y=10)

        self.velocity_data_frame = tk.Frame(self.gui, bg="lightblue")
        self.velocity_data_frame.place(x=1950, y=10)

        self.accel_data_frame = tk.Frame(self.gui, bg="lightblue")
        self.accel_data_frame.place(x=2875, y=10)

        self.angle_data_frame = tk.Frame(self.gui, bg="lightblue")
        self.angle_data_frame.place(x=1025, y=1025)

        self.angular_vel_data_frame = tk.Frame(self.gui, bg="lightblue")
        self.angular_vel_data_frame.place(x=1950, y=1025)

    def create_separating_lines(self):
        #Adds the lines that separates each section in the GUI
        self.black_line = tk.Canvas(self.gui, bg="black", height=10, width=1000, highlightthickness=0)
        self.black_line.place(x=10, y=700)

        self.black_line_vertical = tk.Canvas(self.gui, bg="black", height=4000, width=10, highlightthickness=0)
        self.black_line_vertical.place(x=1000, y=10)

    def create_widgets(self):
        #Creates all the widgets insides their respective frames
        font_size = 25
        row = 1
        column = 0

        #Speed Test Frame Widgets
        self.speed_velocity_label = tk.Label(self.speed_test_frame, text="Speed Test: ", font=("Arial", font_size, 'bold'))
        self.speed_velocity_label.grid(row=row, column=column, pady = 10, padx=5, sticky='w')
        
        self.speed_velocity_title = tk.Label(self.speed_test_frame, text="Velocity (cm/s): ", font=("Arial", font_size))
        self.speed_velocity_title.grid(row=row+1, column=column, pady = 10, padx=5)
        self.speed_velocity_input = tk.Entry(self.speed_test_frame, width = 12, font=("Arial", font_size))
        self.speed_velocity_input.grid(row=row+1, column=column+1, pady = 10, padx=5)

        self.speed_time_title = tk.Label(self.speed_test_frame, text="Time (s): ", font=("Arial", font_size))
        self.speed_time_title.grid(row=row+2, column=column, pady = 10, padx=5)
        self.speed_time_input = tk.Entry(self.speed_test_frame, width = 12, font=("Arial", font_size))
        self.speed_time_input.grid(row=row+2, column=column+1, pady = 10, padx=5)

        #Distance Test Frame Widgets
        self.distance_position_label = tk.Label(self.distance_test_frame, text="Distance Test: ", font=("Arial", font_size, 'bold'))
        self.distance_position_label.grid(row=row, column=column, pady = 10, padx=5, sticky='w')
        
        self.distance_position_title = tk.Label(self.distance_test_frame, text="Position (m): ", font=("Arial", font_size))
        self.distance_position_title.grid(row=row+1, column=column, pady = 10, padx=5)
        self.distance_position_input = tk.Entry(self.distance_test_frame, width=12, font=("Arial", font_size))
        self.distance_position_input.grid(row=row+1, column=column+1, pady = 10, padx=5)

        self.distance_velocity_title = tk.Label(self.distance_test_frame, text="Velocity (cm/s): ", font=("Arial", font_size))
        self.distance_velocity_title.grid(row=row+2, column=column, pady = 10, padx=5)
        self.distance_velocity_input = tk.Entry(self.distance_test_frame, width = 12, font=("Arial", font_size))
        self.distance_velocity_input.grid(row=row+2, column=column+1, pady = 10, padx=5)


        #Turning Test Frame Widgets
        self.turning_label = tk.Label(self.turning_frame, text="Turning Test:", font=("Arial", font_size, 'bold'))
        self.turning_label.grid(row=row, column=column, pady=10, padx=5, sticky="w")

        self.turning_direction = tk.Label(self.turning_frame, text="Turning Direction:", font=("Arial", font_size))
        self.turning_direction.grid(row=row+1, column=column, pady=10, padx=5)

        self.direction_select = self.select_box(['None', 'Left', 'Right'], self.turning_frame)
        self.direction_select.grid(row=row+1, column=column+1, pady=10, padx=5)

        self.turning_radius = tk.Label(self.turning_frame, text="Turning Radius (m):", font=("Arial", font_size))
        self.turning_radius.grid(row=row+2, column=column, pady=10, padx=5, sticky="w")

        self.radius_input = tk.Entry(self.turning_frame, width=15, font=("Arial", font_size))
        self.radius_input.grid(row=row+2, column=column+1, pady = 10, padx=5)

        #Send Commands Frame Widgets
        self.go_button = tk.Button(self.send_inputs_frame, text="GO", width=23, command=self.get_input, font=("Arial", font_size))
        self.go_button.grid(row=row, column=column, pady=10, padx=10)

        self.stop_button = tk.Button(self.send_inputs_frame, text="STOP", width = 23, command=self.stop, font=("Arial", font_size))
        self.stop_button.grid(row=row, column=column+1, pady=10, padx=10)

        #Output Label
        self.output_label = tk.Label(self.current_command_frame, font=("Arial", font_size), text=f"Current Command: None")
        self.output_label.grid(row=row, column=column, pady=10, padx=10)

        # PID Tuning Code
        #Gains
        self.gains_label = tk.Label(self.pid_gains_frame, text="Gains:", font=("Arial", font_size))
        self.gains_label.grid(row=row, column=column, pady=10, padx=10)

        #P
        self.p_gain_label = tk.Label(self.pid_gains_frame, text="P:", font=("Arial", font_size))
        self.p_gain_label.grid(row=row+1, column=column+1, pady=10, padx=5)
        self.p_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.p_gain.grid(row=row+1, column=column+2, pady = 10, padx=5)

        #I
        self.I_gain_label = tk.Label(self.pid_gains_frame, text="I:", font=("Arial", font_size))
        self.I_gain_label.grid(row=row+1, column=column+3, pady=10, padx=5)
        self.I_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.I_gain.grid(row=row+1, column=column+4, pady = 10, padx=5)

        #D
        self.D_gain_label = tk.Label(self.pid_gains_frame, text="D:", font=("Arial", font_size))
        self.D_gain_label.grid(row=row+1, column=column+5, pady=10, padx=5)
        self.D_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.D_gain.grid(row=row+1, column=column+6, pady = 10, padx=5)

        #Send PID gains input
        self.send_gains_button = tk.Button(self.pid_send_frame, text="SEND", width = 48, command=self.get_PID_input, font=("Arial", font_size))
        self.send_gains_button.grid(row=row, column=column, pady=10, padx=10)

        #PID plot
        self.PID_plot, self.PID_canvas = self.create_plot(self.PID_plot_frame, "PID tuning", "Time (s)", "Position (m)", xrange=(0,10), yrange=(0,100))

        #Position Plot (Data will come from encoder)
        self.position_vs_time_plot, self.position_canvas = self.create_plot(self.position_data_frame, "Position vs. Time", "Time (s)", "Position (m)", xrange=(0,10), yrange=(0,100))

        #Velocity Plot (dp/dt)
        self.velocity_vs_time_plot, self.velocity_canvas = self.create_plot(self.velocity_data_frame, "Velocity vs. Time", "Time (s)", "Velocity (cm/s)", xrange=(0,10), yrange=(0,100))

        #Acceleration Plot (Data will come from IMU)
        self.acceleration_vs_time_plot, self.acceleration_canvas = self.create_plot(self.accel_data_frame, "Acceleration vs. Time", "Time (s)", "Acceleration (cm/s^2)", xrange=(0,10), yrange=(0,100))

        #Angle Plot (Data will come from IMU)
        self.angle_vs_time_plot, self.angle_canvas = self.create_plot(self.angle_data_frame, "Angle vs. Time", "Time (s)", "Angle (rad)", xrange=(0,10), yrange=(0,100))

        #Angular Velocity Plot (Data will come from IMU)
        self.angular_velocity_vs_time_plot, self.angular_velocity_canvas = self.create_plot(self.angular_vel_data_frame, "Angular Velocity vs. Time", "Time (s)", "Angular Velocity (rad/s)", xrange=(0,10), yrange=(0,100))

    #Will send a command to the rover
    def send_to_rover(self):
        #Sends the user input to the rover
        command = None
        #Setting all the excess packet spaces to 0
        if self.motion_command_tuple[0] != 0:
            self.output_label.config(text=f"Current Command - Speed Test:\nVelocity: {self.motion_command_tuple[0]} cm/s\nTime: {self.motion_command_tuple[1]} s")
            command = ('V', self.motion_command_tuple[0], self.motion_command_tuple[1], 0.0, 0.0)
        elif self.motion_command_tuple[2] != 0:
            self.output_label.config(text=f"Current Command - Distance Test: Test:\nPosition: {self.motion_command_tuple[2]} m\nVelocity: {self.motion_command_tuple[3]} cm/s")
            command = ('P', self.motion_command_tuple[2], self.motion_command_tuple[3], 0.0, 0.0)
        elif self.motion_command_tuple[4] == 'Left':
            self.output_label.config(text=f"Current Command - Turning Test:\nDirection: {self.motion_command_tuple[4]}\nTurning Radius: {self.motion_command_tuple[5]} m")
            command = ('L', self.motion_command_tuple[5], 0.0, 0.0, 0.0)
        elif self.motion_command_tuple[4] == 'Right':
            self.output_label.config(text=f"Current Command - Turning Test:\nDirection: {self.motion_command_tuple[4]}\nTurning Radius: {self.motion_command_tuple[5]} m")
            command = ('R', self.motion_command_tuple[5], 0.0, 0.0, 0.0)
        
        print(command)
        '''tcp_client.send(command)'''  #This guy is under investigation rn


    def get_input(self):
        #Gets user input from the GUI, checks for errors, then calls the send to rover command
        try:
            #Retrieve all input values and return 0 if one is not given
            speed_velocity = float(self.speed_velocity_input.get()) if self.speed_velocity_input.get() else 0   #Need to be updated with the new GUI layout
            speed_time = float(self.speed_time_input.get()) if self.speed_time_input.get() else 0 
            distance_position = float(self.distance_position_input.get()) if self.distance_position_input.get() else 0
            distance_velocity = float(self.distance_velocity_input.get()) if self.distance_velocity_input.get() else 0
            turning_direction = self.direction_select.get()
            turning_radius = float(self.radius_input.get()) if self.radius_input.get() else 0
            
            #Prevent negative turning radius from being input
            if turning_radius < 0:
                self.output_label.config(text='Error: Negative turning radius not allowed')
                return
            
            if (speed_velocity != 0 and distance_position != 0) or (speed_velocity != 0 and distance_velocity != 0) or (speed_time != 0 and distance_position != 0) or (speed_time != 0 and distance_velocity != 0):
                self.output_label.config(text='Error: Only one command can be executed at a time')
                return
            
            if (speed_velocity != 0 and turning_direction != 'None') or (speed_velocity != 0 and turning_radius != 0) or (speed_time != 0 and turning_direction != 'None') or (speed_time != 0 and turning_radius != 0):
                self.output_label.config(text='Error: Only one command can be executed at a time')
                return
            
            if (distance_position != 0 and turning_direction != 'None') or (distance_position != 0 and turning_radius != 0) or (distance_velocity != 0 and turning_direction != 'None') or (distance_velocity != 0 and turning_radius != 0):
                self.output_label.config(text='Error: Only one command can be executed at a time')
                return
            
            if (speed_velocity != 0 and speed_time == 0):
                self.output_label.config(text='Error: Please enter a non-zero time value')
                return
            
            if (speed_velocity == 0 and speed_time != 0):
                self.output_label.config(text='Error: Please enter a non-zero velocity value')
                return
            
            if (distance_position != 0 and distance_velocity == 0):
                self.output_label.config(text='Error: Please enter a non-zero velocity value')
                return
            
            if (distance_position == 0 and distance_velocity != 0):
                self.output_label.config(text='Error: Please enter a non-zero position value')
                return
            
            if (turning_direction != 'None' and turning_radius == 0):
                self.output_label.config(text='Error: Please enter a non-zero turning radius value')
                return
            
            if (turning_direction == 'None' and turning_radius != 0):
                self.output_label.config(text='Error: Please provide a turning direction')
                return

            self.motion_command_tuple = (speed_velocity,speed_time,distance_position,distance_velocity,turning_direction,turning_radius)

            self.send_to_rover()

        except ValueError:
            self.output_label.config(text='Error: please enter a valid integer value for all inputs')

    def send_PID_input(self):
        #Send the PID gains to the rover

        gains = ('G', self.PID_tuple[0], self.PID_tuple[1], self.PID_tuple[2], 0.0)

        '''tcp_client.send(gains)''' #This guy is also under investigation

    def get_PID_input(self):
        #Gets the PID gains inputs from the GUI
        try:
            P_input = float(self.p_gain.get()) if self.p_gain.get() else 0
            I_input = float(self.I_gain.get()) if self.I_gain.get() else 0
            D_input = float(self.D_gain.get()) if self.D_gain.get() else 0

            self.PID_tuple = (P_input, I_input, D_input)

            self.send_PID_input()

        except ValueError:
            self.output_label.config(text='Error: please enter a valid integer value for all inputs') #Need to make an error label for the PID stuff


    def stop(self):
        #Resets all commands to 0 and sends to the rover
        self.motion_command_tuple = (0.0, 0.0, 0.0, 0.0, "None", 0.0)
        self.output_label.config(text=f"Current Command:\nVelocity: 0 cm/s\nPosition: 0 m\nTime: 0 s\nTurning Direction: None\nTurning Radius: 0 m")

        print(self.motion_command_tuple)

    def create_plot(self, gui, title, x_label, y_label, xrange=None, yrange=None):
    
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

    def update_plots(self, ax, canvas, time_data, y_data):
        #Updates the plots with the telemetry data
        ax.clear()
        ax.plot(time_data, y_data, marker='o')
        
        #Need to update the axis ranges so the line always remains on the plot
        '''ax.set_xlim(max(0, time_data[0] if time_data else 0), time_data[-1] if time_data else 10)
        ax.set_ylim(min(y_data) - 5 if y_data else 0, max(y_data) + 5 if y_data else 10)
'''
        canvas.draw()

    def plot_data(self):
        #Plots and handles the feedback data
        current_time = time.time()

        self.position_data.append(random.uniform(0,100))
        self.velocity_data.append(random.uniform(0,100))
        self.acceleration_data.append(random.uniform(0,100))
        self.angle_data.append(random.uniform(0,3.14))
        self.angular_velocity_data.append(random.uniform(0,100))
        self.time_data.append(current_time)

            
        if len(self.time_data) > 100:
            self.position_data.pop(0)
            self.velocity_data.pop(0)
            self.acceleration_data.pop(0)
            self.angle_data.pop(0)
            self.angular_velocity_data.pop(0)
            self.time_data.pop(0)

        self.update_plots(self.position_vs_time_plot, self.position_canvas, self.time_data, self.position_data)
        self.update_plots(self.velocity_vs_time_plot, self.velocity_canvas, self.time_data, self.velocity_data)
        self.update_plots(self.acceleration_vs_time_plot, self.acceleration_canvas, self.time_data, self.acceleration_data)
        self.update_plots(self.angle_vs_time_plot, self.angle_canvas, self.time_data, self.angle_data)
        self.update_plots(self.angular_velocity_vs_time_plot, self.angular_velocity_canvas, self.time_data, self.angular_velocity_data)

        self.gui.after(100, self.plot_data)

    def select_box(self, labels, gui):
        combo_box = ttk.Combobox(gui, values=labels, font=("Arial", 25), width=15)
        combo_box.set(labels[0])
    
        return combo_box

    def run_GUI(self):
        #Run the main GUI loop
        self.gui.mainloop()

robit = CubeRoverGUI()
robit.run_GUI()