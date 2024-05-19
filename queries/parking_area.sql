CREATE TABLE parking_bufs UNRECOVERABLE AS
    SELECT SDO_GEOM.SDO_BUFFER(A.GEOM, B.DIMINFO, 5000) as GEOM
    FROM s2559258.PARKING A, USER_SDO_GEOM_METADATA B
    WHERE TABLE_NAME='PARKING' AND COLUMN_NAME='GEOM'
/
CREATE INDEX parkbuf_idx
   ON parking_bufs(GEOM)
   INDEXTYPE IS MDSYS.SPATIAL_INDEX_V2

/
--NOTE: those other bits exist so just run this query
SELECT distinct /*+ ordered */ W.WALK_ID, P.NAME, P.AREA
FROM TABLE(SDO_JOIN('WALKS', 'GEOM', 'parking_bufs', 'GEOM','mask=ANYINTERACT')) c,
            (SDO_JOIN('PARKING', 'GEOM', 'parking_bufs', 'GEOM','mask=ANYINTERACT')) d,
        s2559258.WALKS W, s2559258.Parking P, s2559258.parking_bufs B
  WHERE c.rowid1 = w.rowid AND c.rowid2 = B.rowid
  and d.rowid1 = P.rowid AND d.rowid2 = B.rowid
  AND P.AREA > (SELECT AVG(AREA) FROM s2559258.PARKING)

/