# brillo.py
# Control de brillo mediante PWM software en GPIO12 
# Recibe valores 0–255 (por ejemplo, state.brillo_display).
# En el código:
# from brillo import BrilloController
# brillo = BrilloController()
# Cuando cambie el slider (mejor un callback desde state):
# brillo.set_brillo(state.brillo_display)

import RPi.GPIO as GPIO
import time

PWM_PIN = 12
PWM_FREQ = 1000  # 1 kHz → perfecto para brillo sin parpadeos

class BrilloController:
    def __init__(self, pin = PWM_PIN, freq = PWM_FREQ):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

        # PWM software (suficiente para brillo)
        self.pwm = GPIO.PWM(pin, freq)
        self.pwm.start(0)

    def set_brillo(self, value_0_255):
        # Limitar rango
        if value_0_255 < 0:
            value_0_255 = 0
        elif value_0_255 > 255:
            value_0_255 = 255

        # Convertir a porcentaje 0–100
        duty = (value_0_255 / 255) * 100
        self.pwm.ChangeDutyCycle(duty)

    def apagar(self):
        self.pwm.stop()
        GPIO.cleanup()

