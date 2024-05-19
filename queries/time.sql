SELECT
    w.WALK_ID,
    (m.HEIGHT/10 + w.LENGTH*15) /60 AS time_taken_hours, w.geom
FROM
    s2559258.WALKS w
JOIN
    S2559258.MUNROS m ON SDO_CONTAINS(w.GEOM, m.GEOM) = 'TRUE';