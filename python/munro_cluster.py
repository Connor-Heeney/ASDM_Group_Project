# import modules
import cx_Oracle
import matplotlib.pyplot as plt
from shapely import wkt
from shapely.wkt import loads
from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
import pandas as pd
import numpy as np
from pyproj import Proj, transform
from matplotlib import pyplot as plt
import cartopy
from cartopy.io.img_tiles import OSM


def reprojectData(lon, lat, outEPSG):
    # set projections
    inProj = Proj("epsg:4326")
    outProj = Proj("epsg:" + str(outEPSG))
    # reproject data
    x, y = transform(inProj, outProj, lat, lon)
    return (x, y)


def return_geoms(table):
    # Oracle Spatial connection details
    username = "s2559258"
    password = "Av13m0r32023"
    dsn = "geoslearn"

    # Connect to the Oracle database
    connection = cx_Oracle.connect(username, password, dsn)
    cursor = connection.cursor()
    # Define your spatial query
    query = (
        f""" select name ,SDO_UTIL.TO_WKTGEOMETRY(geom) as geom from s2559258.{table}"""
    )

    # Execute the query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()
    return results


def nn_cluster():
    # Oracle Spatial connection details
    username = "s2559258"
    password = "Av13m0r32023"
    dsn = "geoslearn"

    # Connect to the Oracle database
    connection = cx_Oracle.connect(username, password, dsn)
    cursor = connection.cursor()
    # Define your spatial query
    query = f""" SELECT /*+ INDEX(m munro_spatial_idx) */
    M.MUNRO_ID, M.NAME , SDO_NN_DISTANCE(10) DIST, M.GEOM
    FROM s2559258.MUNROS M  
    WHERE SDO_NN(m.geom,  sdo_geometry(2001, 8307, 
      sdo_point_type(10,7,NULL), NULL,  NULL),
      'sdo_num_res=5', 10) = 'TRUE' 
    ORDER BY DIST"""

    # Execute the query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()
    return results


if __name__ == "__main__":

    # create a new pyplot figure
    plt.figure()
    # apply the OSGB coordinate system to the figure, making it a map
    geo_axes = plt.axes(projection=cartopy.crs.OSGB())
    # Set the area the map covers
    geo_axes.set_extent((240000, 355000, 750000, 840200), crs=cartopy.crs.OSGB())
    # Import OSM imagery and add it to the map
    imagery = OSM()
    geo_axes.add_image(imagery, 9)
    geo_axes.set_xticks(range(240000, 355000, 20000))
    geo_axes.set_yticks(range(750000, 840200, 20000))

    # Plot Munros
    all_munros = return_geoms("munros")
    allmunro_x = []
    allmunro_y = []
    for allmunro in all_munros:
        wkt_munro = loads(str(allmunro[-1]))
        x, y = wkt_munro.xy
        lon, lat = reprojectData(x, y, 27700)
        allmunro_x.append(lon)
        allmunro_y.append(lat)
    geo_axes.scatter(allmunro_x, allmunro_y, color="grey", alpha=0.5)

    munro_x = []
    munro_y = []
    munro_geoms = nn_cluster()
    for allmunro in all_munros:
        iy = allmunro[0]
        for munro in munro_geoms:
            xi = munro[1]
            if xi == iy:
                wkt_munro = loads(str(allmunro[-1]))
                x, y = wkt_munro.xy
                lon, lat = reprojectData(x, y, 27700)
                munro_x.append(lon)
                munro_y.append(lat)

    geo_axes.scatter(munro_x, munro_y, c="red", marker="^")
    print(xi)
    geo_axes.set_title("Cluster of 5 munros")

    regions = return_geoms("regions")
    for result in regions:
        shapely_poly = loads(str(result[-1]))
        x, y = shapely_poly.exterior.xy
        lon, lat = reprojectData(x, y, 27700)
        plt.plot(lon, lat, color="grey", alpha=0.5)

    plt.show()
