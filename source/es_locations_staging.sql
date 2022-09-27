CREATE TABLE `locations` (
  `location_id` int(10) unsigned NOT NULL,
  `city` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `country` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `county` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state_fips` varchar(2) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `county_fips` varchar(6) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `num_assignees` int(10) unsigned NOT NULL,
  `num_inventors` int(10) unsigned NOT NULL,
  `num_patents` int(10) unsigned NOT NULL,
  `persistent_location_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`location_id`),
  KEY `ix_location_county` (`county`),
  KEY `ix_location_state_fips` (`state_fips`),
  KEY `ix_location_county_fips` (`county_fips`),
  KEY `ix_location_num_inventors` (`num_inventors`),
  KEY `ix_location_city` (`city`),
  KEY `ix_location_country` (`country`),
  KEY `ix_location_persistent_location_id` (`persistent_location_id`),
  KEY `ix_location_state` (`state`),
  KEY `ix_location_num_patents` (`num_patents`),
  KEY `ix_location_num_assignees` (`num_assignees`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;truncate table elastic_staging.locations;
insert into elastic_staging.locations( location_id, city, state, country, county, state_fips, county_fips, latitude
                                     , longitude, num_assignees, num_inventors, num_patents, persistent_location_id)
select distinct
    location_id
  , city
  , state
  , country
  , county
  , state_fips
  , county_fips
  , latitude
  , longitude
  , num_assignees
  , num_inventors
  , num_patents
  , timl.old_location_id
from
    PatentsView_20211230.location l
        join PatentsView_20211230.temp_id_mapping_location timl on timl.new_location_id = l.location_id
-- join PatentsView_20211230.temp_id_mapping_location timl
--  on timl.old_location_id_transformed = l.persistent_location_id
#         left join elastic_staging.patent_inventor pi on pi.persistent_location_id = timl.old_location_id
#         left join elastic_staging.patent_assignee pa on pi.persistent_location_id = timl.old_location_id
#         left join elastic_staging.assignees a on a.lastknown_persistent_location_id = timl.old_location_id
#         left join elastic_staging.inventors i on i.lastknown_persistent_location_id = timl.old_location_id
# where
#      pi.persistent_location_id is not null
#   or pa.persistent_location_id is not null
#   or i.lastknown_persistent_location_id is not null
#   or a.lastknown_persistent_location_id is not null;

select
    location_id
  , city
  , state
  , country
  , county
  , state_fips
  , county_fips
  , latitude
  , longitude
  , num_assignees
  , num_inventors
  , num_patents
  , persistent_location_id
from
    elastic_staging.locations l