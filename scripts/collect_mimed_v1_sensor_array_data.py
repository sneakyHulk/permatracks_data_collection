import itertools
import csv
import numpy as np
import math

from scripts.collect import collect_position_direction_values, collect

def get_holes_position_direction_values(holes_descriptions):
    with open("../data/test.csv", "w") as file:
        writer = csv.DictWriter(file,
                                fieldnames=["mag_x0", "mag_y0", "mag_z0", "mag_theta0", "mag_phi0"])

        writer.writeheader()
        writer.writerow({'mag_x0': None, 'mag_y0': None, 'mag_z0': None, 'mag_theta0': None, 'mag_phi0': None})
        for holes_description in holes_descriptions:
            if holes_description['holes_facing'] == 'x':
                writer.writerow({'mag_x0': 7.5e-3 + (holes_description['x_pos'] - 1) * 15e-3,
                                 "mag_y0": 0e-3 + (holes_description['y_pos'] - 1) * 15e-3, 'mag_z0': 54e-3,
                                 'mag_theta0': 90 * math.pi / 180 if holes_description[
                                     'in_positive_direction'] else -90 * math.pi / 180,
                                 'mag_phi0': 0})
            elif holes_description['holes_facing'] == 'y':
                writer.writerow({'mag_x0': 0e-3 + (holes_description['x_pos'] - 1) * 15e-3,
                                 "mag_y0": 7.5e-3 + (holes_description['y_pos'] - 1) * 15e-3, 'mag_z0': 54e-3,
                                 'mag_theta0': 90 * math.pi / 180,
                                 'mag_phi0': 90 * math.pi / 180 if holes_description[
                                     'in_positive_direction'] else -90 * math.pi / 180})
            elif holes_description['holes_facing'] == 'z':
                writer.writerow({'mag_x0': 0e-3 + (holes_description['x_pos'] - 1) * 15e-3,
                                 "mag_y0": 0e-3 + (holes_description['y_pos'] - 1) * 15e-3, 'mag_z0': 54e-3,
                                 'mag_theta0': 0 if holes_description['in_positive_direction'] else 180 * math.pi / 180,
                                 'mag_phi0': 0})
            else:
                raise ValueError("Invalid holes_facing")


def get_sensor_position_values(rows=4, columns=4, stride=30e-3, start=(22.5e-3, 22.5e-3)):
    return np.array([[start[0] + row * stride, start[1] + column * stride, 0] for column, row in
                     itertools.product(range(columns), range(rows))])


def collect_mag_data_position_direction_values(filepaths):
    return collect(filepaths), collect_position_direction_values(filepaths)


if __name__ == '__main__':
    filepaths = ["../data/mag_data_LIS3MDL_ARRAY_mean_2025Mar14_15h26min51s_calibration_x.txt",
                 "../data/mag_data_LIS3MDL_ARRAY_mean_2025Mar14_15h39min41s_calibration_y.txt",
                 "../data/mag_data_LIS3MDL_ARRAY_mean_2025Mar14_15h45min44s_calibration_z.txt"]

    print(collect(filepaths))
    print(collect_position_direction_values(filepaths))

    get_sensor_position_values(4, 4, 30e-3, (40e-3, 45e-3))

    holes_descriptions_x = [{'holes_facing': 'x', 'x_pos': 1, 'y_pos': 1, 'in_positive_direction': True},
                            {'holes_facing': 'x', 'x_pos': 1, 'y_pos': 1, 'in_positive_direction': False},
                            {'holes_facing': 'x', 'x_pos': 10, 'y_pos': 1, 'in_positive_direction': True},
                            {'holes_facing': 'x', 'x_pos': 10, 'y_pos': 1, 'in_positive_direction': False},
                            {'holes_facing': 'x', 'x_pos': 10, 'y_pos': 11, 'in_positive_direction': True},
                            {'holes_facing': 'x', 'x_pos': 10, 'y_pos': 11, 'in_positive_direction': False},
                            {'holes_facing': 'x', 'x_pos': 1, 'y_pos': 11, 'in_positive_direction': True},
                            {'holes_facing': 'x', 'x_pos': 1, 'y_pos': 11, 'in_positive_direction': False},
                            {'holes_facing': 'x', 'x_pos': 5, 'y_pos': 6, 'in_positive_direction': True},
                            {'holes_facing': 'x', 'x_pos': 5, 'y_pos': 6, 'in_positive_direction': False}]

    holes_descriptions_y = [{'holes_facing': 'y', 'x_pos': 1, 'y_pos': 1, 'in_positive_direction': True},
                            {'holes_facing': 'y', 'x_pos': 1, 'y_pos': 1, 'in_positive_direction': False},
                            {'holes_facing': 'y', 'x_pos': 11, 'y_pos': 1, 'in_positive_direction': True},
                            {'holes_facing': 'y', 'x_pos': 11, 'y_pos': 1, 'in_positive_direction': False},
                            {'holes_facing': 'y', 'x_pos': 11, 'y_pos': 10, 'in_positive_direction': True},
                            {'holes_facing': 'y', 'x_pos': 11, 'y_pos': 10, 'in_positive_direction': False},
                            {'holes_facing': 'y', 'x_pos': 1, 'y_pos': 10, 'in_positive_direction': True},
                            {'holes_facing': 'y', 'x_pos': 1, 'y_pos': 10, 'in_positive_direction': False},
                            {'holes_facing': 'y', 'x_pos': 5, 'y_pos': 6, 'in_positive_direction': True},
                            {'holes_facing': 'y', 'x_pos': 5, 'y_pos': 6, 'in_positive_direction': False}]

    holes_descriptions_z = [{'holes_facing': 'z', 'x_pos': 1, 'y_pos': 1, 'in_positive_direction': True},
                            {'holes_facing': 'z', 'x_pos': 1, 'y_pos': 1, 'in_positive_direction': True},
                            {'holes_facing': 'z', 'x_pos': 11, 'y_pos': 1, 'in_positive_direction': True},
                            {'holes_facing': 'z', 'x_pos': 11, 'y_pos': 1, 'in_positive_direction': True},
                            {'holes_facing': 'z', 'x_pos': 11, 'y_pos': 11, 'in_positive_direction': True},
                            {'holes_facing': 'z', 'x_pos': 11, 'y_pos': 11, 'in_positive_direction': True},
                            {'holes_facing': 'z', 'x_pos': 1, 'y_pos': 11, 'in_positive_direction': True},
                            {'holes_facing': 'z', 'x_pos': 1, 'y_pos': 11, 'in_positive_direction': True},
                            {'holes_facing': 'z', 'x_pos': 6, 'y_pos': 6, 'in_positive_direction': True},
                            {'holes_facing': 'z', 'x_pos': 6, 'y_pos': 6, 'in_positive_direction': True}]

    holes_descriptions_test = [{'holes_facing': 'x', 'x_pos': 1, 'y_pos': 3, 'in_positive_direction': True},
                               {'holes_facing': 'x', 'x_pos': 2, 'y_pos': 3, 'in_positive_direction': True},
                               {'holes_facing': 'x', 'x_pos': 3, 'y_pos': 3, 'in_positive_direction': True},
                               {'holes_facing': 'x', 'x_pos': 4, 'y_pos': 3, 'in_positive_direction': True},
                               {'holes_facing': 'x', 'x_pos': 5, 'y_pos': 3, 'in_positive_direction': True},
                               {'holes_facing': 'x', 'x_pos': 6, 'y_pos': 3, 'in_positive_direction': True},
                               {'holes_facing': 'x', 'x_pos': 7, 'y_pos': 3, 'in_positive_direction': True},
                               {'holes_facing': 'x', 'x_pos': 8, 'y_pos': 3, 'in_positive_direction': True},
                               {'holes_facing': 'x', 'x_pos': 9, 'y_pos': 3, 'in_positive_direction': True},
                               {'holes_facing': 'x', 'x_pos': 10, 'y_pos': 3, 'in_positive_direction': True}]

    get_holes_position_direction_values(holes_descriptions_x)
    get_holes_position_direction_values(holes_descriptions_y)
    get_holes_position_direction_values(holes_descriptions_z)
    get_holes_position_direction_values(holes_descriptions_test)
