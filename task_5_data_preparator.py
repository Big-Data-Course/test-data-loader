from astropy.io import ascii
import os

data_dir = "loaded_data"

def prepare_data(dir):
    for filename in os.listdir(data_dir):
        print(filename)
        fin = os.path.join(data_dir, filename)
        fout = os.path.join(dir, filename)
        print(fin)
        print(fout)
        print("read start")
        data = ascii.read(fin)
        print("read finish")
        ascii.write(data["random_index", "visibility_periods_used", "astrometric_matched_transits", "astrometric_n_obs_al", "astrometric_n_obs_ac"], fout, overwrite=True)
        print(filename)

if __name__ == "__main__":
    if not os.path.exists("task_5_data"):
        os.makedirs("task_5_data")
    prepare_data("task_5_data")