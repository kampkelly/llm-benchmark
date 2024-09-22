import os
import hashlib
import numpy as np
from dotenv import load_dotenv

load_dotenv()

SEED_VALUE = os.getenv("SEED", "")


def generate_data_points(min_val: float, max_val: float, llm_name: str, metric: str, size: int = 1000) -> list:
    """
    Generates a list of random data points within a specified range.

    This function generates a specified number of random data points between a minimum and maximum value,
    rounded to two decimal places.

    Args:
        min_val (float): The minimum value of the range.
        max_val (float): The maximum value of the range.
        size (int, optional): The number of data points to generate. Defaults to 1000.

    Returns:
        list: A list of generated data points.
    """
    unique_string = f"{llm_name}_{metric}_{SEED_VALUE}"
    unique_seed = int(hashlib.md5(unique_string.encode()).hexdigest(), 16) % (2**32)
    np.random.seed(unique_seed)
    return np.round(np.random.uniform(min_val, max_val, size), 2).tolist()
