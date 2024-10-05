from picozero import Pot # Pot is short for Potentiometer
from time import sleep

dial1 = Pot(0) # Connected to pin A0 (GP_26)
dial2 = Pot(1) # Connected to pin A1 (GP_27)
uart = machine.UART(0, baudrate=115200)

while True:
    value1 = dial1.value
    value2 = dial2.value
    print(f"{value1,value2}")
    sleep(0.1) # slow down the output