SELECT wlk.walk_id, wlk.geom
FROM s2559258.walks wlk
WHERE EXISTS (
    SELECT 1
    FROM s2559258.munros mun
    WHERE mun.munro_id = &Munro_ID
    AND SDO_GEOM.SDO_INTERSECTION(wlk.geom, mun.geom, 0.5) IS NOT NULL
);