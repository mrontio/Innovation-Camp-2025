# Pi Sensor Examples
This directory contains the examples for a selected number of sensors.
Here is the table with links to guides used (or chatgpt where applicable).

| Sensor                   | Example                  | Tutorial Used                                                                                       | Notes                                             |
|:-------------------------|:-------------------------|:----------------------------------------------------------------------------------------------------|:--------------------------------------------------|
| ADC (MCP3008)            | [adc.py](./adc.py)         | [Link](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008)                | Use the function in here whenever you need an ADC |
| Ultrasonic               | [ultrasonic.py](./ultrasonic.py)  | [Link](https://projects.raspberrypi.org/en/projects/physical-computing/12)                          | 330R, 470R                                        |
| Membrane Keypad          | [keypad.py](./keypad.py)      | [Link](https://www.digikey.co.uk/en/maker/tutorials/2021/how-to-connect-a-keypad-to-a-raspberry-pi) |                                                   |
| Laser emitter (KY-008)   | [laser.py](./laser.py)       | ChatGPT                                                                                             |                                                   |
| Gyroscope (GY-521)       | [gyro.py](./gyro.py)        | [Link](https://www.instructables.com/How-to-Use-the-MPU6050-With-the-Raspberry-Pi-4/)               |                                                   |
| Temperature sensor       | [dht11.py](./dht11.py)       | [Link](https://randomnerdtutorials.com/raspberry-pi-dht11-dht22-python/)                            | 4.7k resistor                                     |
| Motion sensor (HC-SR501) | [motion.py](./motion.py)      | ChatGPT                                                                                             |                                                   |
| Linear Hall (KY-024)     | [linear-hall.py](./linear-hall.py) | ChatGPT                                                                                             | ADC                                               |
| 1602 Display             | [display.py](./display.py)     | [YouTube](https://www.youtube.com/watch?v=DHbLBTRpTWM&t=1s)                                         | I2C Hat                                           |
| Water level sensor       | [water-level.py](./water-level.py) | ChatGPT                                                                                             | ADC                                               |
| Photo Interrupter        | [interrupter.py](./interrupter.py) | [Link](https://docs.sunfounder.com/projects/sensorkit-v2-pi/en/latest/lesson_12.html)               |                                                   |
| RGB Led                  | [rgb.py](./rgb.py)         |                                                                                                     |                                                   |


If you have any questions about any of these, don't hesitate to ask Michail! (okay, maybe hesitate a little bit).

## Oh no, the sensor I want to use is not in this list!

That's the fun of it.
The Pi ecosystem is so mature now that it is more than simple to look up what you need.
Just like in the video, you need 3 things:
1. A wiring diagram.
2. Sample code.
3. Someone to explain things to you in case you get lost.

When searching, make sure to note the part number down. It narrows the search a lot to exactly what you need.
When asking ChatGPT queries, here's a good prompt to use:
```
I am building a Raspberry Pi 4b project with a breadboard. I will ask you to help me with connecting speciifc sensors. Specifically, I would like you to (A) Give me the wiring instructions in a table, (B) Give me a quick code sample which I want to use and (C) if you are able to access the internet, provide sources for the wiring diagram, thank you very much. For now, could you please give me instructions to use the sensor: <SENSOR>
```

Advice for LLMs
- **DOUBLE CHECK WIRING**, it does get part numbers wrong.
- Turn on web search. It's much better if it can find links for you to follow as they are more likely to get you a working version.
- Only one sensor at a time. Do not ask it to hook up multiple sensors. You can abstract the working code into functions, and then ask it to combine it for you in whichever way.
