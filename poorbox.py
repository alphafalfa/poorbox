#!/usr/bin/python

###########################################################################
# © Copyright-CK 2024 - All Rights Reserved
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
###########################################################################

# This Python script will read from /dev/ttyACM0 and send key events via uinput.
# If ACM0 doesn't work, check /dev/ttyACM?, it's probably just ACM1.
# Install python-uinput (`pip install python-uinput`) and pyserial (`pip install pyserial`) to run this script.
# List of accepted KEY codes here: /usr/include/linux/input-event-codes.h

import serial
import uinput

# Define a mapping from 4-byte hex codes to uinput key codes or events
KEY_CODE_MAPPING = {
    "0080": uinput.KEY_BACK,                    # ring down
    "0181": uinput.KEY_ESC,                     # thumb down
    "0282": uinput.KEY_REFRESH,                 # space bar down
    "0383": uinput.KEY_FORWARD,                 # pinky down
    "0a8a": uinput.KEY_PASTE,                   # scroll press
    "1090": uinput.KEY_UP,                      # north down
    "1191": uinput.KEY_DOWN,                    # south down
    "1292": uinput.KEY_LEFT,                    # west down
    "1393": uinput.KEY_RIGHT,                   # east down
    "22a2": uinput.KEY_PREVIOUSSONG,            # left dot down
    "23a3": uinput.KEY_NEXTSONG,                # right dot down
    "2aaa": uinput.KEY_PLAYPAUSE,               # moon down
    "37b7": uinput.KEY_MUTE,                    # knob down
    "38b8": uinput.KEY_COPY,                    # disc down
    "0484": uinput.KEY_VOLUMEDOWN,              # knob left
    "0989": "WHEEL_DOWN",                      # scroll down
    "0f8f": uinput.KEY_BRIGHTNESSUP,            # disc right
    "44c4": uinput.KEY_VOLUMEUP,                # knob right
    "49c9": "WHEEL_UP",                        # scroll up
    "4fcf": uinput.KEY_BRIGHTNESSDOWN           # disc left
}

# Setup uinput device for emulating keypresses
def setup_uinput_device():
    keys = [key for key in KEY_CODE_MAPPING.values() if isinstance(key, int)]
    return uinput.Device(keys + [uinput.REL_WHEEL])

def process_serial_data(serial_data_str, device):
    if serial_data_str in KEY_CODE_MAPPING:
        key_code = KEY_CODE_MAPPING[serial_data_str]
        if key_code == "WHEEL_UP":
            device.emit(uinput.REL_WHEEL, 1)  # Scroll up
        elif key_code == "WHEEL_DOWN":
            device.emit(uinput.REL_WHEEL, -1)  # Scroll down
        else:
            device.emit_click(key_code)
    else:
        print(f"Unknown key code: {serial_data_str}")

def main():
    try:
        # Serial configuration
        ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
        device = setup_uinput_device()

        while True:
            # Read input from serial device
            if ser.in_waiting > 0:
                serial_data = ser.read(2)  # Read 2 bytes
                if len(serial_data) == 2:  # Ensure we have exactly 2 bytes
                    serial_data_str = serial_data.hex()  # Convert binary data to hex string
                    process_serial_data(serial_data_str, device)
                else:
                    print(f"Unexpected data length: {len(serial_data)} bytes, data: {serial_data.hex()}")

    except (serial.SerialException, KeyboardInterrupt) as e:
        print(f"Exiting due to: {e}")
    finally:
        if ser:
            ser.close()

if __name__ == "__main__":
    main()

