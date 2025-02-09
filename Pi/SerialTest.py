# Sample serial communication over a COM port
import serial
import time

port = "COM6" #COM Port for the Arduino Serial Communication

arduino = serial.Serial(port,115200 , timeout=1)
time.sleep(1)
print("Initialized")

userInput = "Happy"
while userInput != "q":
    userInput = input("Happy,Sad,Heart,q:")
    arduino.write(userInput.encode())
    time.sleep(0.1)
    #reading message
    print(arduino.readline().decode("ascii"))
