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


def parking():
    # Oracle Spatial connection details
    username = "s2559258"
    password = "Av13m0r32023"
    dsn = "geoslearn"

    # Connect to the Oracle database
    connection = cx_Oracle.connect(username, password, dsn)
    cursor = connection.cursor()
    # Define your spatial query
    query = f"""SELECT distinct /*+ ordered */ W.WALK_ID, P.NAME, P.AREA
    FROM TABLE(SDO_JOIN('WALKS', 'GEOM', 'parking_bufs', 'GEOM','mask=ANYINTERACT')) c,
                (SDO_JOIN('PARKING', 'GEOM', 'parking_bufs', 'GEOM','mask=ANYINTERACT')) d,
            s2559258.WALKS W, s2559258.Parking P, s2559258.parking_bufs B
    WHERE c.rowid1 = w.rowid AND c.rowid2 = B.rowid
    and d.rowid1 = P.rowid AND d.rowid2 = B.rowid
    AND P.AREA > (SELECT AVG(AREA) FROM s2559258.PARKING)"""

    # Execute the query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()
    return results


def get_geom(table, condition):
    # Oracle Spatial connection details
    username = "s2559258"
    password = "Av13m0r32023"
    dsn = "geoslearn"

    # Connect to the Oracle database
    connection = cx_Oracle.connect(username, password, dsn)
    cursor = connection.cursor()
    # Define your spatial query
    query = f""" select SDO_UTIL.TO_WKTGEOMETRY(geom) as geom from s2559258.{table} where {condition}"""

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
    all = return_geoms("parking")
    allx = []
    ally = []
    for al in all:
        # print(allmunro[-1])
        wkt_all = loads(str(al[-1]))
        x, y = wkt_all.xy
        lon, lat = reprojectData(x, y, 27700)
        allx.append(lon)
        ally.append(lat)
    geo_axes.scatter(allx, ally)

    regions = return_geoms("regions")
    for result in regions:
        shapely_poly = loads(str(result[-1]))
        x, y = shapely_poly.exterior.xy
        lon, lat = reprojectData(x, y, 27700)
        plt.plot(lon, lat, color="grey", alpha=0.5)

    # geo_axes.scatter(park_x, park_y)
    # print(park)

    parking1 = parking()
    park_x = []
    park_y = []
    walk_x = []
    walk_y = []
    for park in parking1:
        park_subsets = get_geom("PARKING", f"AREA = {park[-1]}")
        for set in park_subsets:
            wkt_set = loads(str(set[0]))
            x, y = wkt_set.xy
            lon, lat = reprojectData(x, y, 27700)
            park_x.append(lon)
            park_y.append(lat)

        walk_subsets = get_geom("WALKS", f"WALK_ID = {park[0]}")
        for walk in walk_subsets:
            # print(walk[0])
            walk_set = loads(str(walk[0]))
            xi, yi = walk_set.xy
            loni, lati = reprojectData(xi, yi, 27700)
            geo_axes.plot(loni, lati, color="red")
    geo_axes.scatter(park_x, park_y, color="red")

    plt.title(f"Nearest walks to {park[1]}")

    plt.show()
