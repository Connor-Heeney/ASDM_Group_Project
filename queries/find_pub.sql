WITH StartingPoints AS (
    SELECT
        w.WALK_ID,
        V.X AS START_X,
        V.Y AS START_Y,
        ROW_NUMBER() OVER (PARTITION BY w.WALK_ID ORDER BY V.ID) AS RN
    FROM
        S2559258.WALKS w,
        TABLE(SDO_UTIL.GETVERTICES(w.GEOM)) V
),
NearestPubs AS (
    SELECT
        sp.WALK_ID,
        sp.START_X,
        sp.START_Y,
        pb.PUB,
        SDO_GEOM.SDO_DISTANCE(
            SDO_GEOMETRY(2001, 8307, SDO_POINT_TYPE(sp.START_X, sp.START_Y, NULL), NULL, NULL),
            pb.GEOM,
            0.005
        ) AS DISTANCE,
        ROW_NUMBER() OVER (PARTITION BY sp.WALK_ID ORDER BY SDO_GEOM.SDO_DISTANCE(
            SDO_GEOMETRY(2001, 8307, SDO_POINT_TYPE(sp.START_X, sp.START_Y, NULL), NULL, NULL),
            pb.GEOM,
            0.005
        )) AS PUB_RANK
    FROM
        StartingPoints sp
    CROSS JOIN
        S2559258.PUBS pb
    WHERE
        sp.RN = 1
)
SELECT
    np.WALK_ID,
    np.START_X,
    np.START_Y,
    np.PUB,
    np.DISTANCE,
    w.GEOM
FROM
    NearestPubs np
JOIN
    S2559258.WALKS w ON np.WALK_ID = w.WALK_ID
WHERE
    np.PUB_RANK = 1;


