LOAD DATA
INFILE walk_data.csv
INTO TABLE s2559258.walks
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(WALK_ID, LENGTH, GEOM, POPULARITY, DIFFICULTY)
