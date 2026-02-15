import time
import csv
import os
import numpy as np
from sksurgerynditracker.nditracker import NDITracker
from scipy.spatial.transform import Rotation


def track_optical_generator(settings,
                            origin=np.array([[1, 0, 0, 18.25],
                                             [0, 1, 0, 13.25],
                                             [0, 0, 1, 0],
                                             [0, 0, 0, 1]])):
    tracker = NDITracker(settings)
    tracker.start_tracking()

    while True:
        try:
            port_handles, timestamps, framenumbers, tracking, quality = tracker.get_frame()

            TM = np.dot(np.linalg.inv(origin), np.dot(np.linalg.inv(tracking[0]), tracking[1]))
            Q = Rotation.from_matrix(TM[:3, :3]).as_quat(canonical=True, scalar_first=True)
            D = TM[:3, 2]  # get direction vector when board is [0, 0, 1]
            T = TM[:3, 3]

            print("Transformation Matrix (TM):\n", TM)
            print("Translation (T):", T, "mm")
            print("Quaternion (Q):", Q)
            print("Direction Vector (D):", D)
            print("Timestamps:", np.array(timestamps))

            yield int(np.mean(np.array(timestamps) * 1e9)), *(T * 1e-3), *D, *Q

        except OSError as os_err:
            print("OSError during get_frame. Possible tracker disconnection.")
            break


def track_optical(settings, origin):
    stop = False

    tracker = NDITracker(settings)
    tracker.start_tracking()

    filename = f"vicra_pose_data_{time.time_ns()}.csv"
    filepath = os.path.join("..", "..", "result", filename)

    with open(filepath, 'w', newline=None) as file:
        writer = csv.writer(file)
        writer.writerow(
            ['timestamp', 'mag_x0', 'mag_y0', 'mag_z0', 'mag_mx0', 'mag_my0', 'mag_mz0', 'mag_qx0', 'mag_qy0',
             'mag_qz0', 'mag_qw0'])

        try:
            while True:
                try:
                    port_handles, timestamps, framenumbers, tracking, quality = tracker.get_frame()

                    TM = np.dot(np.linalg.inv(origin), np.dot(np.linalg.inv(tracking[0]), tracking[1]))
                    Q = Rotation.from_matrix(TM[:3, :3]).as_quat(canonical=True, scalar_first=True)
                    D = TM[:3, 2]  # get direction vector when board is [0, 0, 1]
                    T = TM[:3, 3]

                    print("Transformation Matrix (TM):\n", TM)
                    print("Translation (T):", T, "mm")
                    print("Quaternion (Q):", Q)
                    print("Direction Vector (D):", D)
                    print("Timestamps:", np.array(timestamps))

                    writer.writerow([int(np.mean(np.array(timestamps) * 1e9)), *(T * 1e-3), *D, *Q])

                    # from quat and translation to transformation matrix
                    TM = np.eye(4)
                    TM[:3, :3] = Rotation.from_quat(Q, scalar_first=True).as_matrix()
                    TM[:3, 3] = T
                    print("Transformation Matrix (TM):\n", TM)

                except OSError as os_err:
                    print("OSError during get_frame. Possible tracker disconnection.")
                    break

        except KeyboardInterrupt:
            print("KeyboardInterrupt received. Exiting gracefully.")
        finally:
            print("Tracker shut down.")


if __name__ == "__main__":
    origin = np.array([[1, 0, 0, 18.25],
                       [0, 1, 0, 13.25],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

    settings = {
        "tracker type": "polaris",
        "romfiles": ["magnetometer_tool.rom", "magnet_tool.rom"],
        "serial port": "/dev/cu.usbserial-14420"
    }

    track_optical(settings, origin)
