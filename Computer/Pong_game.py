import serial

# Set up the serial connection (adjust 'COM12' to your port)
ser = serial.Serial('COM12', 115200, timeout=1)

while True:
    # Read the serial data from the Raspberry Pi Pico
    try:
        data = ser.readline().decode('utf-8').strip()
        data = data.strip('()')
        value1, value2 = data.split(',')
    except:
        value1 = 0
        value2 = 0
    float(value2)
    float(value1)

    print(value2)
    print(value1)