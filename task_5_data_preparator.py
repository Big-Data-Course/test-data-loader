import pandas as pd
from sys import argv
import os

data_dir = "loaded_data"

def prepare_data(dir, indFrom = -1, indTo = -1):
    for filename in os.listdir(data_dir):
        ind = int(filename.split("_")[-1])
        if indFrom != indTo and (ind < indFrom or ind >= indTo):
            continue
        print(filename)
        fin = os.path.join(data_dir, filename)
        fout = os.path.join(dir, filename)
        data = pd.read_csv(fin, sep=" ")
        data[["random_index", "visibility_periods_used", "astrometric_matched_transits", "astrometric_n_obs_al", "astrometric_n_obs_ac"]].to_csv(fout, sep=" ", index=False)

if __name__ == "__main__":
    if not os.path.exists("task_5_data"):
        os.makedirs("task_5_data")
    if len(argv) != 3:
        prepare_data("task_5_data")
    else:
        prepare_data("task_5_data", int(argv[1]), int(argv[2]))