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

# Define your spatial query
query = """
    select * from s2559258.walks
"""

# Execute the query
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()
print(results)

# Close the cursor and connection
cursor.close()
connection.close()
"""
# Plot the spatial data on a map
fig, ax = plt.subplots()

for result in results:
    # Convert Oracle Spatial WKB to Shapely geometry
    geometry = loads(bytes(result[0].read()))

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

"""
import folium
import webbrowser
import os


def mapgeo():
    m = folium.Map(location=[57.0600000, -3.6500000], zoom_start=12)
    folium.Marker([57.0600000, -3.6500000], popup="jaingjiang").add_to(m)
    m.save("my_map.html")
    webbrowser.open("file://" + os.path.realpath("my_map.html"))  # 打开生成的 HTML 文件
    return


if __name__ == "__main__":
    mapgeo()
