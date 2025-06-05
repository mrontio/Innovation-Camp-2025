import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)            # bus 0, device 0 (CE0)
spi.max_speed_hz = 1350000

def read_ch(ch):
    # send start bit, single-ended mode, channel (ch 0–7)
    cmd = 0b11 << 6 | (ch & 0x07) << 3
    resp = spi.xfer2([cmd, 0, 0])
    return ((resp[0] & 1) << 9) | (resp[1] << 1) | (resp[2] >> 7)

channel = 0
value = read_ch(channel)
print(f"Value from channel {channel}: {value}")
