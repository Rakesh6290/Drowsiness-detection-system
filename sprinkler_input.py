import serial

# Define the serial port and baud rate (adjust COM port as needed)
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the appropriate port

def turn_on_sprinkler():
    # Send a command to turn on the sprinkler
    ser.write(b'1')
    print("Sprinkler turned on")

def turn_off_sprinkler():
    # Send a command to turn off the sprinkler
    ser.write(b'0')
    print("Sprinkler turned off")

try:
    while True:
        choice = input("Enter 1 to turn on sprinkler, 0 to turn off, or 'q' to quit: ")
        if choice == '1':
            turn_on_sprinkler()
        elif choice == '0':
            turn_off_sprinkler()
        elif choice == 'q':
            break

except KeyboardInterrupt:
    print("Keyboard interrupt. Exiting...")

finally:
    # Close the serial connection
    ser.close()
