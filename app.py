
from tools.diy_logger import Logger

import datetime


if __name__ == '__main__':
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = [1, 3, 2]

    item = [(x, y, z) for x, y, z in (a, b, c)]

    print(item)

