from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

lcd = LCD()

def safe_exit(signgum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

try:
    lcd.text("Welcome ,", 1)
    lcd.text("MINDS and SustAI!", 2)

    pause()
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()
