import os
import sys
import base64
import tkinter as tk
from tkinter import messagebox

def get_machine_serial():
    if sys.platform == 'win32':
        serial_cmd = 'wmic bios get serialnumber'
    elif sys.platform == 'darwin':
        serial_cmd = 'ioreg -l | grep IOPlatformSerialNumber'
    else:
        raise NotImplementedError("Serial number retrieval not supported on this platform.")
    serial = os.popen(serial_cmd).read().strip().split('\n')[-1].strip()
    encoded = base64.b64encode(serial.encode('utf-8'))
    encoded_text = encoded.decode('utf-8')
    return encoded_text

# Thay thế bằng chuỗi bạn muốn kiểm tra
serial_number = "SN22051J005592"
encoded_serial_number = base64.b64encode(serial_number.encode('utf-8')).decode('utf-8')

print(f"Encoded serial number: {encoded_serial_number}")


"wmic bios get serialnumber"
