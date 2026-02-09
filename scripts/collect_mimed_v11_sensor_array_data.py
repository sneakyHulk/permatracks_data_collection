import itertools
import numpy as np
import matplotlib.pyplot as plt

from scripts.collect import collect_position_direction_values, collect, collect_position_direction_vector_values


def get_sensor_position_values():
    return np.concatenate(([[5e-3 + row * 35e-3, 5e-3 + column * 35e-3, 0] for column, row in
                            itertools.product(range(5), range(5))],
                           [[22.5e-3 + row * 35e-3, 22.5e-3 + column * 35e-3, 0] for column, row in
                            itertools.product(range(4), range(4))]))


def get_sensor_noise_values():
    return np.array(
        [0.04 * 1e-6, 0.04 * 1e-6, 0.04 * 1e-6] * 25 + [0.32 * 1e-6, 0.32 * 1e-6, 0.41 * 1e-6] * 16).reshape((41, 3))


def get_sensor_position_values_optimization():
    return np.concatenate(([[5e-3 + row * 35e-3, 5e-3 + column * 35e-3, 0] for column, row in
                            itertools.product(range(5), range(5))],
                           [[22.5e-3 + row * 35e-3, 22.5e-3 + column * 35e-3, 0] for column, row in
                            itertools.product(range(4), range(4))]))


def get_sensor_noise_values_optimization():
    return np.array(
        [0.04 * 1e-6, 0.04 * 1e-6, 0.04 * 1e-6] * 25 + [0.32 * 1e-6, 0.32 * 1e-6, 0.41 * 1e-6] * 16).reshape((41, 3))


def collect_mag_data_position_direction_values(filepaths):
    return collect(filepaths), collect_position_direction_values(filepaths)


def collect_mag_data_position_direction_vector_values(filepaths, skip=1):
    return collect(filepaths, skip), collect_position_direction_vector_values(filepaths, skip)

if __name__ == "__main__":
    filepaths = ["../data/mag_data_1758205094942749000_2025Sep18_16h18min14s_earth_magnetic_field_calibration.csv"]

    data = collect_mag_data_position_direction_values(filepaths)
    print(data)

    filepaths = ["../data/result_6_6_6_3_150_correct_coordinate_system_corrected.csv"]

    data = collect_mag_data_position_direction_values(filepaths)
    print(data)

    data = get_sensor_position_values_optimization()

    plt.figure(figsize=(6, 6), constrained_layout=True)
    plt.scatter(data[:, 0], data[:, 1])
    plt.grid(True)
    plt.axis("equal")

    for i, datapoint in enumerate(data):
        plt.text(datapoint[0], datapoint[1], str(i), fontsize=8, ha='right', va='bottom')

    plt.show()