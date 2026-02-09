import csv
import itertools
import numpy as np


def collect(filepaths, skip=1):
    def collect_single(filepath):
        with open(filepath) as file:
            reader = csv.DictReader(file)

            def relevant_fieldnames(fieldnames):
                for i in itertools.count(0):
                    if 'x' + str(i) in fieldnames and 'y' + str(i) in fieldnames and 'z' + str(i) in fieldnames:
                        yield ['x' + str(i), 'y' + str(i), 'z' + str(i)]
                    else:
                        break

            data = np.array([[[float(row[x]), float(row[y]), float(row[z])] for x, y, z in
                              relevant_fieldnames(reader.fieldnames)] for row in
                             itertools.islice(reader, skip, None)])
            return data

    data = np.concatenate([collect_single(filepath) for filepath in filepaths], axis=1)
    return data


def collect_position_direction_values(filepaths, skip=1):
    def collect_single(filepath):
        with open(filepath) as file:
            reader = csv.DictReader(file)

            def relevant_fieldnames(fieldnames):
                for i in itertools.count(0):
                    if 'mag_x' + str(i) in fieldnames and 'mag_y' + str(i) in fieldnames and 'mag_z' + str(
                            i) in fieldnames and 'mag_theta' + str(i) in fieldnames and 'mag_phi' + str(
                        i) in fieldnames:
                        yield ['mag_x' + str(i), 'mag_y' + str(i), 'mag_z' + str(i), 'mag_theta' + str(i),
                               'mag_phi' + str(i)]
                    else:
                        break

            data = np.array([[[float(row[mag_x]), float(row[mag_y]), float(row[mag_z]), float(row[mag_theta]),
                               float(row[mag_phi])] for mag_x, mag_y, mag_z, mag_theta, mag_phi in
                              relevant_fieldnames(reader.fieldnames)] for row in
                             itertools.islice(reader, skip, None)])
            return data

    data = np.concatenate([collect_single(filepath) for filepath in filepaths], axis=1)
    return data


def collect_position_direction_vector_values(filepaths, skip=1):
    def collect_single(filepath):
        with open(filepath) as file:
            reader = csv.DictReader(file)

            def relevant_fieldnames(fieldnames):
                for i in itertools.count(0):
                    if 'mag_x' + str(i) in fieldnames and 'mag_y' + str(i) in fieldnames and 'mag_z' + str(
                            i) in fieldnames and 'mag_mx' + str(i) in fieldnames and 'mag_my' + str(
                        i) in fieldnames and 'mag_mz' + str(i) in fieldnames:
                        yield ['mag_x' + str(i), 'mag_y' + str(i), 'mag_z' + str(i), 'mag_mx' + str(i),
                               'mag_my' + str(i), 'mag_mz' + str(i)]
                    else:
                        break

            data = np.array([[[float(row[mag_x]), float(row[mag_y]), float(row[mag_z]), float(row[mag_mx]),
                               float(row[mag_my]), float(row[mag_mz])] for mag_x, mag_y, mag_z, mag_mx, mag_my, mag_mz
                              in relevant_fieldnames(reader.fieldnames)] for row in
                             itertools.islice(reader, skip, None)])
            return data

    data = np.concatenate([collect_single(filepath) for filepath in filepaths], axis=1)
    return data


if __name__ == '__main__':
    filepaths = ["../data/mag_data_1758205094942749000_2025Sep18_16h18min14s_earth_magnetic_field_calibration.csv"]

    data = collect(filepaths, 0)  # 4999, 41, 3
    print(data)
