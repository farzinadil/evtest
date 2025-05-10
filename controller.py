import time, serial
from evdev import InputDevice, ecodes

EVDEV_DEVICE = '/dev/input/event0'  # your pedal’s keyboard interface
SERIAL_PORT  = '/dev/ttyUSB0'
BAUDRATE     = 9600

CMD = {
    1: b'PS1R\n',
    2: b'PS2R\n',
}
current = 1

ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
dev = InputDevice(EVDEV_DEVICE)
print("Waiting for pedal…")

for ev in dev.read_loop():
    if ev.type == ecodes.EV_KEY and ev.code == ecodes.KEY_B and ev.value == 1:
        current = 2 if current == 1 else 1
        ser.write(CMD[current])
        print(f"{time.strftime('%T')} → now on HDMI{current}")
