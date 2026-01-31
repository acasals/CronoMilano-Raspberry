# brillo.py
# Control de brillo mediante PWM software en GPIO12 
# Recibe valores 0–255 (por ejemplo, state.brillo_display).
# En el código:
# from brillo import BrilloController
# brillo = BrilloController()
# Cuando cambie el slider (mejor un callback desde state):
# brillo.set_brillo(state.brillo_display)

import RPi.GPIO as GPIO

PWM_PIN = 12
PWM_FREQ = 1000  # Hz

class BrilloController:
    def __init__(self, pin=PWM_PIN, freq=PWM_FREQ):
        self.pin = pin
        self.freq = freq
        self.initialized = False
        self.pwm = None

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)

            self.pwm = GPIO.PWM(self.pin, self.freq)
            self.pwm.start(0)

            self.initialized = True

        except Exception as e:
            print(f"[BrilloController] Error inicializando PWM: {e}")
            self.initialized = False

    def set_brillo(self, value_0_255):
        if not self.initialized:
            return

        if value_0_255 < 0:
            value_0_255 = 0
        elif value_0_255 > 255:
            value_0_255 = 255

        duty = (value_0_255 / 255) * 100

        try:
            self.pwm.ChangeDutyCycle(duty)
        except Exception as e:
            print(f"[BrilloController] Error cambiando duty: {e}")

    def apagar(self):
        if not self.initialized:
            return

        try:
            if self.pwm:
                self.pwm.stop()
        except Exception:
            pass

        try:
            GPIO.cleanup(self.pin)
        except Exception:
            pass

        self.initialized = False