BREAK ON starting_point

SELECT m1.munro_id AS starting_point, m2.munro_id AS surrounding_munros, m1.geom
FROM s2559258.munros m1, s2559258.munros m2
WHERE m1.munro_id <> m2.munro_id AND m1.munro_id = &user_munro_id
ORDER BY SDO_GEOM.SDO_DISTANCE(m1.geom, m2.geom, 0.005) ASC
FETCH FIRST &returned_rows ROWS ONLY;
