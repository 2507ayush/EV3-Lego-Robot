import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import slam.common.datapoint as datapoint
from slam.map import Map

def main():
    map_instance = Map()

    sample_points = [
        datapoint.DataPoint(1, 1, path_id=1),
        datapoint.DataPoint(2, 2, path_id=1),
        datapoint.DataPoint(3, 1, path_id=1),
        datapoint.DataPoint(4, 3, path_id=1),
    ]

    for point in sample_points:
        map_instance.add_data(point)

    map_instance.redraw()

    time.sleep(10)

if __name__ == "__main__":
    main()
