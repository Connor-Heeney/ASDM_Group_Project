CREATE INDEX munro_spatial_idx
   ON munros(geom)
   INDEXTYPE IS MDSYS.SPATIAL_INDEX_V2
/
CREATE INDEX walks_spatial_idx
   ON walks(geom)
   INDEXTYPE IS MDSYS.SPATIAL_INDEX_V2
/
CREATE INDEX pubs_spatial_idx
   ON pubs(geom)
   INDEXTYPE IS MDSYS.SPATIAL_INDEX_V2
/
CREATE INDEX parking_spatial_idx
   ON parking(geom)
   INDEXTYPE IS MDSYS.SPATIAL_INDEX_V2
/