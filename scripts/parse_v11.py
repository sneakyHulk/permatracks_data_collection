import csv
import time

import numpy as np
import matplotlib.pyplot as plt
from serial import Serial
import platform
from crc import Calculator, Configuration
from collections import deque

crc16 = Calculator(
    Configuration(width=16, polynomial=0x8005, init_value=0x0000, final_xor_value=0x0000, reverse_input=True,
                  reverse_output=True), optimized=True)

crc8 = Calculator(
    Configuration(width=8, polynomial=0x07, init_value=0x00, final_xor_value=0x00, reverse_input=False,
                  reverse_output=False), optimized=True)


def parse(raw_bytes: bytes, n_bits_x: int, n_bits_y: int, n_bits_z: int, scale: int) -> tuple[float, float, float]:
    combined_value = int.from_bytes(raw_bytes, byteorder='little', signed=False)

    x_raw = (combined_value >> 0) & ((1 << n_bits_x) - 1)
    y_raw = (combined_value >> n_bits_x) & ((1 << n_bits_y) - 1)
    z_raw = (combined_value >> (n_bits_x + n_bits_y)) & ((1 << n_bits_z) - 1)

    x_signed = x_raw - (1 << n_bits_x) if (x_raw >> (n_bits_x - 1)) & 1 else x_raw
    y_signed = y_raw - (1 << n_bits_y) if (y_raw >> (n_bits_y - 1)) & 1 else y_raw
    z_signed = z_raw - (1 << n_bits_z) if (z_raw >> (n_bits_z - 1)) & 1 else z_raw

    return x_signed / scale, y_signed / scale, z_signed / scale


def run(serial_port_path: str, baud_rate, sensors: list[dict[str, int]]):

    magnetic_flux_density_message_size = int(1
                                             + int(np.sum([sensor["n_bytes"] for sensor in sensors]))
                                             # how many different sensors -> how many scale values
                                             + len({frozenset(sensor.items()) for sensor in sensors}) * 4
                                             + 8 + 2 + 1)
    timestamp_message_size = int(1 + 2 * 8 + 1 + 1)

    max_message_size = max(magnetic_flux_density_message_size, timestamp_message_size)

    with (Serial(serial_port_path, baud_rate, timeout=1) as serial_port):
        buffer = deque(maxlen=max_message_size)
        timestamps = deque(maxlen=timestamp_message_size)

        buffer.extend([b'0'] * max_message_size)
        timestamps.extend([int(0)] * timestamp_message_size)

        while True:
            timestamps.append(time.time_ns())
            byte = serial_port.read(1)
            buffer.append(byte)
            print(byte)

            if byte == b'T':
                if buffer[-timestamp_message_size] != b'T':
                    continue
                msg = bytes(x[0] for i, x in enumerate(buffer) if
                            max_message_size - timestamp_message_size + 1 <= i < max_message_size - 1 - 1)
                crc = crc8.checksum(msg).to_bytes(1, byteorder='little')

                if buffer[-2][0] != crc[0]:
                    continue

                t2 = time.time_ns()
                serial_port.write(b'T')
                serial_port.write(timestamps[0].to_bytes(8, byteorder='little'))
                serial_port.write(t2.to_bytes(8, byteorder='little'))
                crc = crc8.checksum([timestamps[0].to_bytes(8, byteorder='little'), t2.to_bytes(8, byteorder='little')])
                serial_port.write(crc.to_bytes(1, byteorder='little'))
                serial_port.write(b'T')

            if byte == b'M':
                if buffer[-magnetic_flux_density_message_size] != b'M':
                    continue

                msg = bytes(x[0] for i, x in enumerate(buffer) if
                            max_message_size - magnetic_flux_density_message_size + 1 <= i < max_message_size - 2 - 1)
                crc = crc16.checksum(msg).to_bytes(2, byteorder='little')

                if buffer[-3][0] != crc[0]:
                    continue

                if buffer[-2][0] != crc[1]:
                    continue

                sensor_type = None
                scale = None
                offset = 0
                index = None

                data = np.zeros((len(sensors), 3))

                for sensor in sensors:
                    if sensor_type != sensor["type"]:
                        sensor_type = sensor["type"]
                        index = sensor["starting_index"]
                        scale = int.from_bytes(msg[offset:offset + 4], byteorder='little', signed=False)
                        offset += 4

                    x, y, z = parse(msg[offset:offset + sensor["n_bytes"]], sensor["n_bits_x"], sensor["n_bits_y"],
                                    sensor["n_bits_z"], scale)
                    offset += sensor["n_bytes"]
                    data[index] = (x, y, z)
                    index += 1

                timestamp = int.from_bytes(msg[offset:offset + 8], byteorder='little', signed=False)

                return timestamp, data


if __name__ == "__main__":
    baud_rate = 230400
    os_name = platform.system()
    if os_name == 'Linux':
        serial_port_path = "/dev/ttyUSB0"
    elif os_name == 'Darwin':
        serial_port_path = "/dev/cu.usbserial-0001"
    else:
        raise RuntimeError("Unsupported OS")

    sensors = [{"type": 'LIS3MDL', "n_bits_x": 16, "n_bits_y": 16, "n_bits_z": 16, "n_bytes": 6,
                "starting_index": 25}] * 16 + [
                  {"type": 'MMC5983MA', "n_bits_x": 19, "n_bits_y": 19, "n_bits_z": 18, "n_bytes": 7,
                   "starting_index": 0}] * 25

    for timestamp, data in run(serial_port_path, baud_rate, sensors):
        print(data, timestamp)
