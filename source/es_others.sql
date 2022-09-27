CREATE TABLE `foreign_citations` (
  `uuid` varchar(36) COLLATE utf8mb4_unicode_ci NOT NULL,
  `patent_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `number` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `country` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sequence` int(11) DEFAULT NULL,
  `patent_zero_prefix` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `patent_id` (`patent_id`,`sequence`),
  KEY `country` (`country`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
insert into elastic_staging.foreign_citations ( uuid, patent_id, date, number, country, category, sequence
                                              , patent_zero_prefix)
select
    fc.uuid
  , fc.patent_id
  , fc.date
  , fc.number
  , fc.country
  , fc.category
  , fc.sequence
  , pe.patent_id_eight_char

from
    patent.foreigncitation fc
        join elastic_staging.patents p on p.patent_id = fc.patent_id
        join patent.patent_to_eight_char pe on pe.id = p.patent_id;


CREATE TABLE `attorneys` (
  `lawyer_id` int(10) unsigned NOT NULL,
  `name_first` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name_last` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `organization` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `num_patents` int(10) unsigned NOT NULL,
  `num_assignees` int(10) unsigned NOT NULL,
  `num_inventors` int(10) unsigned NOT NULL,
  `first_seen_date` date DEFAULT NULL,
  `last_seen_date` date DEFAULT NULL,
  `years_active` smallint(5) unsigned NOT NULL,
  `persistent_lawyer_id` varchar(36) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`lawyer_id`),
  KEY `ix_lawyer_name_last` (`name_last`),
  KEY `ix_lawyer_organization` (`organization`),
  KEY `ix_lawyer_num_patents` (`num_patents`),
  KEY `ix_lawyer_name_first` (`name_first`),
  KEY `ix_lawyer_num_assignees` (`num_assignees`),
  KEY `ix_lawyer_num_inventors` (`num_inventors`),
  KEY `ix_lawyer_first_seen_date` (`first_seen_date`),
  KEY `ix_lawyer_last_seen_date` (`last_seen_date`),
  KEY `ix_lawyer_persistent_lawyer_id` (`persistent_lawyer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
insert into elastic_staging.attorneys ( lawyer_id, name_first, name_last, organization, num_patents, num_assignees
                                      , num_inventors, first_seen_date, last_seen_date, years_active
                                      , persistent_lawyer_id)
select distinct
    l.*

from
    PatentsView_20211230.lawyer l
        join PatentsView_20211230.patent_lawyer pl on pl.lawyer_id = l.lawyer_id
        join elastic_staging.patents p on p.patent_id = pl.patent_id;



CREATE TABLE `other_reference` (
  `uuid` varchar(36) COLLATE utf8mb4_unicode_ci NOT NULL,
  `patent_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `text` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sequence` int(11) DEFAULT NULL,
  `patent_zero_prefix` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `patent_id` (`patent_id`,`sequence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
insert into elastic_staging.other_reference(uuid, patent_id, text, sequence, patent_zero_prefix)
select
    o.uuid
  , o.patent_id
  , o.text
  , o.sequence
  , pe.patent_id_eight_char
from
    patent.otherreference o
        join elastic_staging.patents p on o.patent_id = p.patent_id
        join patent.patent_to_eight_char pe on pe.id = p.patent_id;


CREATE TABLE `rel_app_text` (
  `uuid` varchar(36) COLLATE utf8mb4_unicode_ci NOT NULL,
  `patent_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `text` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `sequence` int(10) unsigned DEFAULT NULL,
  `patent_zero_prefix` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `patent_id` (`patent_id`,`sequence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert into elastic_staging.rel_app_text(uuid, patent_id, text, sequence, patent_zero_prefix)
select
    r.uuid
  , r.patent_id
  , r.text
  , r.sequence
  , pe.patent_id_eight_char
from
    patent.rel_app_text r
        join elastic_staging.patents p on r.patent_id = p.patent_id
        join patent.patent_to_eight_char pe on pe.id = p.patent_id;

CREATE TABLE `us_patent_citations` (
  `uuid` varchar(36) COLLATE utf8mb4_unicode_ci NOT NULL,
  `patent_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `citation_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `kind` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sequence` bigint(22) NOT NULL,
  `patent_zero_prefix` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `patent_id` (`patent_id`),
  KEY `citation_id` (`citation_id`),
  KEY `patent_id_2` (`patent_id`,`sequence`),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert into elastic_staging.us_patent_citations( uuid, patent_id, citation_id, date, name, kind, category
                                               , sequence, patent_zero_prefix)

select
    u2.uuid
  , u2.patent_id
  , u2.citation_id
  , p2.date
  , u2.name
  , u2.kind
  , u2.category
  , u2.sequence
  , p.patent_zero_prefix

from
    patent.uspatentcitation u2
        join elastic_staging.patents p on p.patent_id = u2.patent_id
        join patent.patent p2 on p2.id = u2.citation_id;


CREATE TABLE `us_application_citations` (
  `uuid` varchar(36) COLLATE utf8mb4_unicode_ci NOT NULL,
  `patent_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `document_number` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `kind` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sequence` int(11) DEFAULT NULL,
  `patent_zero_prefix` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `patent_id` (`patent_id`,`sequence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert into elastic_staging.us_application_citations ( uuid, patent_id, document_number, date, name, kind, category
                                                     , sequence, patent_zero_prefix)
select
    uuid
  , u.patent_id
  , u.number_transformed
  , u.date
  , name
  , u.kind
  , category
  , sequence
  , patent_zero_prefix
from
    patent.usapplicationcitation u
        join elastic_staging.patents p on p.patent_id = u.patent_id



CREATE TABLE `wipo_field` (
  `id` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sector_title` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `field_title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_wipo_field_sector_title` (`sector_title`),
  KEY `ix_wipo_field_field_title` (`field_title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
insert into wipo_field
select *
from
    PatentsView_20211230.wipo_field;



CREATE TABLE `cpc_class` (
  `id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `num_patents` int(10) unsigned DEFAULT NULL,
  `num_inventors` int(10) unsigned DEFAULT NULL,
  `num_assignees` int(10) unsigned DEFAULT NULL,
  `first_seen_date` date DEFAULT NULL,
  `last_seen_date` date DEFAULT NULL,
  `years_active` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_cpc_subsection_num_inventors` (`num_inventors`),
  KEY `ix_cpc_subsection_num_assignees` (`num_assignees`),
  KEY `ix_cpc_subsection_num_patents` (`num_patents`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
insert into elastic_staging.cpc_class
select *
from
    PatentsView_20211230.cpc_subsection;

CREATE TABLE `cpc_subclass` (
  `id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `num_patents` int(10) unsigned DEFAULT NULL,
  `num_inventors` int(10) unsigned DEFAULT NULL,
  `num_assignees` int(10) unsigned DEFAULT NULL,
  `first_seen_date` date DEFAULT NULL,
  `last_seen_date` date DEFAULT NULL,
  `years_active` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_cpc_group_num_inventors` (`num_inventors`),
  KEY `ix_cpc_group_num_assignees` (`num_assignees`),
  KEY `ix_cpc_group_num_patents` (`num_patents`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert into elastic_staging.cpc_subclass
select *
from
    PatentsView_20211230.cpc_group;
 CREATE TABLE `cpc_group` (
  `id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(2048) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


insert into cpc_group
select *
from
    PatentsView_20211230.cpc_subgroup
;



CREATE TABLE `uspc_mainclass` (
  `id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `num_patents` int(10) unsigned DEFAULT NULL,
  `num_inventors` int(10) unsigned DEFAULT NULL,
  `num_assignees` int(10) unsigned DEFAULT NULL,
  `first_seen_date` date DEFAULT NULL,
  `last_seen_date` date DEFAULT NULL,
  `years_active` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_uspc_mainclass_num_patents` (`num_patents`),
  KEY `ix_uspc_mainclass_num_inventors` (`num_inventors`),
  KEY `ix_uspc_mainclass_num_assignees` (`num_assignees`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


insert into uspc_mainclass
select *
from
    PatentsView_20211230.uspc_mainclass;



CREATE TABLE `uspc_subclass` (
  `id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
insert into uspc_subclass
select *
from
    PatentsView_20211230.uspc_subclass;



select
    uuid
  , patent_id
  , date
  , number
  , country
  , category
  , sequence
  , patent_zero_prefix
from
    elastic_staging.foreign_citations;

select
    uuid
  , patent_id
  , text
  , sequence
  , patent_zero_prefix
from
    elastic_staging.other_reference;

select
    id, title, num_patents, num_inventors, num_assignees, first_seen_date, last_seen_date, years_active
from elastic_staging.cpc_class;

select
    id, title, num_patents, num_inventors, num_assignees, first_seen_date, last_seen_date, years_active
from elastic_staging.cpc_subclass cs join elastic_staging.cpc_class cc on cc.id=cs.id;


select
    id, title
from elastic_staging.cpc_group;

select
    ipcr_id, section, ipc_class, subclass
from
    elastic_staging.ipcr;

select uuid, patent_id, text, sequence, patent_zero_prefix from elastic_staging.rel_app_text;;

select uuid, patent_id, citation_id, date, name, kind, category, sequence, patent_zero_prefix from elastic_staging.us_patent_citations;

select uuid, patent_id, document_number, date, name, kind, category, sequence, patent_zero_prefix from elastic_staging.us_application_citations;


select id, title, num_patents, num_inventors, num_assignees, first_seen_date, last_seen_date, years_active from PatentsView_20211230.uspc_mainclass;