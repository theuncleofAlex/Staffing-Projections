import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def generate_default_wait(num_training_points):
    return np.full((num_training_points, 2), [60, 90])


def sinusoid(x, a, b, c):
    return a * np.exp(-(np.square(x - b)) * c)


def bimodal(x, sinusoid_scalars):
    return (sinusoid(x, sinusoid_scalars[0], sinusoid_scalars[1], sinusoid_scalars[2]) +
            sinusoid(x, sinusoid_scalars[3], sinusoid_scalars[4], sinusoid_scalars[5]))


def bimodal_np(index_points_, sinusoid_scalars):
    return [bimodal(x, sinusoid_scalars) for x in index_points_]


def hold_time(c, a, n):
    return c / 2 * (n / a - 1)


def generate_bimodal_data(num_training_points):
    """Generate noisy bimodal observations at a random set of points.

      Returns:
         observation_index_points, observations
    """
    sinusoid_scalars = [np.random.uniform(10, 20),
                        np.random.uniform(6, 9),
                        np.random.uniform(0.01, 0.1),
                        np.random.uniform(10, 20),
                        np.random.uniform(13, 15),
                        np.random.uniform(0.05, 0.15)]
    index_points_ = np.arange(0, 24, 24.0 / num_training_points)
    index_points_ = index_points_.astype(np.float64)
    # y = f(x) + noise
    observations_ = bimodal_np(index_points_, sinusoid_scalars)
    observations_ = observations_ + np.random.normal(loc=0,
                                                     scale=np.sqrt(sinusoid_scalars[0] * 0.25),
                                                     size=(num_training_points))
    observations_ = observations_.astype(np.float64)
    observations_[observations_ < 0] = 0
    return index_points_, observations_


def generate_bimodal_dataframe(num_points, wait_time=[]):
    wait_time_ = generate_default_wait(num_points)
    hour_, call_volume_ = generate_bimodal_data(num_points)
    data = pd.DataFrame(list(zip(hour_, call_volume_, wait_time_)))
    data.columns = ["hour", "call_volume", "wait_time"]
    return data


def generate_bimodal_sets(num_sets, num_points):
    x = [0]
    y = [0]
    for i in range(num_sets):
        new_x, new_y = generate_bimodal_data(num_points)
        x.append(new_x)
        y.append(new_y)
    x.remove(0)
    y.remove(0)
    return x, y
