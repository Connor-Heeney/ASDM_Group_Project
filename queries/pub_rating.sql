CREATE TABLE pub_bufs UNRECOVERABLE AS
    SELECT SDO_GEOM.SDO_BUFFER(A.GEOM, B.DIMINFO, 5000) as GEOM
    FROM PUBS A, USER_SDO_GEOM_METADATA B
    WHERE TABLE_NAME='PUBS' AND COLUMN_NAME='GEOM'
/
CREATE INDEX pb_spatial_idx
   ON pub_bufs(GEOM)
   INDEXTYPE IS MDSYS.SPATIAL_INDEX_V2

/
SELECT distinct /*+ ordered */ W.WALK_ID, P.NAME, P.RATING
FROM TABLE(SDO_JOIN('WALKS', 'GEOM', 'PUB_BUFS', 'GEOM','mask=ANYINTERACT')) c,
            (SDO_JOIN('PUBS', 'GEOM', 'PUB_BUFS', 'GEOM','mask=ANYINTERACT')) d,
        WALKS W, PUBS P, pub_bufs B
  WHERE c.rowid1 = w.rowid AND c.rowid2 = B.rowid
  and d.rowid1 = P.rowid AND d.rowid2 = B.rowid
  AND P.rating = 5

/