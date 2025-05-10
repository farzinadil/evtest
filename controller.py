#!/usr/bin/env python3
from evdev import InputDevice, ecodes
import serial, time

# ————— CONFIG ————————————————
EVDEV_DEVICE = '/dev/input/event3'     # replace with your pedal’s event node
SERIAL_PORT  = '/dev/ttyUSB0'
BAUDRATE     = 115200
# J-Tech toggle commands:
CMD = {
    1: bytes([0xA0,0x01,0x01,(0xA0+0x01+0x01)&0xFF]),
    2: bytes([0xA0,0x01,0x02,(0xA0+0x01+0x02)&0xFF]),
}
current = 1
# ————————————————————————————

# Open serial to the HDMI switch
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

# Open the pedal’s evdev interface
dev = InputDevice(EVDEV_DEVICE)
print("Listening on", dev.path, "for pedal presses…")

for event in dev.read_loop():
    # A key‐press event with value==1 means “key down”
    if event.type == ecodes.EV_KEY and event.value == 1:
        if event.code == ecodes.KEY_F13:   # or whatever your pedal uses
            # toggle
            current = 2 if current == 1 else 1
            ser.write(CMD[current])
            print(f"[{time.strftime('%H:%M:%S')}] Toggled to input {current}")
