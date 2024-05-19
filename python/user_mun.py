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


def user_in_m(munro_id):
    # Oracle Spatial connection details
    username = "s2559258"
    password = "Av13m0r32023"
    dsn = "geoslearn"

    # Connect to the Oracle database
    connection = cx_Oracle.connect(username, password, dsn)
    cursor = connection.cursor()
    # Define your spatial query

    query = f"""SELECT SDO_UTIL.TO_WKTGEOMETRY(wlk.geom) as walk_geom, SDO_UTIL.TO_WKTGEOMETRY(mun.geom) AS munro_geom , wlk.walk_id, mun.munro_Id, mun.name
    FROM s2559258.walks wlk, s2559258.munros mun
    WHERE EXISTS (SELECT 1 FROM s2559258.munros mun WHERE mun.munro_id = {munro_id}
    AND SDO_GEOM.SDO_INTERSECTION(wlk.geom, mun.geom, 0.5) IS NOT NULL)
    AND mun.munro_id = {munro_id}"""
    # Execute the query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()
    return results


if __name__ == "__main__":
    munro_id = input("Select MUNRO_ID:")
    # Plot the spatial data on a map
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

    munro_x = []
    munro_y = []

    results = user_in_m(munro_id)
    for result in results:
        wkt_walks = loads(str(result[0]))
        wkt_munro = loads(str(result[1]))
        x, y = wkt_munro.xy
        xi, yi = wkt_walks.xy
        lon, lat = reprojectData(x, y, 27700)
        loni, lati = reprojectData(xi, yi, 27700)
        geo_axes.plot(loni, lati, color="red")
        munro_x.append(lon)
        munro_y.append(lat)
    geo_axes.scatter(munro_x, munro_y, color="red", marker="^")

    plt.title(f"Nearest walk to {result[-1]}")
    plt.savefig("python/figures/Nearestto.png")
    plt.clf()
    # plt.show()
