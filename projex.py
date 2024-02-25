import serial
import time

arduino_port = 'COM10'  # Change this to match your Arduino's serial port
arduino = serial.Serial(arduino_port, 9600, timeout=1)
time.sleep(2)  # Allow time for the Arduino to reset

while True:
    user_input = input("Enter 1 to turn the LED on, 0 to turn it off, or Q to quit: ")
    if user_input == '1':
        arduino.write(b'1')
        print("LED is ON")
    elif user_input == '0':
        arduino.write(b'0')
        print("LED is OFF")
    elif user_input == 'Q' or user_input == 'q':
        break

arduino.close()
