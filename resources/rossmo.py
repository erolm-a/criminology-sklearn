#!/usr/bin/python3
# Copyright by Enrico "erolm_a" Trombetta et al.

import numpy as np
import matplotlib.pyplot as plt
#import geotiler
#from mpl_toolkits.basemap import Basemap

# Places I've been frequently

dataset = np.array([(38.119888, 13.358329), # Poste, Piazza G. Verdi
                       (38.120271, 13.361493), # Poste, Via Roma
                       (38.122011, 13.354435), # Poste, Via Mariano Stabile
                       (38.123881, 13.350402), # Poste, Via Brunetto Latini
                       (38.135180, 13.354118), # Our School :)
                       (38.133512, 13.344011) # Drago, Japanese Restaurant
                   ])
    

longitudes = dataset[:,0]
latitudes = dataset[:,1]

# impostazioni per Matplotlib

origin = 'lower'
#origin = 'upper'

width = 300
height = 300

x = np.linspace(38.11, 38.14, width)
y = np.linspace(13.34, 13.37, height)

center = np.average(x), np.average(y)
X, Y = np.meshgrid(x, y)

def distance(x, X): return np.linalg.norm(np.array(x)-np.array(X))

def rossmo_model(b, f, g, k):
    Z = np.zeros((width, height))
    for i in range(len(x)):
        for j in range(len(y)):
            lon, lat = x[i], y[j]
            for d in dataset:
                dist = distance(d, (lon, lat))
                Z[i][j] += ((dist > b) / dist**f) + ((dist<=b)*(b**(g-f)) / np.abs(2*b - dist))**g
            Z[i][j] *= k
    return Z

Z = rossmo_model(0.0005, 0.5, 0.4, 0.008)

print("Rossmo predictions computed")

bbox = 13.34, 38.11, 13.37, 38.14

# fig = plt.figure(figsize=(10, 10))

# download background map using OpenStreetMap
#mm = geotiler.Map(extent=bbox, zoom=13)
#img = geotiler.render_map(mm)

# create basemap
#map = Basemap(
#    llcrnrlon=bbox[0], llcrnrlat=bbox[1],
#    urcrnrlon=bbox[2], urcrnrlat=bbox[3],
#    projection='merc'
#)

#map.imshow(img, interpolation='lanczos', origin='upper')

# draw the probability layers
#ax, ay = map(X, Y)
CS = plt.contourf(X, Y, Z, 10,
                  #[-1, -0.1, 0, 0.1],
#                  alpha=0,
                  cmap=plt.cm.RdYlGn_r,
                  origin=origin)

# Draw the dataset
plt.plot(longitudes, latitudes, 'b^')
# plt.scatter(x, y, c='blue', edgecolor='none', s=10, alpha=0.9, marker='^')

plt.title('Rossmo model for erolm_a')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Make a colorbar for the ContourSet returned by the contourf call.

cbar = plt.colorbar(CS)
#ap.ax.set_ylabel('Residence probability')

plt.show()