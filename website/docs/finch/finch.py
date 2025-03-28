"""Finch Robot API v2.0 by Chris Mayfield <mayfiecs@jmu.edu>.

The Finch is a robot for computer science education. Its design is
the result of a four year study at Carnegie Mellon's CREATE lab.

This module provides classes for controlling Finch robots. It is
based on finch.py and finchconnection.py (see FinchPython120.zip
on https://www.finchrobot.com/software/python) originally written
by Jay Jin, Justas Sadzevicius, and others. The HID code has been
modified to support connecting to multiple robots.
"""

import atexit
import ctypes
import os
import platform
import sys
import threading
import time

VENDOR_ID = 0x2354
DEVICE_ID = 0x1111

HIDAPI_LIBRARY_PATH = os.environ.get('HIDAPI_LIB_PATH', './')
PING_FREQUENCY_SECONDS = 2.0  # seconds

# detect which operating system is present and load corresponding library

system = platform.system()

if system == 'Windows':
    if sys.maxsize > 2**32:
        hid_api = ctypes.CDLL(os.path.join(HIDAPI_LIBRARY_PATH, "hidapi64.dll"))
    else:
        hid_api = ctypes.CDLL(os.path.join(HIDAPI_LIBRARY_PATH, "hidapi32.dll"))

elif system == 'Linux':
    if sys.maxsize > 2**32:
        hid_api = ctypes.CDLL(os.path.join(HIDAPI_LIBRARY_PATH, "libhidapi64.so"))
    else:
        hid_api = ctypes.CDLL(os.path.join(HIDAPI_LIBRARY_PATH, "libhidapi32.so"))

elif system == 'Darwin':
    hid_api = ctypes.CDLL(os.path.join(HIDAPI_LIBRARY_PATH, "libhidapi.dylib"))

else: # Raspberry Pi
    hid_api = ctypes.CDLL(os.path.join(HIDAPI_LIBRARY_PATH, "libhidapipi.so"))

# http://www.signal11.us/oss/hidapi/hidapi/doxygen/html/structhid__device__info.html

class HIDInfo(ctypes.Structure):
    pass

HIDInfo._fields_ = [
    ("path", ctypes.c_char_p),
    ("vendor_id", ctypes.c_ushort),
    ("product_id", ctypes.c_ushort),
    ("serial_number", ctypes.c_wchar_p),
    ("release_number", ctypes.c_ushort),
    ("manufacturer_string", ctypes.c_wchar_p),
    ("product_string", ctypes.c_wchar_p),
    ("usage_page", ctypes.c_ushort),
    ("usage", ctypes.c_ushort),
    ("interface_number", ctypes.c_int),
    ("next", ctypes.POINTER(HIDInfo))]

def _get_all_paths():
    paths = []
    # get all connected finches
    hid_api.hid_enumerate.restype = ctypes.POINTER(HIDInfo)
    head = hid_api.hid_enumerate(
        ctypes.c_ushort(VENDOR_ID), ctypes.c_ushort(DEVICE_ID))
    # iterate the linked list
    curr = head
    while curr:
        paths.append(curr.contents.path)
        curr = curr.contents.next
    # free the linked list
    hid_api.hid_free_enumeration.argtypes = [ctypes.POINTER(HIDInfo)]
    hid_api.hid_free_enumeration(head)
    return paths

# functions that handle the list of open finches

_open_finches = []

def _new_finch_connected(finch):
    if finch not in _open_finches:
        _open_finches.append(finch)

def _close_all_finches():
    for finch in _open_finches:
        if finch.is_open():
            finch.close()

atexit.register(_close_all_finches)

#-------------------------------------------------------------------------------
# FinchConnection

class FinchConnection:
    """ USB connection to the Finch robot. Uses the HID API
        to read and write from the robot. """

    def __init__(self):
        self.c_finch_handle = ctypes.c_void_p(None)
        self.c_io_buffer = ctypes.c_char_p(None)
        self.cmd_id = 0
        self.path = b''

    def is_open(self):
        """ Returns True if connected to the robot. """
        return bool(self.c_finch_handle)

    def open(self):
        """ Connect to the robot.

        This method looks for a USB port the Finch is connceted to. """

        if self.is_open():
            self.close()
        # get the next available path
        used = [finch.path for finch in _open_finches]
        for path in _get_all_paths():
            if path not in used:
                break
        else:
            raise Exception("Finch not found on USB (%d in use)." % len(used))
        # connect to the robot path
        try:
            hid_api.hid_open_path.restype = ctypes.c_void_p
            self.c_finch_handle = hid_api.hid_open_path(path)
            self.c_io_buffer = ctypes.create_string_buffer(9)
            self.cmd_id = self.read_cmd_id()
            self.path = path
            _new_finch_connected(self)
        except:
            raise Exception("Failed to connect to the Finch robot.")

    def close(self):
        """ Disconnect the robot. """

        if self.c_finch_handle:
            self.send(b'R', [0]) # exit to idle (rest) mode
            hid_api.hid_close.argtypes = [ctypes.c_void_p]
            hid_api.hid_close(self.c_finch_handle)
        if self in _open_finches:
            _open_finches.remove(self)
        FinchConnection.__init__(self)

    def read_cmd_id(self):
        """ Read the robot's internal command counter. """

        self.send(b'z')
        data = self.receive()
        return data[0]

    def send(self, command, payload=()):
        """Send a command to the robot (internal).

        command: The command ASCII character
        payload: a list of up to 6 bytes of additional command info """

        if not self.is_open():
            raise Exception("Connection to Finch was closed.")

        # Format the buffer to contain the contents of the payload.
        for i in range(7):
            self.c_io_buffer[i] = b'\x00'
        self.c_io_buffer[1] = command[0]

        python_version = sys.version_info[0]

        if payload:
            for i in range(len(payload)):
                if python_version >= 3:
                    self.c_io_buffer[i+2] = payload[i]
                else:
                    self.c_io_buffer[i+2] = bytes(chr(payload[i]))
        # Make sure command id is incremented if this is a receive case
        else:
            self.cmd_id = (self.cmd_id + 1) % 256

        if python_version >= 3:
            self.c_io_buffer[8] = self.cmd_id
        else:
            self.c_io_buffer[8] = bytes(chr(self.cmd_id))

        # Write to the Finch bufffer
        res = 0
        while not res:
            hid_api.hid_write.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
            res = hid_api.hid_write(self.c_finch_handle, self.c_io_buffer, ctypes.c_size_t(9))

    def receive(self):
        """ Read the data from the Finch buffer. """

        res = 9
        while res > 0:
            hid_api.hid_read.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
            if system == 'Darwin':
                res = hid_api.hid_read(self.c_finch_handle, self.c_io_buffer, ctypes.c_size_t(9))
            else:
                res = hid_api.hid_read_timeout(self.c_finch_handle, self.c_io_buffer, ctypes.c_size_t(9), 50)
            if self.cmd_id == ord(self.c_io_buffer[8]):
                break
        return [ord(self.c_io_buffer[i]) for i in range(9)]

#-------------------------------------------------------------------------------
# ThreadedFinchConnection

def _inherit_docstring(cls):
    def doc_setter(method):
        parent = getattr(cls, method.__name__)
        method.__doc__ = parent.__doc__
        return method
    return doc_setter

class ThreadedFinchConnection(FinchConnection):
    """ Threaded implementation of FinchConnection """

    def __init__(self):
        FinchConnection.__init__(self)
        self.lock = None
        self.thread = None
        self.main_thread = None
        self.last_cmd_sent = time.time()

    @_inherit_docstring(FinchConnection)
    def open(self):
        FinchConnection.open(self)
        if not self.is_open():
            return
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.__class__._pinger, args=(self, ))
        self.main_thread = threading.current_thread()
        self.thread.start()

    @_inherit_docstring(FinchConnection)
    def send(self, command, payload=()):
        try:
            if self.lock is not None:
                self.lock.acquire()
            FinchConnection.send(self, command, payload=payload)
            self.last_cmd_sent = time.time()
        finally:
            if self.lock is not None:
                self.lock.release()

    @_inherit_docstring(FinchConnection)
    def receive(self):
        try:
            if self.lock is not None:
                self.lock.acquire()
            data = FinchConnection.receive(self)
        finally:
            if self.lock is not None:
                self.lock.release()
        return data

    def _pinger(self):
        """ Sends keep-alive commands every few secconds of inactivity. """

        while True:
            if not self.lock:
                break
            if not self.c_finch_handle:
                break
            if not self.main_thread.isAlive():
                break
            try:
                self.lock.acquire()
                now = time.time()
                if self.last_cmd_sent:
                    delta = now - self.last_cmd_sent
                else:
                    delta = PING_FREQUENCY_SECONDS
                if delta >= PING_FREQUENCY_SECONDS:
                    FinchConnection.send(self, b'z')
                    FinchConnection.receive(self)
                    self.last_cmd_sent = now
            finally:
                self.lock.release()
            time.sleep(0.1)

    @_inherit_docstring(FinchConnection)
    def close(self):
        FinchConnection.close(self)
        self.thread.join()
        self.lock = None
        self.thread = None

#-------------------------------------------------------------------------------
# Finch

class Finch:
    """ API for controling a Finch robot. """

    def __init__(self):
        self.connection = ThreadedFinchConnection()
        self.connection.open()

    def close(self):
        """ Closes the connection to the Finch. """
        self.connection.close()

    def halt(self):
        """ Set all motors and LEDs to off. """
        self.connection.send(b'X', [0])

    def led(self, *args):
        """ Control three LEDs (orbs).

            Hex triplet string: led('#00FF8B') or
            0-255 RGB values: led(0, 255, 139) """

        if len(args) == 3:
            r, g, b = [int(x) % 256 for x in args]
        elif (len(args) == 1 and isinstance(args[0], str)):
            color = args[0].strip()
            if len(color) == 7 and color.startswith('#'):
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
        else:
            return
        self.connection.send(b'O', [r, g, b])

    def wheels(self, left, right):
        """ Controls the left and right wheels.

        Values must range from -1.0 (full throttle reverse) to
        1.0 (full throttle forward). Use (0.0,0.0) to stop. """

        dir_left = int(left < 0)
        dir_right = int(right < 0)
        left = min(abs(int(left * 255)), 255)
        right = min(abs(int(right * 255)), 255)
        self.connection.send(b'M', [dir_left, left, dir_right, right])

    def buzzer(self, duration, frequency):
        """ Outputs sound. Does not wait until a note is done beeping.

        duration - duration to beep, in seconds (s).
        frequency - integer frequency, in hertz (HZ). """

        millisec = int(duration * 1000)
        self.connection.send(b'B',
                [(millisec & 0xff00) >> 8, millisec & 0x00ff,
                 (frequency & 0xff00) >> 8, frequency & 0x00ff])

    def temperature(self):
        """ Returns temperature in degrees Celsius. """

        self.connection.send(b'T')
        data = self.connection.receive()
        if data is not None:
            return (data[0] - 127) / 2.4 + 25;

    def light(self):
        """ Get light sensor readings. The values ranges from 0.0 to 1.0.

            returns - a tuple(left, right) of two real values """

        self.connection.send(b'L')
        data = self.connection.receive()
        if data is not None:
            left = data[0] / 255.0
            right = data[1] / 255.0
            return left, right

    def obstacle(self):
        """ Get obstacle sensor readings.

            returns - a tuple(left,right) of two boolean values """

        self.connection.send(b'I')
        data = self.connection.receive()
        if data is not None:
            left = data[0] != 0
            right = data[1] != 0
            return left, right

    def _convert_raw_accel(self, a):
        """ Converts raw acceleration obtained from the hardware into G's. """

        if a > 31:
            a -= 64
        return a * 1.6 / 32.0

    def acceleration(self):
        """ Returns (x, y, z, tap, shake).
            x, y, and z are the acceleration readings in units of G's and range from -1.5 to 1.5.
            When the finch is horizontal, z is close to 1; x and y are close to 0.
            When the finch stands on its tail, y and z are close to 0; x is close to -1.
            When the finch is held with its left wing down, x and z are close to 0; y is close to 1.
            tap and shake are boolean values; true if the correspondig event has happened. """

        self.connection.send(b'A')
        data = self.connection.receive()
        if data is not None:
            x = self._convert_raw_accel(data[1])
            y = self._convert_raw_accel(data[2])
            z = self._convert_raw_accel(data[3])
            tap = (data[4] & 0x20) != 0
            shake = (data[4] & 0x80) != 0
            return (x, y, z, tap, shake)

#-------------------------------------------------------------------------------
# Test program

if __name__ == "__main__":
    romeo = Finch()
    romeo.led(30, 144, 255)
    juliet = Finch()
    juliet.led(255, 20, 147)
    time.sleep(3.0)
