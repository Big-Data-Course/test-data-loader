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
        ascii.write(data["random_index", "phot_g_mean_mag", "phot_rp_mean_mag", "phot_bp_mean_mag"], fout, overwrite=True)
        print(filename)

if __name__ == "__main__":
    if not os.path.exists("task_4_data"):
        os.makedirs("task_4_data")
    prepare_data("task_4_data")