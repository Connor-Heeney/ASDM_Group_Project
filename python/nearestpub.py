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
    query = f""" select SDO_UTIL.TO_WKTGEOMETRY(geom) as geom from s2559258.{table}"""

    # Execute the query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()
    return results


def height():
    # Oracle Spatial connection details
    username = "s2559258"
    password = "Av13m0r32023"
    dsn = "geoslearn"

    # Connect to the Oracle database
    connection = cx_Oracle.connect(username, password, dsn)
    cursor = connection.cursor()
    # Define your spatial query
    query = f""" WITH StartingPoints AS (
    SELECT
        w.WALK_ID,
        V.X AS START_X,
        V.Y AS START_Y,
        ROW_NUMBER() OVER (PARTITION BY w.WALK_ID ORDER BY V.ID) AS RN
    FROM
        S2559258.WALKS w,
        TABLE(SDO_UTIL.GETVERTICES(w.GEOM)) V
),
NearestPubs AS (
    SELECT
        sp.WALK_ID,
        sp.START_X,
        sp.START_Y,
        pb.PUB,
        SDO_GEOM.SDO_DISTANCE(
            SDO_GEOMETRY(2001, 8307, SDO_POINT_TYPE(sp.START_X, sp.START_Y, NULL), NULL, NULL),
            pb.GEOM,
            0.005
        ) AS DISTANCE,
        ROW_NUMBER() OVER (PARTITION BY sp.WALK_ID ORDER BY SDO_GEOM.SDO_DISTANCE(
            SDO_GEOMETRY(2001, 8307, SDO_POINT_TYPE(sp.START_X, sp.START_Y, NULL), NULL, NULL),
            pb.GEOM,
            0.005
        )) AS PUB_RANK
    FROM
        StartingPoints sp
    CROSS JOIN
        S2559258.PUBS pb
    WHERE
        sp.RN = 1
)
SELECT
    np.WALK_ID,
    np.START_X,
    np.START_Y,
    np.PUB,
    np.DISTANCE,
    w.GEOM
FROM
    NearestPubs np
JOIN
    S2559258.WALKS w ON np.WALK_ID = w.WALK_ID
WHERE
    np.PUB_RANK = 1

"""

    # Execute the query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()
    return results


def height_geom():
    # Oracle Spatial connection details
    username = "s2559258"
    password = "Av13m0r32023"
    dsn = "geoslearn"

    # Connect to the Oracle database
    connection = cx_Oracle.connect(username, password, dsn)
    cursor = connection.cursor()
    # Define your spatial query
    query = f""" select SDO_UTIL.TO_WKTGEOMETRY(geom) as geom from s2559258.MUNROS"""

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
        # print(allmunro[-1])
        wkt_munro = loads(str(allmunro[-1]))
        x, y = wkt_munro.xy
        lon, lat = reprojectData(x, y, 27700)
        allmunro_x.append(lon)
        allmunro_y.append(lat)
    geo_axes.scatter(allmunro_x, allmunro_y, marker="^", color="grey", alpha=0.5)

    regions = return_geoms("regions")
    for result in regions:
        shapely_poly = loads(str(result[-1]))
        x, y = shapely_poly.exterior.xy
        lon, lat = reprojectData(x, y, 27700)
        # plt.plot(lon, lat, color="grey", alpha=0.5)

    heights = height()
    reproj_x = []
    reproj_y = []

    for height2 in heights:
        # Extract the coordinates
        lon, lat = height2[1], height2[2]

        # Reproject the coordinates
        reproj_lon, reproj_lat = reprojectData(lon, lat, 27700)

        # Append the reprojected coordinates to the lists
        reproj_x.append(reproj_lon)
        reproj_y.append(reproj_lat)

    # Plot the reprojected coordinates
    plt.scatter(reproj_x, reproj_y, color="red")

# Show the plot
plt.title("Walks which start and end near pubs")
plt.show()
