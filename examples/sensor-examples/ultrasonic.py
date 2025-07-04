from gpiozero import DistanceSensor
from time import sleep
import matplotlib.pyplot as plt

ultrasonic = DistanceSensor(echo=17, trigger=4)

distances = []
times = []

for i in range(20):
    dist = ultrasonic.distance * 100
    print(f"{i}: {dist:.1f} cm")
    distances.append(dist)
    times.append(i * 0.5)
    sleep(0.5)

plt.plot(times, distances)
plt.xlabel("Time (s)")
plt.ylabel("Distance (cm)")
plt.title("Ultrasonic Sensor Readings")
plt.grid(True)
plt.savefig('hehe.png')
