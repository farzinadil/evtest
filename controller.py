#!/usr/bin/env python3
import time
import serial
from evdev import InputDevice, ecodes, categorize

# ————— CONFIG ——————————————————————————
EVDEV_DEVICE = '/dev/input/event0'   # your pedal’s event node
SERIAL_PORT  = '/dev/ttyUSB0'        # your USB-RS232 adapter
BAUDRATE     = 115200

# J-Tech JTD-2996 toggle commands
CMD = {
    1: bytes([0xA0, 0x01, 0x01, (0xA0+0x01+0x01)&0xFF]),
    2: bytes([0xA0, 0x01, 0x02, (0xA0+0x01+0x02)&0xFF]),
}
# start on input 1
current = 1

# ————— SETUP ——————————————————————————
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
dev = InputDevice(EVDEV_DEVICE)
print(f"Listening for KEY_B on {dev.path}…")

# ————— MAIN LOOP ——————————————————————————
for ev in dev.read_loop():
    if ev.type == ecodes.EV_KEY and ev.code == ecodes.KEY_B and ev.value == 1:
        # toggle
        current = 2 if current == 1 else 1
        ser.write(CMD[current])
        print(f"[{time.strftime('%H:%M:%S')}] Toggled to HDMI input {current}")
