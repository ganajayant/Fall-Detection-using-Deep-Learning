# Code for wearble device such as Raspberry Pi to publish sensor data to RabbitMQ

import json
import time

import pika
import smbus

URL = "amqps://eqngwxhk:NSeWEGDZXu_YxStcpembCdwmZx9hMRpe@puffin.rmq2.cloudamqp.com/eqngwxhk"
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
DEVICE_ADDRESS = 0x68
DELAY_TIME = 1
ACCELERATION_SENSITIVITY = 16384.0
GYROSCOPE_SENSITIVITY = 131.0

try:
    params = pika.URLParameters(URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(exchange="sensor_data", exchange_type="fanout")
    channel.queue_declare(queue="sensor_data_queue")
    channel.queue_bind(exchange="sensor_data", queue="sensor_data_queue")
except pika.exceptions.AMQPError as e:
    print("Error connecting to RabbitMQ:", str(e))
    exit(1)


def MPU_Init():
    bus.write_byte_data(DEVICE_ADDRESS, SMPLRT_DIV, 7)
    bus.write_byte_data(DEVICE_ADDRESS, PWR_MGMT_1, 1)
    bus.write_byte_data(DEVICE_ADDRESS, CONFIG, 0)
    bus.write_byte_data(DEVICE_ADDRESS, GYRO_CONFIG, 24)
    bus.write_byte_data(DEVICE_ADDRESS, INT_ENABLE, 1)


def read_raw_data(addr):
    high = bus.read_byte_data(DEVICE_ADDRESS, addr)
    low = bus.read_byte_data(DEVICE_ADDRESS, addr + 1)
    value = (high << 8) | low
    if value > 32768:
        value = value - 65536
    return value


bus = smbus.SMBus(1)
MPU_Init()

while True:
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    Ax = acc_x / ACCELERATION_SENSITIVITY
    Ay = acc_y / ACCELERATION_SENSITIVITY
    Az = acc_z / ACCELERATION_SENSITIVITY
    Gx = gyro_x / GYROSCOPE_SENSITIVITY
    Gy = gyro_y / GYROSCOPE_SENSITIVITY
    Gz = gyro_z / GYROSCOPE_SENSITIVITY

    if None in [Ax, Ay, Az, Gx, Gy, Gz]:
        continue
    print(
        "\n Gx=%.3f °/s\tGy=%.3f °/s\tGz=%.3f °/s\tAx=%.3f g\tAy=%.3f g\tAz=%.3f g\n",
        Gx,
        Gy,
        Gz,
        Ax,
        Ay,
        Az,
    )
    data = {
        "accelerometer_x": Ax,
        "accelerometer_y": Ay,
        "accelerometer_z": Az,
        "gyroscope_x": Gx,
        "gyroscope_y": Gy,
        "gyroscope_z": Gz,
        "lat": 13.555541400652805,
        "longi": 80.02680962057917,
    }
    payload = json.dumps(data)

    try:
        channel.basic_publish(exchange="sensor_data", routing_key="", body=payload)
        print("Data published to the sensor_data exchange")
    except pika.exceptions.AMQPError as e:
        print("Error publishing data to RabbitMQ:", str(e))

    time.sleep(DELAY_TIME)
