SELECT SUM(w.length) AS total_length
FROM s2559258.walks w, s2559258.regions r
WHERE SDO_RELATE(w.geom, r.geom, 'mask=inside') = 'TRUE' AND r.region_id = &region_id;