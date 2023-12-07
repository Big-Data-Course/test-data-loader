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

    '''print("Create cluster")

    open_cluster_c = SkyCoord(
        ra=results['ra'],
        dec=results['dec'],
        unit='deg')
    
    print("Cluser is ready")

    open_cluster_gal = open_cluster_c.transform_to(Galactic())

    print("Projection is ready")

    fig, ax = coordinates_aitoff_plot(open_cluster_gal)
    ax.set_xlabel('Galactic longitude, $l$ [deg]')
    ax.set_ylabel('Galactic latitude, $b$ [deg]')'''

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
    
    lon = results['ra']
    lat = results['dec']
    print('Lon apply...')
    lon = lon.apply(lambda x: -(x if x <= 180 else x - 360) * 0.0175)
    print('Lat apply...')
    lat = lat.apply(lambda x: x * 0.0175)
    #sph = coords.spherical
    a = ScatterDensityArtist(ax,
                             lon,
                             lat,
                             cmap=white_viridis)
    ax.add_artist(a)

    def fmt_func(x, pos):
        val = coord.Angle(-x*u.radian).wrap_at(360*u.deg).degree
        return f'${val:.0f}' + r'^{\circ}$'

    ticker = mpl.ticker.FuncFormatter(fmt_func)
    ax.xaxis.set_major_formatter(ticker)
    ax.set_xlabel('RA')
    ax.set_ylabel('DEG')
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