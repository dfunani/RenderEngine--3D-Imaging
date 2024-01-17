import math
import numpy as np
from typing import List

from models.vectors import Vector4


def embed(v, dim):
    ret = [v[i] if i < len(v) else 1.0 for i in range(dim)]
    return Vector4(*ret)

