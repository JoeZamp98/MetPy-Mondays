from awips.dataaccess import DataAccessLayer
from awips.tables import vtec
from datetime import datetime
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.feature import ShapelyFeature, NaturalEarthFeature
from shapely.geometry import MultiPolygon, Polygon

def warning_color(phensig):
    return vtec[phensig]['color']

def make_map(bbox, projection=ccrs.PlateCarree()):
    fig, ax = plt.subplots(figsize=(20,12),
        subplot_kw = dict(projection=projection))
    ax.set_extent(bbox)

    gl = ax.gridlines(draw_labels = True)
    gl.top_labels = gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    
    return fig, ax

print("TEST")
DataAccessLayer.changeEDEXHost("edex-cloud.unidata.ucar.edu")
request = DataAccessLayer.newDataRequest()
request.setDatatype("warning")
request.setParameters('phensig')
times = DataAccessLayer.getAvailableTimes(request)

#Retrieve records for 50 most recent available times

response = DataAccessLayer.getGeometryData(request, times[-50:-1])
print("Using " + str(len(response))  + " records")

#Records as numpy arrays

parameters = {}

for x in request.getParameters():
    parameters[x] = np.array([])

print(parameters)

bbox = [-127, -64, 24, 49]
fig, ax = make_map(bbox=bbox)

siteids = np.array([])
periods = np.array([])
reftimes = np.array([])

for ob in response: 

    poly = ob.getGeometry()
    site = ob.getLocationName()
    pd = ob.getDataTime()
    ref = ob.getDataTime().getRefTime()

    #avoid plotting if phensig is blank (SPS)
    if ob.getString('phensig'):

        phensigString = ob.getString('phensig')

        siteids = np.append(siteids, site)
        periods = np.append(periods, pd)
        reftimes = np.append(reftimes, ref)

        for param in parameters:
            parameters[param] = np.append(parameters[param], ob.getString(param))

        if poly.geom_type == 'MultiPolygon':
            geometries = np.array([])
            geometries = np.append(geometries, MultiPolygon(poly))
            geom_count = ", " + str(len(geometries)) + " geometries"
        else:
            geometries = np.array([])
            geometries = np.append(geometries, Polygon(poly))
            geom_count=""

        for geom in geometries:
            bounds = Polygon(geom)
            intersection = bounds.intersection
            geoms = (intersection(geom)
                for geom in geometries
                if bounds.intersects(geom))