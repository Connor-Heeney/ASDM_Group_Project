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
    munros = return_geoms("munros")
    munro_x = []
    munro_y = []
    for munro in munros:
        print(munro[-1])
        wkt_munro = loads(str(munro[-1]))
        x, y = wkt_munro.xy
        lon, lat = reprojectData(x, y, 27700)
        munro_x.append(lon)
        munro_y.append(lat)
    geo_axes.scatter(munro_x, munro_y, label="Munros", marker="^", color="dodgerblue")

    pubs = return_geoms("pubs")
    pub_x = []
    pub_y = []
    for pub in pubs:
        wkt_pub = loads(str(pub[-1]))
        x, y = wkt_pub.xy
        lon, lat = reprojectData(x, y, 27700)
        pub_x.append(lon)
        pub_y.append(lat)
    geo_axes.scatter(pub_x, pub_y, label="Pub", color="green")

    parking = return_geoms("parking")
    park_x = []
    park_y = []
    for park in parking:
        wkt_park = loads(str(park[-1]))
        x, y = wkt_park.xy
        lon, lat = reprojectData(x, y, 27700)
        park_x.append(lon)
        park_y.append(lat)
    geo_axes.scatter(park_x, park_y, label="Parking", marker="*", color="black")

    regions = return_geoms("regions")
    for result in regions:
        shapely_poly = loads(str(result[-1]))
        x, y = shapely_poly.exterior.xy
        lon, lat = reprojectData(x, y, 27700)
        geo_axes.plot(lon, lat, label="Region", color="sienna")

    walks = return_geoms("walks")
    for walk in walks:
        shapely_walk = loads(str(walk[-1]))
        x, y = shapely_walk.xy
        lon, lat = reprojectData(x, y, 27700)
        geo_axes.plot(lon, lat, color="indigo")

    geo_axes.legend()
    plt.title("All spatial data")
    plt.savefig("python/figures/all.png")
    plt.clf()
    # plt.show()
