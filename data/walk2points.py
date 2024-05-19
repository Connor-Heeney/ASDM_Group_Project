import geopandas as gpd
import pandas as pd

# load shapefile into geodataframe
shapefile_path = "data/walks/walk.shp"
gdf = gpd.read_file(shapefile_path)

# extract points
# coordinates_df = gdf.geometry.apply(
#  lambda geom: pd.Series({"x": geom.xy[0].tolist(), "y": geom.xy[1].tolist()}))
coordinates_df = pd.DataFrame()
coordinates_df["coordinates"] = gdf.geometry.apply(
    lambda geom: list(zip(geom.xy[0], geom.xy[1]))
)

# combine points with original attributes
coordinates_df = pd.concat([gdf.drop("geometry", axis=1), coordinates_df], axis=1)

# save result to csv
result_csv_path = "data/outputcsv/walkpoints.csv"
coordinates_df.to_csv(result_csv_path, index=False, columns=["coordinates"])

print(f"CSV file saved to {result_csv_path}")
