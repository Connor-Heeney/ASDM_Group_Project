import cx_Oracle
import matplotlib.pyplot as plt
from shapely.wkb import loads
from shapely.geometry import Point, LineString, Polygon

# Oracle Spatial connection details
username = "s2559258"
password = "Av13m0r32023"
dsn = "geoslearn"

# Connect to the Oracle database
connection = cx_Oracle.connect(username, password, dsn)
cursor = connection.cursor()

# Define your spatial query (example: select all points within a polygon)
height = """    SELECT geom_column
    FROM your_spatial_table
    WHERE SDO_RELATE(geom_column, 
                    SDO_GEOMETRY(2003, NULL, NULL, SDO_ELEM_INFO_ARRAY(1, 1003, 3), 
                                 SDO_ORDINATE_ARRAY(x1, y1, x2, y2, x3, y3)), 
                    'MASK=INSIDE') = 'TRUE'"""

# Execute the query
cursor.execute(height)

# Fetch the results
results = cursor.fetchall()

# Close the cursor and connection
cursor.close()
connection.close()

print(results)

# Plot the spatial data on a map
fig, ax = plt.subplots()

for result in results:
    # Convert Oracle Spatial WKB to Shapely geometry
    geometry = loads(result[0].read())

    # Plot the geometry based on its type
    if isinstance(geometry, Point):
        ax.plot(geometry.x, geometry.y, "ro")  # Red dot for points
    elif isinstance(geometry, LineString):
        ax.plot(*geometry.xy, "b-")  # Blue line for lines
    elif isinstance(geometry, Polygon):
        x, y = geometry.exterior.xy
        ax.fill(x, y, alpha=0.5, fc="g")  # Green filled polygon

# Customize the map appearance
ax.set_aspect("equal", adjustable="datalim")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Spatial Query Results")

# Show the map
plt.show()
