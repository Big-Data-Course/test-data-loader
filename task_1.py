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

def task_load_data(dir, indFrom = -1, indTo = -1):
    li = []
    for i in range(indFrom, indTo):
        print(i)
        filename = dir + '/data_dr3_' + str(i)
        result = pd.read_csv(filename, sep=' ', header = 0)
        li.append(result)
    frame = pd.concat(li, axis = 0, ignore_index=True)
    return frame

def coordinates_aitoff_plot(coords):
    white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
        (0, '#ffffff'),
        (1e-20, '#440053'),
        (0.05, '#404388'),
        (0.2, '#2a788e'),
        (0.4, '#21a784'),
        (0.6, '#78d151'),
        (1, '#fde624'),
    ], N=256)

    fig, ax = plt.subplots(figsize=(10, 4), 
                           subplot_kw=dict(projection="aitoff"))
    
    sph = coords.spherical
    a = ScatterDensityArtist(ax,
                             -sph.lon.wrap_at(180*u.deg).radian,
                             sph.lat.radian,
                             cmap=white_viridis)
    ax.add_artist(a)

    def fmt_func(x, pos):
        val = coord.Angle(-x*u.radian).wrap_at(360*u.deg).degree
        return f'${val:.0f}' + r'^{\circ}$'

    ticker = mpl.ticker.FuncFormatter(fmt_func)
    ax.xaxis.set_major_formatter(ticker)

    ax.grid()
    
    #cb = fig.colorbar(cs)
    #cb.set_label('distance [pc]')
    
    return fig, ax

def task_6(results):
    norm = ImageNormalize(vmin=1e-10, stretch=PowerStretch(0.5))

    open_cluster_c = SkyCoord(
        ra=results['ra'],
        dec=results['dec'],
        unit='deg')

    open_cluster_gal = open_cluster_c.transform_to(Galactic())

    fig, ax = coordinates_aitoff_plot(open_cluster_gal)
    ax.set_xlabel('Galactic longitude, $l$ [deg]')
    ax.set_ylabel('Galactic latitude, $b$ [deg]')
    ax.set_xlabel(r'RA')
    ax.set_ylabel(r'DEC')
    
    #density = ax.scatter_density(x, y, cmap=white_viridis, norm=norm)
    #ax.invert_yaxis()
    #fig.colorbar(density, label='')
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