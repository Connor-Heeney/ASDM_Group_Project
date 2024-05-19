import cx_Oracle
from flask import Flask, jsonify, make_response, request
import matplotlib.pyplot as plt
from shapely import wkt
from shapely.wkt import loads
from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
import csv
import pandas as pd
import numpy as np
from pyproj import Proj, transform
from matplotlib import pyplot as plt


def reprojectData(lon, lat, outEPSG):
    # set projections
    inProj = Proj("epsg:4326")
    outProj = Proj("epsg:" + str(outEPSG))
    # reproject data
    x, y = transform(inProj, outProj, lat, lon)
    return (x, y)


# Oracle Spatial connection details
username = "s2559258"
password = "Av13m0r32023"
dsn = "geoslearn"


# Connect to the Oracle database
connection = cx_Oracle.connect(username, password, dsn)
cursor = connection.cursor()
# Define your spatial query
munro_id = input()


query = f"""SELECT SDO_UTIL.TO_WKTGEOMETRY(wlk.geom) as walk_geom, SDO_UTIL.TO_WKTGEOMETRY(mun.geom) AS munro_geom , wlk.walk_id
FROM s2559258.walks wlk, s2559258.munros mun
WHERE EXISTS (SELECT 1 FROM s2559258.munros mun WHERE mun.munro_id = {munro_id}
AND SDO_GEOM.SDO_INTERSECTION(wlk.geom, mun.geom, 0.5) IS NOT NULL)"""


'''query = """SELECT /*+ INDEX(m munro_spatial_idx) */
    SDO_UTIL.TO_WKTGEOMETRY(M.GEOM) AS geom, M.MUNRO_ID, M.NAME , SDO_NN_DISTANCE(10) DIST
    FROM s2559258.MUNROS M  
    WHERE SDO_NN(m.geom,  sdo_geometry(2001, 8307, 
    sdo_point_type(10,7,NULL), NULL,  NULL),
    'sdo_num_res=5', 10) = 'TRUE' 
    ORDER BY DIST"""
'''
# Execute the query
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()
# Close the cursor and connection


# Plot the spatial data on a map
# fig, ax = plt.subplots()

xcoord = []
ycoord = []



munro_x = []
munro_y = []
for result in results:
    print(result)
    wkt_walks = loads(str(result[0]))
    wkt_munro = loads(str(result[1]))
    x, y = wkt_munro.xy
    xi, yi = wkt_walks.xy
    lon, lat = reprojectData(x, y, 27700)
    loni, lati = reprojectData(xi, yi, 27700)
    plt.plot(loni,lati)
    munro_x.append(lon)
    munro_y.append(lat)
plt.scatter(munro_x, munro_y)



# gdf.plot()
# ax.set_aspect("equal", adjustable="datalim")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.title("Spatial Query Results")

# Show the map
plt.show()

cursor.close()
connection.close()
