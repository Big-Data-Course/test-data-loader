import pandas as pd
from sys import argv
import os
import numpy as np
import matplotlib as mpl
import mpl_scatter_density # adds projection='scatter_density'
from mpl_scatter_density import ScatterDensityArtist
from matplotlib.colors import LinearSegmentedColormap
from astropy.visualization.mpl_normalize import ImageNormalize
from astropy.visualization import PowerStretch
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import (SkyCoord, Distance, Galactic, 
                                 EarthLocation, AltAz)
import astropy.coordinates as coord
import math

def task_load_data(dir, indFrom = -1, indTo = -1):
    li = []
    for i in range(indFrom, indTo):
        print(i)
        filename = dir + '/data_dr3_' + str(i)
        result = pd.read_csv(filename, sep=' ', header = 0)
        li.append(result)
    frame = pd.concat(li, axis = 0, ignore_index=True)
    return frame

def task_6(results):
    norm = ImageNormalize(vmin=1e-10, stretch=PowerStretch(0.5))

    white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
        (0, '#ffffff'),
        (1e-20, '#440053'),
        (0.05, '#404388'),
        (0.2, '#2a788e'),
        (0.4, '#21a784'),
        (0.6, '#78d151'),
        (1, '#fde624'),
    ], N=256)

    fig, ax = plt.subplots(figsize=(15, 8),
                           subplot_kw=dict(projection="aitoff"))
    
    radian = np.pi / 180
    print('Lon apply...')
    results['ra'] = results['ra'].apply(lambda x: (x if x <= 180 else x - 360) * radian)
    print('Lat apply...')
    results['dec'] = results['dec'].apply(lambda x: x * radian)

    '''def to_galactic(row):
        lon = row['ra']
        lat = row['dec']
        row['ra'] = math.asin(math.sin(lon) * math.sin(27.12825 * radian) + math.cos(lon) * math.cos(27.12825 * radian) * math.cos(lat - 192.85948 * radian))
        row['dec'] = -math.asin((math.cos(lon) * math.sin(lat - 192.85948 * radian)) / math.cos(row['ra'])) + 122.93192 * radian
        return row

    print('To galactic...')
    results = results.apply(to_galactic, axis=1)'''

    print('To numpy...')
    alpha = results['ra'].to_numpy()
    print('lot ready')
    delta = results['dec'].to_numpy()
    print('lat ready')

    b = np.arcsin(np.sin(delta) * np.sin(27.12825 * radian) + np.cos(delta) * np.cos(27.12825 * radian) * np.cos(alpha - 192.85948 * radian))
    cosll = (np.sin(delta) * np.cos(27.12825 * radian) - np.cos(delta) * np.sin(27.12825 * radian) * np.cos(alpha - 192.85948 * radian)) / np.cos(b)
    sinll = (np.cos(delta) * np.sin(alpha - 192.85948 * radian)) / np.cos(b)
    def lformula (cosll, sinll):
        return (np.arcsin(sinll) if cosll > 0 else np.pi - np.arcsin(sinll)) * -1 + 122.93192 * radian
    lvectorizer = np.vectorize(lformula)
    l = lvectorizer(cosll, sinll)
    normilize = np.vectorize(lambda x: -x if x <= np.pi else -x + np.pi * 2)
    l = normilize(l)

    a = ScatterDensityArtist(ax,
                             l,
                             b,
                             cmap=white_viridis
                             )
    ax.add_artist(a)

    def fmt_func(x, pos):
        val = coord.Angle(-x*u.radian).wrap_at(360*u.deg).degree
        return f'${val:.0f}' + r'^{\circ}$'

    ticker = mpl.ticker.FuncFormatter(fmt_func)
    ax.xaxis.set_major_formatter(ticker)
    ax.set_xlabel('Galactic longitude, $l$ [deg]')
    ax.set_ylabel('Galactic latitude, $b$ [deg]')
    ax.grid()
        
    #density = ax.scatter_density(x, y, cmap=white_viridis, norm=norm)
    #ax.invert_yaxis()
    #fig.colorbar(density, label='')
    plt.savefig("Figure_2_full_projection.png", dpi=500)
    plt.show()

if __name__ == "__main__":
    results = []
    path = "task_1_data"
    if not os.path.exists(path):
        os.makedirs(path)
    if len(argv) != 3:
        results = task_load_data(path)
    else:
        results = task_load_data(path, int(argv[1]), int(argv[2]))
    print (results.size)
    task_6(results)