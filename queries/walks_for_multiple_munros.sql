SELECT mun.name, mun.munro_id
FROM s2559258.munros mun
WHERE (
    SELECT COUNT(DISTINCT wlk.walk_id)
    FROM s2559258.walks wlk
    WHERE SDO_GEOM.SDO_INTERSECTION(wlk.geom, mun.geom, 0.05) IS NOT NULL
) >= 2/
