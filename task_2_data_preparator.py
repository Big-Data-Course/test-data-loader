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
        ascii.write(data["random_index", "pmra", "pmdec"], fout, overwrite=True)
        print(filename)

if __name__ == "__main__":
    if not os.path.exists("task_2_data"):
        os.makedirs("task_2_data")
    prepare_data("task_2_data")