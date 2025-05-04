import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Network.TCP_Send import sendTCP
import time
import random
import queue

import csv

class CubeRoverGUI:

    def __init__(self):

        #Global Variables
        self.motion_command_tuple = (0.0, 0.0, 0.0, 0.0, "None", 0.0, 0.0, 0.0)
        self.PID_tuple = (None, None, None, None, None)
        self.command_line = queue.Queue()

        #Initialize GUI
        self.gui = tk.Tk()
        self.gui.title("CubeRover GUI")
        self.gui.geometry("3000x1800")

        #Creates the GUI when an object is initialized
        self.create_frames()
        self.create_widgets()
        self.create_separating_lines()


        #Initial Mode the rover will start with
        self.mode = 'T'

        #Initial Mode the PID will start in
        self.PID_mode = 'Pos'

        #Initialize what windows os
        self.os_mode = "W"

        #Initial Recording State
        self.record_state = "N"

        #Start plotting the random telemetry(this will need to be changed to only happen when a button is pressed)

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
        self.pid_send_frame.place(x=10, y=1050)

        self.PID_plot_frame = tk.Frame(self.gui, bg="lightblue")
        self.PID_plot_frame.place(x=10, y=1050)

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

        self.temperature_data_frame = tk.Frame(self.gui, bg="lightblue")
        self.temperature_data_frame.place(x=2875, y=1025)

        self.toggle_mode_button_frame = tk.Frame(self.gui, bg="lightblue")
        self.toggle_mode_button_frame.place(x=2850, y=2000)

        self.PID_toggle_button_frame = tk.Frame(self.gui, bg="lightblue")
        self.PID_toggle_button_frame.place(x=10, y=950)

        self.toggle_OS_button_frame = tk.Frame(self.gui, bg="lightblue")
        self.toggle_OS_button_frame.place(x=2850, y=2100)

        self.export_button_frame = tk.Frame(self.gui, bg="lightblue")
        self.export_button_frame.place(x=1025, y=2000)

        self.recording_button_frame = tk.Frame(self.gui, bg="lightblue")
        self.recording_button_frame.place(x=1025, y=2100)

    def create_separating_lines(self):
        #Adds the lines that separates each section in the GUI
        self.black_line_horizontal_1 = tk.Canvas(self.gui, bg="black", height=10, width=1000, highlightthickness=0)
        self.black_line_horizontal_1.place(x=10, y=700)

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

        self.radius_input = tk.Entry(self.turning_frame, width=10, font=("Arial", font_size))
        self.radius_input.grid(row=row+2, column=column+1, pady = 10, padx=5)

        self.turning_angle = tk.Label(self.turning_frame, text="Angle (deg):", font=("Arial", font_size))
        self.turning_angle.grid(row=row+1, column=column+2, pady=10, padx=5, sticky="w")

        self.angle_input = tk.Entry(self.turning_frame, width=10, font=("Arial", font_size))
        self.angle_input.grid(row=row+1, column=column+3, pady = 10, padx=5)

        self.turning_velocity = tk.Label(self.turning_frame, text="Velocity (cm/s):", font=("Arial", font_size))
        self.turning_velocity.grid(row=row+2, column=column+2, pady=10, padx=5, sticky="w")

        self.turning_velocity_input = tk.Entry(self.turning_frame, width=10, font=("Arial", font_size))
        self.turning_velocity_input.grid(row=row+2, column=column+3, pady = 10, padx=5)

        #Send Commands Frame Widgets
        self.go_button = tk.Button(self.send_inputs_frame, text="GO", width=23, command=self.get_input, font=("Arial", font_size))
        self.go_button.grid(row=row, column=column, pady=10, padx=10)

        self.stop_button = tk.Button(self.send_inputs_frame, text="STOP", width = 23, command=self.stop, font=("Arial", font_size))
        self.stop_button.grid(row=row, column=column+1, pady=10, padx=10)

        #Output Label
        self.output_label = tk.Label(self.current_command_frame, font=("Arial", font_size), text=f"Current Command: None")
        self.output_label.grid(row=row, column=column, pady=10, padx=10)

        # PID Tuning Code
        #Position Gains
        self.position_gains_label = tk.Label(self.pid_gains_frame, text="Position:", font=("Arial", font_size))
        self.position_gains_label.grid(row=row, column=column, pady=10, padx=10)

        #Pos P
        self.position_p_gain_label = tk.Label(self.pid_gains_frame, text="P:", font=("Arial", font_size))
        self.position_p_gain_label.grid(row=row, column=column+1, pady=10, padx=5)
        self.position_p_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.position_p_gain.grid(row=row, column=column+2, pady = 10, padx=5)

        #Pos I
        self.position_I_gain_label = tk.Label(self.pid_gains_frame, text="I:", font=("Arial", font_size))
        self.position_I_gain_label.grid(row=row, column=column+3, pady=10, padx=5)
        self.position_I_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.position_I_gain.grid(row=row, column=column+4, pady = 10, padx=5)

        #Pos D
        self.position_D_gain_label = tk.Label(self.pid_gains_frame, text="D:", font=("Arial", font_size))
        self.position_D_gain_label.grid(row=row, column=column+5, pady=10, padx=5)
        self.position_D_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.position_D_gain.grid(row=row, column=column+6, pady = 10, padx=5)

        #Velocity Gains
        self.velocity_gains_label = tk.Label(self.pid_gains_frame, text="Velocity:", font=("Arial", font_size))
        self.velocity_gains_label.grid(row=row+1, column=column, pady=10, padx=10)

        #Vel P
        self.velocity_p_gain_label = tk.Label(self.pid_gains_frame, text="P:", font=("Arial", font_size))
        self.velocity_p_gain_label.grid(row=row+1, column=column+1, pady=10, padx=5)
        self.velocity_p_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.velocity_p_gain.grid(row=row+1, column=column+2, pady = 10, padx=5)

        #Vel I
        self.velocity_I_gain_label = tk.Label(self.pid_gains_frame, text="I:", font=("Arial", font_size))
        self.velocity_I_gain_label.grid(row=row+1, column=column+3, pady=10, padx=5)
        self.velocity_I_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.velocity_I_gain.grid(row=row+1, column=column+4, pady = 10, padx=5)

        #Vel D
        self.velocity_D_gain_label = tk.Label(self.pid_gains_frame, text="D:", font=("Arial", font_size))
        self.velocity_D_gain_label.grid(row=row+1, column=column+5, pady=10, padx=5)
        self.velocity_D_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.velocity_D_gain.grid(row=row+1, column=column+6, pady = 10, padx=5)

        #Turning Gains
        self.turning_gains_label = tk.Label(self.pid_gains_frame, text="Turning:", font=("Arial", font_size))
        self.turning_gains_label.grid(row=row+2, column=column, pady=10, padx=10)

        #Turn P
        self.turning_p_gain_label = tk.Label(self.pid_gains_frame, text="P:", font=("Arial", font_size))
        self.turning_p_gain_label.grid(row=row+2, column=column+1, pady=10, padx=5)
        self.turning_p_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.turning_p_gain.grid(row=row+2, column=column+2, pady = 10, padx=5)

        #Turn I
        self.turning_I_gain_label = tk.Label(self.pid_gains_frame, text="I:", font=("Arial", font_size))
        self.turning_I_gain_label.grid(row=row+2, column=column+3, pady=10, padx=5)
        self.turning_I_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.turning_I_gain.grid(row=row+2, column=column+4, pady = 10, padx=5)

        #Turn D
        self.turning_D_gain_label = tk.Label(self.pid_gains_frame, text="D:", font=("Arial", font_size))
        self.turning_D_gain_label.grid(row=row+2, column=column+5, pady=10, padx=5)
        self.turning_D_gain = tk.Entry(self.pid_gains_frame, width=12, font=("Arial", font_size))
        self.turning_D_gain.grid(row=row+2, column=column+6, pady = 10, padx=5)

        #Send PID gains input
        self.send_gains_button = tk.Button(self.pid_send_frame, text="SEND", width = 48, command=self.get_input, font=("Arial", font_size))
        self.send_gains_button.grid(row=row, column=column, pady=10, padx=10)

        #PID mode toggle button
        self.PID_toggle_button = tk.Button(self.PID_toggle_button_frame, text="SWITCH PID MODE - CURRENT: POSITION", width = 48, command=self.toggle_PID_mode, font=("Arial", font_size))
        self.PID_toggle_button.grid(row=row, column=column, pady=10, padx=10)

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

        #Temperature Plot
        self.temperature_vs_time_plot, self.temperature_canvas = self.create_plot(self.temperature_data_frame, "Temperature vs. Time", "Time (s)", "Temperature (F)", xrange=(0,10), yrange=(0,100))

        #Toggle Mode Button
        self.toggle_mode_button = tk.Button(self.toggle_mode_button_frame, text="SWITCH MODE - CURRENT: TESTING", width = 48, command=self.toggle_mode, font=("Arial", font_size))
        self.toggle_mode_button.grid(row=row, column=column, pady=10, padx=10)

        #OS Toggle Button
        self.toggle_os_button = tk.Button(self.toggle_OS_button_frame, text="SWITCH OS - CURRENT: WINDOWS", width = 48, command=self.toggle_OS, font=("Arial", font_size))
        self.toggle_os_button.grid(row=row, column=column, pady=10, padx=10)

        #Export Button
        self.export_button = tk.Button(self.export_button_frame, text="EXPORT DATA (.csv)", width = 48, command=self.export_to_csv, font=("Arial", font_size))
        self.export_button.grid(row=row, column=column, pady=10, padx=10)
        
        #Recording Button
        self.recording_button = tk.Button(self.recording_button_frame, text="START RECORDING", width = 48, command=self.toggle_record_state, font=("Arial", font_size))
        self.recording_button.grid(row=row, column=column, pady=10, padx=10)


    #Will send a command to the rover
    def send_command(self):
        command = None
        #Setting all the excess packet spaces to 0
        if self.motion_command_tuple[0] != 0:
            self.output_label.config(text=f"Current Command - Speed Test:\nVelocity: {self.motion_command_tuple[0]} cm/s\nTime: {self.motion_command_tuple[1]} s")
            command = (self.mode, 0, 0, self.motion_command_tuple[0], 0, self.motion_command_tuple[1])
            print(f"Sending speed test command: {command}")
        elif self.motion_command_tuple[2] != 0:
            self.output_label.config(text=f"Current Command - Distance Test: Test:\nPosition: {self.motion_command_tuple[2]} m\nVelocity: {self.motion_command_tuple[3]} cm/s")
            command = (self.mode, self.motion_command_tuple[2], 0, self.motion_command_tuple[3], 0.0, 0.0)
            print(f"Sending distance test command: {command}")
        elif self.motion_command_tuple[4] == 'Left':
            angle = self.motion_command_tuple[5]
            self.output_label.config(text=f"Current Command - Turning Test:\nDirection: {self.motion_command_tuple[4]}\nTurning Radius: {self.motion_command_tuple[5]} m")
            command = (self.mode, 0, -1*self.motion_command_tuple[6], self.motion_command_tuple[7], angle, 0)
            print(f"Sending left turn command: {command}")
        elif self.motion_command_tuple[4] == 'Right':
            self.output_label.config(text=f"Current Command - Turning Test:\nDirection: {self.motion_command_tuple[4]}\nTurning Radius: {self.motion_command_tuple[5]} m")
            command = (self.mode, 0, self.motion_command_tuple[6], self.motion_command_tuple[7], self.motion_command_tuple[5], 0.0)
            print(f"Sending right turn command: {command}")
        
        if command:
            print(f"Final command being sent: {command}")
            self.command_line.put(command)

        if None not in self.PID_tuple:
            print(f'PID command: {self.PID_tuple}')
            self.command_line.put(self.PID_tuple)
        

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
            turning_angle = float(self.angle_input.get()) if self.angle_input.get() else 0
            turning_velocity = float(self.turning_velocity_input.get()) if self.turning_velocity_input.get() else 0
            
            #Error Handling
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
            
            if (turning_direction != 'None' and (turning_radius == 0 or turning_angle == 0 or turning_velocity == 0)):
                self.output_label.config(text='Error: Please enter a valid turning command')
                return
            
            if (turning_radius != 0 and (turning_direction == 'None' or turning_angle == 0 or turning_velocity == 0)):
                self.output_label.config(text='Error: Please enter a valid turning command')
                return

            if (turning_angle != 0 and (turning_direction == 'None' or turning_radius == 0 or turning_velocity == 0)):
                self.output_label.config(text='Error: Please enter a valid turning command')
                return

            if (turning_velocity != 0 and (turning_direction == 'None' or turning_angle == 0 or turning_radius == 0)):
                self.output_label.config(text='Error: Please enter a valid turning command')
                return

            self.motion_command_tuple = (speed_velocity,speed_time,distance_position,distance_velocity,turning_direction,turning_angle,turning_radius,turning_velocity)

            position_P_input = float(self.position_p_gain.get()) if self.position_p_gain.get() else None
            position_I_input = float(self.position_I_gain.get()) if self.position_I_gain.get() else None
            position_D_input = float(self.position_D_gain.get()) if self.position_D_gain.get() else None
            velocity_P_input = float(self.velocity_p_gain.get()) if self.velocity_p_gain.get() else None
            velocity_I_input = float(self.velocity_I_gain.get()) if self.velocity_I_gain.get() else None
            velocity_D_input = float(self.velocity_D_gain.get()) if self.velocity_D_gain.get() else None
            turning_P_input = float(self.turning_p_gain.get()) if self.turning_p_gain.get() else None
            turning_I_input = float(self.turning_I_gain.get()) if self.turning_I_gain.get() else None
            turning_D_input = float(self.turning_D_gain.get()) if self.turning_D_gain.get() else None

            if self.PID_mode == 'Pos':
                self.PID_tuple = ('T', position_P_input, position_I_input, position_D_input, 1, 1)
            elif self.PID_mode == 'Vel':
                self.PID_tuple = ('T', 1, velocity_P_input, velocity_I_input, velocity_D_input, 1)
            elif self.PID_mode == 'Turn':
                self.PID_tuple = ('T', 1, 1, turning_P_input, turning_I_input, turning_D_input)

            self.send_command()

        except ValueError:
            self.output_label.config(text='Error: please enter a valid integer value for all inputs')


    def stop(self):
        #Resets all commands to 0 and sends to the rover
        self.motion_command_tuple = ('T', 0.0, 0.0, 0.0, 0.0, 0.0)
        self.output_label.config(text=f"Current Command:\nVelocity: 0 cm/s\nPosition: 0 m\nTime: 0 s\nTurning Direction: None\nTurning Radius: 0 m")

        print(self.motion_command_tuple)

    def create_plot(self, gui, title, x_label, y_label, xrange=None, yrange=None):
    
        fig, ax = plt.subplots(figsize=(9,9), dpi=100)  #Create the figure and axis
        ax.grid(True)

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

    def update_plots(self, ax, canvas, time_data, y_data, title="", x_label="", y_label=""):
        ax.cla()

        ax.grid(True)
        ax.set_title(title, fontsize=20)
        ax.set_xlabel(x_label, fontsize=15)
        ax.set_ylabel(y_label, fontsize=15)

        ax.plot(time_data, y_data, marker='o')

        ax.relim()
        ax.autoscale_view()

        canvas.draw()

    def plot_data(self):
        #Plots and handles the feedback data

        if self.gui.winfo_exists():
            current_time = time.time()

            self.position_data.append(random.uniform(0,100))
            self.velocity_data.append(random.uniform(0,100))
            self.acceleration_data.append(random.uniform(0,100))
            self.angle_data.append(random.uniform(0,3.14))
            self.angular_velocity_data.append(random.uniform(0,100))
            self.temperature_data.append(random.uniform(0,100))
            self.time_data.append(current_time)

            self.position_data_export.append(random.uniform(0,100))
            self.velocity_data_export.append(random.uniform(0,100))
            self.acceleration_data_export.append(random.uniform(0,100))
            self.angle_data_export.append(random.uniform(0,3.14))
            self.angular_velocity_data_export.append(random.uniform(0,100))
            self.temperature_data_export.append(random.uniform(0,100))
            self.time_data_export.append(current_time)

                
            if len(self.time_data) > 20:
                self.position_data.pop(0)
                self.velocity_data.pop(0)
                self.acceleration_data.pop(0)
                self.angle_data.pop(0)
                self.angular_velocity_data.pop(0)
                self.temperature_data.pop(0)
                self.time_data.pop(0)

            self.update_plots(self.position_vs_time_plot, self.position_canvas, self.time_data, self.position_data, "Position vs. Time", 'Time (s)', 'Position (m)')
            self.update_plots(self.velocity_vs_time_plot, self.velocity_canvas, self.time_data, self.velocity_data, 'Velocity vs. Time', 'Time (s)', 'Velocity (cm/s)')
            self.update_plots(self.acceleration_vs_time_plot, self.acceleration_canvas, self.time_data, self.acceleration_data, 'Acceleration vs. Time', 'Time', 'Acceleration (cm/s^2)')
            self.update_plots(self.angle_vs_time_plot, self.angle_canvas, self.time_data, self.angle_data, "Angle vs. Time", 'Time (s)', 'Angle (rad)')
            self.update_plots(self.angular_velocity_vs_time_plot, self.angular_velocity_canvas, self.time_data, self.angular_velocity_data, "Angular Velocity vs. Time", 'Time (s)', 'Angular Velocity (rad/s)')
            self.update_plots(self.temperature_vs_time_plot, self.temperature_canvas, self.time_data, self.temperature_data, "Temperature vs. Time", 'Time (s)', 'Temperature (F)')

        if self.gui.winfo_exists():
            self.schedule = self.gui.after(1, self.plot_data)


    '''def toggle_PID_plot(self):
        #This will update the PID plot if the toggle button is pressed
        if self.PID_mode == 'Pos':
            y_data = self.position_data
            y_label = 'Position (m)'
            title = 'Position'

        elif self.PID_mode == 'Vel':
            y_data = self.velocity_data
            y_label = "Velocity (m/s)"
            title = 'Velocity'
        
        self.PID_plot.clear()
        self.PID_plot.set_title(f'{title} PID Tuning')
        self.PID_plot.set_xlabel('Time (s)')
        self.PID_plot.set_ylabel(y_label)

        self.PID_plot.plot(self.time_data, y_data)
        self.PID_canvas.draw'''


    def select_box(self, labels, gui):
        combo_box = ttk.Combobox(gui, values=labels, font=("Arial", 25), width=7)
        combo_box.set(labels[0])
    
        return combo_box
    
    #TOggle between controller and testing mode
    def toggle_mode(self):
        if self.mode == 'T':
            self.mode = 'C'
            self.toggle_mode_button.config(text='SWITCH MODE - CURRENT: CONTROLLER')
        elif self.mode == 'C':
            self.mode = 'T'
            self.toggle_mode_button.config(text='SWITCH MODE - CURRENT: TESTING')

    #Toggle between Windows and Linux OS
    def toggle_OS(self):
        if self.os_mode == "W":
            self.os_mode = "L"
            self.toggle_os_button.config(text='SWITCH MODE - CURRENT: LINUX')
        elif self.os_mode == "L":
            self.os_mode = "W"
            self.toggle_os_button.config(text='SWITCH MODE - CURRENT: WINDOWS')

    #Toggle between position and velocity PID tuning
    def toggle_PID_mode(self):
        if self.PID_mode == 'Pos':
            self.PID_mode = 'Vel'
            self.PID_toggle_button.config(text='SWITCH PID MODE - CURRENT: VELOCITY')
        elif self.PID_mode == 'Vel':
            self.PID_mode = 'Turn'
            self.PID_toggle_button.config(text='SWITCH PID MODE - CURRENT: TURNING')
        elif self.PID_mode == 'Turn':
            self.PID_mode = 'Pos'
            self.PID_toggle_button.config(text='SWITCH PID MODE - CURRENT: POSITION')

        #self.toggle_PID_plot()  The plot is low priority rn

    def toggle_record_state(self):
        if self.record_state == "N":
            self.record_state = "D"
            self.recording_button.config(text='STOP RECORDING')
            #Insert all of the sent data here - empty arrays
            #These variables will store feedback data
            self.position_data = []
            self.velocity_data = []
            self.acceleration_data = []
            self.angle_data = []
            self.angular_velocity_data = []
            self.temperature_data = []
            self.time_data = []

            #Need to make sure that I save all of the data so it can be exported
            self.position_data_export = []
            self.velocity_data_export = []
            self.acceleration_data_export = []
            self.angle_data_export = []
            self.angular_velocity_data_export = []
            self.temperature_data_export = []
            self.time_data_export = []
            #I need this to say if we are recording, then I will begin appending data to the above array and the
            '''Cam is going to send stuff constantly and then ill need to manipulate the time 
            data so that it starts back at 0 when the record button is pressed'''
            self.schedule = self.gui.after(1, self.plot_data)
        elif self.record_state == "D":
            self.record_state = "N"
            self.recording_button.config(text='START RECORDING')
            self.gui.after_cancel(self.schedule)
            self.schedule = None


    #Update this when I get the full data packet
    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension = ".csv",
            filetypes = [("CSV files", ".csv")],
            title = "Save data as..."
        )

        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)

                writer.writerow(["Time","Position","Velocity","Acceleration","Angle","Angular Velocity","Temperature"])

                for i in range(len(self.time_data_export)):
                    writer.writerow([self.time_data_export[i],self.position_data_export[i],self.velocity_data_export[i],self.acceleration_data_export[i],self.angle_data_export[i],self.angular_velocity_data_export[i],self.temperature_data_export[i]])

    def run_GUI(self):
        #Run the main GUI loop
        self.gui.mainloop()




#This is how you run the GUI

'''def check_mode(gui):
    while True:
        print(f'[Thread] Current Mode: {gui.mode}')
        time.sleep(2)'''

if __name__ == "__main__":
    robit = CubeRoverGUI()



    robit.run_GUI()

#This stuff is for debugging
'''def check_mode(gui):
    while True:
        print(f'[Thread] Current Mode: {gui.mode}')
        print(f'[Thread] Current OS: {gui.os_mode}')
        time.sleep(2)
#Threading allows for the mode to be checked outside of the GUI loop
#For implementing include the check_mode function and the two following lines
mode_thread = threading.Thread(target=check_mode, args=(robit,), daemon=True)
mode_thread.start()'''


'''TODO Change the data lists to numpy arrays because it will be a bit faster
Modify the create plot function to not clear everytime (I dont know why this makes it work but it does)
If the above step doesnt make it faster then I'll need to look into using the animation class in matplotlib

Add a button that allows the user save the data as a csv or excel file - DONE
all motor encoders - NOT DONE
all IMU data - NOT DONE
temp data - NOT DONE'''
