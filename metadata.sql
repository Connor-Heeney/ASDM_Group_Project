select srid from user_sdo_geom_metadata where table_name = 'PARKING';



update user_sdo_geom_metadata
set srid = 8307
where table_name = 'PARKING'

update user_sdo_geom_metadata
set srid = 8307
where table_name = 'PARKING_BUFS'