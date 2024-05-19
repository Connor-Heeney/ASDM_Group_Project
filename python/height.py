# import modules
import cx_Oracle
import matplotlib.pyplot as plt
from shapely.wkt import loads
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
    query = f""" SELECT SUM(M.HEIGHT) HEIGHT, W.NAME
        FROM s2559258.MUNROS M, s2559258.WALKERS W
        WHERE M.WALKER = W.WALKER
        AND M.WALKER = 1
        GROUP BY W.NAME"""

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
    query = f""" select SDO_UTIL.TO_WKTGEOMETRY(geom) as geom from s2559258.MUNROS where walker = 1"""

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
    geo_axes.scatter(allmunro_x, allmunro_y, color="grey", marker="^", alpha=0.5)

    regions = return_geoms("regions")
    for result in regions:
        shapely_poly = loads(str(result[-1]))
        x, y = shapely_poly.exterior.xy
        lon, lat = reprojectData(x, y, 27700)
        plt.plot(lon, lat, color="grey", alpha=0.5)

    heights = height()
    for height in heights:
        plt.title(f" The total height is {height[0]}m by {height[1]}")
        # print(height)

    munro_geoms = height_geom()
    munro_x = []
    munro_y = []
    for munro in munro_geoms:
        print(munro[-1])
        wkt_munro = loads(str(munro[-1]))
        x, y = wkt_munro.xy
        lon, lat = reprojectData(x, y, 27700)
        munro_x.append(lon)
        munro_y.append(lat)
    geo_axes.scatter(munro_x, munro_y, color="red", marker="^")

    plt.show()
