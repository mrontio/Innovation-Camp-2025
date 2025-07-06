import mpu6050
import time
import matplotlib.pyplot as plt

# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)

# Define a function to read the sensor data
def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050.get_accel_data()

    # Read the gyroscope values
    gyroscope_data = mpu6050.get_gyro_data()

    # Read temp
    temperature = mpu6050.get_temp()

    return accelerometer_data, gyroscope_data, temperature

for i in range(20):
    accelerometer_data, gyroscope_data, temperature = read_sensor_data()
    print("Accelerometer data:", accelerometer_data)
    print("Gyroscope data:", gyroscope_data)
    print("Temp:", temperature)
    if i == 0:
        accel_list = []
        gyro_list = []
        temp_list = []
    accel_list.append(accelerometer_data)
    gyro_list.append(gyroscope_data)
    temp_list.append(temperature)
    time.sleep(0.5)


plt.figure(figsize=(12,6))
plt.subplot(311)
plt.title("Accelerometer Data")
x_vals = [entry['x'] for entry in accel_list]
y_vals = [entry['y'] for entry in accel_list]
z_vals = [entry['z'] for entry in accel_list]
plt.plot(x_vals, label='x')
plt.plot(y_vals, label='y')
plt.plot(z_vals, label='z')
plt.legend()



plt.subplot(312)
plt.title("Gyroscope Data")
x_vals = [item['x'] for item in gyro_list]
y_vals = [item['y'] for item in gyro_list]
z_vals = [item['z'] for item in gyro_list]
plt.plot(x_vals, label='x')
plt.plot(y_vals, label='y')
plt.plot(z_vals, label='z')
plt.legend()

plt.subplot(313)
plt.title("Temperature Data")
plt.plot(temp_list)
plt.tight_layout()
plt.savefig('yeah.png')
