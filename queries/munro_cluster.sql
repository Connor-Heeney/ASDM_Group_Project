SELECT /*+ INDEX(m munro_spatial_idx) */
M.MUNRO_ID, M.NAME , SDO_NN_DISTANCE(10) DIST, M.GEOM
   FROM s2559258.MUNROS M  
   WHERE SDO_NN(m.geom,  sdo_geometry(2001, 8307, 
      sdo_point_type(10,7,NULL), NULL,  NULL),
      'sdo_num_res=5', 10) = 'TRUE' 
    ORDER BY DIST
/