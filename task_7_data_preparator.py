from astropy.io import ascii
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
        print(fin)
        print(fout)
        print("read start")
        data = ascii.read(fin)
        print("read finish")
        ascii.write(data["random_index", "ra_error", "pmra_error", "dec_error", "pmdec_error", "parallax_error", "dist"], fout, overwrite=True)
        print(filename)

if __name__ == "__main__":
    if not os.path.exists("task_7_data"):
        os.makedirs("task_7_data")
    if len(argv) != 3:
        prepare_data("task_7_data")
    else:
        prepare_data("task_7_data", int(argv[1]), int(argv[2]))