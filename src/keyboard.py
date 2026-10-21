import os
import sys
import termios
import tty


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        first = os.read(fd, 1)
        if first == b"\x03":   # Ctrl+C
            return "CTRL_C"
        if first in (b"\r", b"\n"):
            return "ENTER"
        if first in (b"\x7f", b"\x08"):
            return "BACKSPACE"
        if first == b"\x1b":
            second = os.read(fd, 1)
            if second != b"[":
                return "ESC"
            third = os.read(fd, 1)
            if third == b"A":
                return "UP"
            if third == b"B":
                return "DOWN"
            if third == b"C":
                return "RIGHT"
            if third == b"D":
                return "LEFT"
            if third == b"H":
                return "HOME"
            if third == b"F":
                return "END"
            if third.isdigit():
                sequence = third
                while True:
                    char = os.read(fd, 1)
                    if char == b"~":
                        break
                    sequence += char
                if sequence in (b"1", b"7"):
                    return "HOME"
                if sequence in (b"4", b"8"):
                    return "END"
                if sequence == b"5":
                    return "PAGE_UP"
                if sequence == b"6":
                    return "PAGE_DOWN"
            return "ESC"
        try:
            return first.decode()
        except UnicodeDecodeError:
            return ""
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
