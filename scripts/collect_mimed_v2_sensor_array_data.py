import numpy as np
import matplotlib.pyplot as plt


def get_sensor_position_values():
    return np.concatenate(
        ([[0e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[15e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[30e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[45e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[60e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[75e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[90e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[105e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[120e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[135e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[150e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[165e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[180e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)]))


def get_sensor_position_values_optimization():
    return np.concatenate(
        ([[0e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[15e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[30e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[45e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[60e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[75e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[90e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[105e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[120e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[135e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[150e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)],
         [[165e-3, 225e-3 - row * 30e-3, 0e-3] for row in range(8)],
         [[180e-3, 240e-3 - row * 30e-3, 0e-3] for row in range(9)]))


def get_sensor_noise_values():
    return np.array(
        [0.04 * 1e-6, 0.04 * 1e-6, 0.04 * 1e-6] * 111).reshape((111, 3))


def get_sensor_noise_values_optimization():
    return np.array(
        [0.04 * 1e-6, 0.04 * 1e-6, 0.04 * 1e-6] * 111).reshape((111, 3))


if __name__ == "__main__":
    data = get_sensor_position_values_optimization()

    plt.figure(figsize=(6, 6), constrained_layout=True)
    plt.scatter(data[:, 0], data[:, 1])
    plt.grid(True)
    plt.axis("equal")

    for i, datapoint in enumerate(data):
        plt.text(datapoint[0], datapoint[1], str(i), fontsize=8, ha='right', va='bottom')

    plt.show()