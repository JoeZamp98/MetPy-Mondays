from awips.dataaccess import DataAccessLayer
from awips.tables import vtec
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.feature import ShapelyFeature, NaturalEarthFeature
from shapely.geometry import MultiPolygon, Polygon

def warning_color(phensig):
    return vtec[phensig]['color']

