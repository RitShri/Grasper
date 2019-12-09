
import serial
import time

# Setup
BAUD = 9600 # Baud Rate
ser = serial.Serial('/dev/tty.usbmodem14101') # Found with 'ls /dev/tty.*'
print("Serial Port is open: {}".format(ser.is_open))
print("Baud Rate: {}".format(BAUD))
# Serial pins for communication: 0(RX), 1(TX)

def rock():
    """
    Activate servos that form Rock hand.
    """

def paper():
    """
    Activate respective seros [list them here] to form paper hand.
    """

def scissor():
    """
    Activate respecftive servos [list them here] to form the scissor hand.
    """

def grasp():
    """
    """


def game_on():
    "Ask, wait, write"
    while True:
        u_input = input("\n Choose your hand [Rock, Paper, Scissors]: ")
        if u_input in ["Rock", "rock", "R", "r"]:
            print("LED is on...")
            time.sleep(0.1) 
            ser.write(b'R') 
        elif u_input in ["Paper", "paper", "P", "p"]:
            print("LED is off...")
            time.sleep(0.1)
            ser.write(b'P')
        elif u_input in ["Scissors", "scissors", "S", "s"]:
            print("LED is off...")
            time.sleep(0.1)
            ser.write(b'P')
        elif u_input in ["quit", "q"]:
            print("Program Exiting")
            time.sleep(0.1)
            ser.write(b'L')
            ser.close()
            break
        else:
            print("Invalid input. Type on / off / quit.")
    print("Thank you for playing!")

time.sleep(3) # wait for the serial connection to initialize

game_on()