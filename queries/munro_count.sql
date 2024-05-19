select M.Name, W.WALK_ID
FROM TABLE(SDO_JOIN('WALKS', 'GEOM', 
                    'MUNROS', 'GEOM',
                    'mask=ANYINTERACT'))C,
   WALKS W, 
    MUNROS M
WHERE c.rowid1 = W.rowid AND c.rowid2 = M.rowid
--JOIN WALKS ON SDO_RELATE(M.GEOM, W.GEOM, 'MASK=anyinteract') = 'True'
GROUP BY M.NAME, W.WALK_ID
HAVING COUNT(M.MUNRO_ID) = 2    
/