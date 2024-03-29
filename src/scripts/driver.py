
import serial
import time

# Setup
# 0(RX), 1(TX) Serial Pins
BAUD = 9600 # Baud Rate
arduino = serial.Serial('/dev/ttyACM0', 9600) # Found with 'ls /dev/tty.*' [this changes each time the arduino is connected]
print("Serial Port is open: {}".format(arduino.is_open))
print("Baud Rate: {}".format(BAUD))
# Serial pins for communication: 0(RX), 1(TX)

class RobotHand():
    """
    RobotHand that plays Rock, Paper, Scissors
    """
    states = ("Rock", "Paper", "Scissors")

    def __init__(self):
        self.state = self.states[1]

    def state_transition(self, state):
        """
        Abstraction for an FSM to move from one state to another

        Args:
            state (str)
        """
        self.state = state

    def play_rock(self):
        """
        Activate servos that form Rock hand.
        """
        self.state_transition("Rock")
        print("Rock!")
        arduino.write(b"R")

    def play_paper(self):
        """
        Activate respective seros [list them here] to form paper hand.
        """
        self.state_transition("Paper")
        print("Paper!")
        arduino.write(b"P")

    def play_scissor(self):
        """
        Activate respecftive servos [list them here] to form the scissor hand.
        """
        self.state_transition("Scissor")
        print("Scissor!")
        arduino.write(b"S")


def game_on():
    "Ask, wait, write"
    while True:
        hand = RobotHand()
        u_input = input("\n Choose your hand [Rock, Paper, Scissors]: ")
        if u_input in ["Rock", "rock", "R", "r"]:
            hand.play_rock()
            time.sleep(0.1)    
        elif u_input in ["Paper", "paper", "P", "p"]:
            hand.play_paper()
            time.sleep(0.1)
        elif u_input in ["Scissors", "scissors", "S", "s"]:
            hand.play_scissor()
            time.sleep(0.1)
        elif u_input in ["quit", "q"]:
            print("Program Exiting")
            time.sleep(0.1)
            arduino.close()
            break
        else:
            print("Invalid input. Type on / off / quit.")
    print("Thank you for playing!")

time.sleep(3) # wait for the serial connection to initialize

game_on()