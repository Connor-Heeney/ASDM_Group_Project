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
from cartopy.io import img_tiles
import rasterio
from matplotlib.colors import ListedColormap


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


def walk_time():
    # Oracle Spatial connection details
    username = "s2559258"
    password = "Av13m0r32023"
    dsn = "geoslearn"

    # Connect to the Oracle database
    connection = cx_Oracle.connect(username, password, dsn)
    cursor = connection.cursor()
    # Define your spatial query
    query = f"""SELECT w.WALK_ID, (m.HEIGHT/10 + w.LENGTH*15) /60 AS time_taken_hours, SDO_UTIL.TO_WKTGEOMETRY(w.geom) 
    FROM s2559258.WALKS w JOIN
    S2559258.MUNROS m ON SDO_CONTAINS(w.GEOM, m.GEOM) = 'TRUE'"""

    # Execute the query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()
    return results


if __name__ == "__main__":

    # create a new pyplot figure
    fig, ax = plt.subplots(
        figsize=(8, 4), subplot_kw={"projection": cartopy.crs.PlateCarree()}
    )

    # Plot Munros
    all_munros = return_geoms("munros")
    allmunro_x = []
    allmunro_y = []
    for allmunro in all_munros:
        # print(allmunro[-1])
        wkt_munro = loads(str(allmunro[-1]))
        x, y = wkt_munro.xy
        # lon, lat = reprojectData(x, y, 27700)
        allmunro_x.append(x)
        allmunro_y.append(y)
    ax.scatter(allmunro_x, allmunro_y, color="grey", alpha=0.5, marker="^")

    regions = return_geoms("regions")
    for result in regions:
        shapely_poly = loads(str(result[-1]))
        x, y = shapely_poly.exterior.xy
        # lon, lat = reprojectData(x, y, 27700)
        ax.plot(x, y, color="grey", alpha=0.5)

    # Walk query, append results to geodataframe
    walk_times = walk_time()
    walk_df = {
        "geometry": [wkt.loads(str(walk[-1])) for walk in walk_times],
        "Time": [walk[0] for walk in walk_times],
    }
    # Set colour scale
    cmap = plt.get_cmap("RdYlGn")
    reversed_cmap = ListedColormap(cmap(np.linspace(1, 0, cmap.N)))

    ax.add_feature(
        cartopy.feature.NaturalEarthFeature(
            category="physical", scale="10m", name="land", facecolor="lightgray"
        )
    )
    # Convert dataframe to gdf
    gdf = gpd.GeoDataFrame(walk_df, geometry="geometry")
    # cbar = plt.colorbar(label="Walk Time (hrs)")
    gdf.plot(ax=ax, column="Time", cmap=reversed_cmap, legend=True)

    plt.title("Walk Time (hrs)")
    plt.show()
