import pandas as pd
from sys import argv
import os
import numpy as np
import mpl_scatter_density # adds projection='scatter_density'
from matplotlib.colors import LinearSegmentedColormap
from astropy.visualization.mpl_normalize import ImageNormalize
from astropy.visualization import PowerStretch
import matplotlib.pyplot as plt

data_dir = "loaded_data"

def task_load_data(dir, indFrom = -1, indTo = -1):
    li = []
    for i in range(indFrom, indTo):
        print(i)
        filename = dir + '/result_3_' + str(i)
        result = pd.read_csv(filename, sep=' ', header = 0)
        li.append(result)
    frame = pd.concat(li, axis = 0, ignore_index=True)
    return frame

def task_6(results):
    # "Viridis-like" colormap with white background
    white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
        (0, '#ffffff'),
        (1e-20, '#440053'),
        (0.05, '#404388'),
        (0.2, '#2a788e'),
        (0.4, '#21a784'),
        (0.6, '#78d151'),
        (1, '#fde624'),
    ], N=256)

    norm = ImageNormalize(vmin=1e-10, stretch=PowerStretch(0.5))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    ax.set_xlabel(r'$G_{BP}-G_{RP}$')
    ax.set_ylabel(r'$M_{G}$')

    res = results.query("dist < 100 or (dist > 100 and azero_gspphot < 0.015 * 3.1) or azero_gspphot == '' or dist == ''")

    print (res.size)

    x = res['bp_rp']
    y = res['mg']
    density = ax.scatter_density(x, y, cmap=white_viridis, norm=norm)
    ax.invert_yaxis()
    fig.colorbar(density, label='')
    plt.show()

    '''res = results.query("bp_rp < 1 and mg > 6")

    print (res.size)

    x = res['bp_rp']
    y = res['mg']
    density = ax.scatter_density(x, y, cmap=white_viridis, norm=norm)
    ax.invert_yaxis()
    fig.colorbar(density, label='')
    plt.show()'''

if __name__ == "__main__":
    results = []
    path = "result"
    if not os.path.exists(path):
        os.makedirs(path)
    if len(argv) != 3:
        results = task_load_data(path)
    else:
        results = task_load_data(path, int(argv[1]), int(argv[2]))
    print (results.size)
    task_6(results)
    
    