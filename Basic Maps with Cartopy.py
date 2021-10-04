import matplotlib.pyplot as plt

import cartopy.crs as ccrs

import cartopy.feature as cfeat

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())


ax.coastlines()

plt.show()