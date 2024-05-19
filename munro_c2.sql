SELECT m.name AS munro_name, w.walk_id
FROM munros m
JOIN (
    SELECT walk_id
    FROM (
        SELECT w.walk_id, COUNT(m.munro_id) AS intersection_count
        FROM walks w
        JOIN munros m ON SDO_RELATE(m.geom, w.geom, 'mask=anyinteract') = 'TRUE'
        GROUP BY w.walk_id
        HAVING COUNT(m.munro_id) > 1
    ) walk_intersections
) walk_intersections ON walk_intersections.walk_id = w.walk_id
JOIN walks w where walk_intersections.walk_id = w.walk_id
/

SELECT m.name, w.walk_id
FROM munros m, walks w
JOIN (
    SELECT w.walk_id
    FROM walks w
    JOIN munros m ON SDO_RELATE(m.geom, w.geom, 'mask=anyinteract') = 'TRUE'
    GROUP BY w.walk_id
    HAVING COUNT(m.munro_id) > 1
) walk_intersections ON walk_intersections.walk_id = w.walk_id
where walk_intersections.walk_id = w.walk_id
/