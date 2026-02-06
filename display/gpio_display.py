# gpio_display.py
# Control de 4 displays 7 elementos 
# 
import RPi.GPIO as GPIO
from time import sleep

alphabet = 'abcdefghijlnopqrstuy'
DIGITS = bytes(b'\x77\x11\xb6\xb3\xd1\xe3\xe7\x31\xf7\xf3')
ALPHABET = bytes(b'\xf5\xc7\x86\x97\xe6\xe4\xf3\xd5\x11\x13\x46\x85\x87\xf4\xf1\x84\xe3\xc6\x07\xd1')

DATA_PIN = 5        	# GPIO5 (pin físico 29)
LATCH_PIN = 13    		# GPIO13 (pin físico 33)
CLOCK_PIN = 6			# GPIO6 (pin fisico 31)

class DISPLAY7:
    def __init__(self, dataPIN = DATA_PIN, latchPIN = LATCH_PIN, clockPIN = CLOCK_PIN):
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.dataPIN = dataPIN
        self.latchPIN = latchPIN
        self.clockPIN = clockPIN

        GPIO.setup(self.dataPIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.latchPIN, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.clockPIN, GPIO.OUT, initial=GPIO.LOW)

    def clear(self):
        for _ in range(4):
            self.__postBlank()

        GPIO.output(self.latchPIN, GPIO.HIGH)
        GPIO.output(self.latchPIN, GPIO.LOW)

    def __postBlank(self):
        for _ in range(8):
            GPIO.output(self.clockPIN, GPIO.LOW)
            GPIO.output(self.dataPIN, GPIO.LOW)
            GPIO.output(self.clockPIN, GPIO.HIGH)

    def dashes(self):
        for _ in range(4):
            self.__postDash()

        GPIO.output(self.latchPIN, GPIO.HIGH)
        GPIO.output(self.latchPIN, GPIO.LOW)

    def __postDash(self):
        for x in range(8):
            GPIO.output(self.clockPIN, GPIO.LOW)
            GPIO.output(self.dataPIN, (128 & (1 << (7 - x))) != 0)
            GPIO.output(self.clockPIN, GPIO.HIGH)

    def __postDigit(self, digit, decimal):
        if isinstance(digit, int):
            segments = DIGITS[digit]
            if decimal:
                segments |= 8

            for x in range(8):
                GPIO.output(self.clockPIN, GPIO.LOW)
                GPIO.output(self.dataPIN, (segments & (1 << (7 - x))) != 0)
                GPIO.output(self.clockPIN, GPIO.HIGH)
        else:
            self.__postBlank()

    def __postChar(self, character):
        idx = alphabet.find(character)
        if idx < 0:
            self.__postBlank()
            return

        segments = ALPHABET[idx]
        for x in range(8):
            GPIO.output(self.clockPIN, GPIO.LOW)
            GPIO.output(self.dataPIN, (segments & (1 << (7 - x))) != 0)
            GPIO.output(self.clockPIN, GPIO.HIGH)

    def show(self, minutos, segundos):
        print(minutos,segundos)
        self.__postDigit(minutos // 10, False)
        self.__postDigit(minutos % 10, False)
        self.__postDigit(segundos // 10, True)
        self.__postDigit(segundos % 10, False)

        GPIO.output(self.latchPIN, GPIO.HIGH)
        GPIO.output(self.latchPIN, GPIO.LOW)

    def scroll(self, cadena, delay=250):
        print(cadena)
        cadena = '    ' + cadena + '     '

        for x in range(len(cadena) - 4):
            for y in range(4):
                c = cadena[x + y]

                if '0' <= c <= '9':
                    self.__postDigit(int(c), False)
                elif c == '-':
                    self.__postDash()
                elif alphabet.find(c) >= 0:
                    self.__postChar(c)
                else:
                    self.__postBlank()

            sleep(delay / 1000.0)

            GPIO.output(self.latchPIN, GPIO.HIGH)
            GPIO.output(self.latchPIN, GPIO.LOW)