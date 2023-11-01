drop database elastic_staging;

create database elastic_staging;

use elastic_staging;

-- Create syntax for TABLE 'patent_gov_contract'
CREATE TABLE `patent_gov_contract`
(
    `patent_id`    varchar(24) COLLATE utf8mb4_unicode_ci NOT NULL,
    `award_number` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    PRIMARY KEY (`patent_id`, `award_number`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'patent_gov_interest_organizations'
CREATE TABLE `patent_gov_interest_organizations`
(
    `patent_id`   varchar(32) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `name`        varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `level_one`   varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `level_two`   varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `level_three` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    KEY `ix_government_organization_name` (`name`),
    KEY `ix_government_organization_level_one` (`level_one`),
    KEY `ix_government_organization_level_two` (`level_two`),
    KEY `ix_government_organization_level_three` (`level_three`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'applicant'
CREATE TABLE `patent_applicant`
(
    `patent_id`              varchar(36) COLLATE utf8mb4_unicode_ci NOT NULL,
    `lname`                  varchar(64) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `fname`                  varchar(64) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `organization`           varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `sequence`               int(11)                                 DEFAULT NULL,
    `designation`            varchar(20) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `applicant_type`         varchar(30) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `location_id`            int(11)                                 DEFAULT NULL,
    `persistent_location_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    KEY `patent_id` (`patent_id`, `sequence`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'application'
CREATE TABLE `patent_application`
(

    `application_id` varchar(36) COLLATE utf8mb4_unicode_ci NOT NULL,
    `patent_id`      varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `type`           varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `number`         varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `country`        varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `date`           date                                   DEFAULT NULL,
    `series_code`    varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `rule_47_flag`   varchar(8) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    PRIMARY KEY (`application_id`, `patent_id`),
    KEY `ix_application_number` (`number`),
    KEY `ix_application_patent_id` (`patent_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'attorneys'
CREATE TABLE `patent_attorneys`
(
    `patent_id`            varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
    `lawyer_id`            int(10) unsigned                       NOT NULL,
    `persistent_lawyer_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `sequence`             int(11)                                NOT NULL,
    `name_first`           varchar(64) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `name_last`            varchar(64) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `organization`         varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`patent_id`, `sequence`),
    KEY `ix_lawyer_name_last` (`name_last`),
    KEY `ix_lawyer_organization` (`organization`),
    KEY `ix_lawyer_name_first` (`name_first`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'botanic'
CREATE TABLE `patent_botanic`
(
    `patent_id`  varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `latin_name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `variety`    varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    KEY `patent_id` (`patent_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'cpc_at_issue'
CREATE TABLE `patent_cpc_at_issue`
(
    `patent_id`    varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `sequence`     int(10) unsigned                       NOT NULL,
    `cpc_section`  varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `cpc_class`    varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `cpc_subclass` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `cpc_group`    varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `cpc_type`     varchar(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`patent_id`, `sequence`),
    KEY `ix_cpc_current_subsection_id` (`cpc_class`),
    KEY `ix_cpc_current_group_id` (`cpc_subclass`),
    KEY `ix_cpc_current_subgroup_id` (`cpc_group`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'cpc_current'
CREATE TABLE `patent_cpc_current`
(
    `patent_id`    varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `sequence`     int(10) unsigned                       NOT NULL,
    `cpc_section`  varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `cpc_class`    varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `cpc_subclass` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `cpc_group`    varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `cpc_type`     varchar(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`patent_id`, `sequence`),
    KEY `ix_cpc_current_subsection_id` (`cpc_class`),
    KEY `ix_cpc_current_group_id` (`cpc_subclass`),
    KEY `ix_cpc_current_subgroup_id` (`cpc_group`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'examiner'
CREATE TABLE `patent_examiner`
(
    `patent_id`              varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
    `examiner_id`            int(10) unsigned                       NOT NULL,
    `persistent_examiner_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `name_first`             varchar(64) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `name_last`              varchar(64) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `role`                   varchar(20) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `group`                  varchar(20) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    PRIMARY KEY (`patent_id`, `examiner_id`),
    KEY `ix_examiner_name_first` (`name_first`),
    KEY `ix_examiner_name_last` (`name_last`),
    KEY `ix_examiner_role` (`role`),
    KEY `ix_examiner_group` (`group`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'figures'
CREATE TABLE `patent_figures`
(
    `patent_id`   varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `num_figures` int(11) DEFAULT NULL,
    `num_sheets`  int(11) DEFAULT NULL,
    KEY `patent_id` (`patent_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'foreign_priority'
CREATE TABLE `patent_foreign_priority`
(
    `patent_id`          varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `sequence`           int(11)                                NOT NULL,
    `foreign_doc_number` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `date`               date                                   DEFAULT NULL,
    `country`            varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `kind`               varchar(24) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`patent_id`, `sequence`),
    KEY `ix_foreignpriority_foreign_doc_number` (`foreign_doc_number`),
    KEY `ix_foreignpriority_date` (`date`),
    KEY `ix_foreignpriority_kind` (`kind`),
    KEY `ix_foreignpriority_country` (`country`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'granted_pregrant_crosswalk'
CREATE TABLE `granted_pregrant_crosswalk`
(
    `patent_id`          varchar(32) DEFAULT NULL,
    `document_number`    bigint(20)  DEFAULT NULL,
    `application_number` varchar(32) DEFAULT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

-- Create syntax for TABLE 'ipcr'
CREATE TABLE `patent_ipcr`
(
    `patent_id`                  varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `sequence`                   int(11)                                NOT NULL,
    `section`                    varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `ipc_class`                  varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `subclass`                   varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `main_group`                 varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `subgroup`                   varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `symbol_position`            varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `classification_value`       varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `classification_data_source` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `action_date`                date                                   DEFAULT NULL,
    PRIMARY KEY (`patent_id`, `sequence`),
    KEY `ix_ipcr_ipc_class` (`ipc_class`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'patent_assignee'
CREATE TABLE `patent_assignee`
(
    `assignee_id`            int(10) unsigned                       NOT NULL,
    `persistent_assignee_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `type`                   varchar(10) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `name_first`             varchar(64) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `name_last`              varchar(64) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `organization`           varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `city`                   varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `state`                  varchar(20) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `country`                varchar(10) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `sequence`               int(11)                                 DEFAULT NULL,
    `location_id`            int(11)                                 DEFAULT NULL,
    `persistent_location_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `patent_id`              varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
    PRIMARY KEY (`patent_id`, `assignee_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'patent_assignee_incarnations'
CREATE TABLE `patent_assignee_incarnations`
(
    `update_version` date NOT NULL,
    `patent_id`      int(11) DEFAULT NULL,
    `assignee_id`    int(11) DEFAULT NULL,
    PRIMARY KEY (`update_version`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- Create syntax for TABLE 'patent_inventor'
CREATE TABLE `patent_inventor`
(
    `inventor_id`            int(10) unsigned                       NOT NULL,
    `persistent_inventor_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `patent_id`              varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
    `sequence`               int(11)                                NOT NULL,
    `name_first`             varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `name_last`              varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `city`                   varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `state`                  varchar(20) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `country`                varchar(10) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `location_id`            int(11)                                 DEFAULT NULL,
    `persistent_location_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`patent_id`, `inventor_id`, `sequence`),
    KEY `ix_inventor_name_first` (`name_first`),
    KEY `ix_inventor_name_last` (`name_last`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'patents'
CREATE TABLE `patents`
(
    `patent_id`                                             varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `type`                                                  varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `number`                                                varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
    `country`                                               varchar(20) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `date`                                                  date                                    DEFAULT NULL,
    `year`                                                  smallint(5) unsigned                    DEFAULT NULL,
    `abstract`                                              text COLLATE utf8mb4_unicode_ci         DEFAULT NULL,
    `title`                                                 text COLLATE utf8mb4_unicode_ci         DEFAULT NULL,
    `kind`                                                  varchar(10) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `num_claims`                                            smallint(5) unsigned                    DEFAULT NULL,
    `num_foreign_documents_cited`                           int(10) unsigned                       NOT NULL,
    `num_us_applications_cited`                             int(10) unsigned                       NOT NULL,
    `num_us_patents_cited`                                  int(10) unsigned                       NOT NULL,
    `num_total_documents_cited`                             int(10) unsigned                       NOT NULL,
    `num_times_cited_by_us_patents`                         int(10) unsigned                       NOT NULL,
    `earliest_application_date`                             date                                    DEFAULT NULL,
    `patent_processing_days`                                int(10) unsigned                        DEFAULT NULL,
    `uspc_current_mainclass_average_patent_processing_days` int(10) unsigned                        DEFAULT NULL,
    `cpc_current_group_average_patent_processing_days`      int(10) unsigned                        DEFAULT NULL,
    `term_extension`                                        int(10) unsigned                        DEFAULT NULL,
    `detail_desc_length`                                    int(10) unsigned                        DEFAULT NULL,
    `gi_statement`                                          text                                    default null,
    `patent_zero_prefix`                                    varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    PRIMARY KEY (`patent_id`),
    KEY `ix_patent_number` (`number`),
    KEY `ix_patent_title` (`title`(128)),
    KEY `ix_patent_type` (`type`),
    KEY `ix_patent_year` (`year`),
    KEY `ix_patent_date` (`date`),
    KEY `ix_patent_num_claims` (`num_claims`),
    KEY `ix_patent_country` (`country`),
    FULLTEXT KEY `fti_patent_title` (`title`),
    FULLTEXT KEY `fti_patent_abstract` (`abstract`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'pct_data'
CREATE TABLE `patent_pct_data`
(
    `patent_id`  varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `doc_type`   varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `kind`       varchar(2) COLLATE utf8mb4_unicode_ci  NOT NULL,
    `doc_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `date`       date                                   DEFAULT NULL,
    `102_date`   date                                   DEFAULT NULL,
    `371_date`   date                                   DEFAULT NULL,
    PRIMARY KEY (`patent_id`, `kind`),
    KEY `ix_pctdata_102_date` (`102_date`),
    KEY `ix_pctdata_date` (`date`),
    KEY `ix_pctdata_doc_number` (`doc_number`),
    KEY `ix_pctdata_doc_type` (`doc_type`),
    KEY `ix_pctdata_371_date` (`371_date`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'us_related_documents'
CREATE TABLE `patent_us_related_documents`
(
    `patent_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `doctype`   varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `relkind`   varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `reldocno`  varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `country`   varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `date`      date                                   DEFAULT NULL,
    `status`    varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `sequence`  int(11)                                DEFAULT NULL,
    `kind`      varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    KEY `patent_id` (`patent_id`, `sequence`),
    KEY `country` (`country`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'us_term_of_grant'
CREATE TABLE `patent_us_term_of_grant`
(
    `patent_id`       varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `disclaimer_date` date                                    DEFAULT NULL,
    `term_disclaimer` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `term_grant`      varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `term_extension`  varchar(20) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    KEY `patent_id` (`patent_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'uspc_at_issue'
CREATE TABLE `patent_uspc_at_issue`
(
    `patent_id`    varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `sequence`     int(10) unsigned                       NOT NULL,
    `mainclass_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `subclass_id`  varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`patent_id`, `sequence`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create syntax for TABLE 'wipo'
CREATE TABLE `patent_wipo`
(
    `patent_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    `field_id`  varchar(3) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `sequence`  int(10) unsigned                       NOT NULL,
    PRIMARY KEY (`patent_id`, `sequence`),
    KEY `ix_wipo_field_id` (`field_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;


insert into elastic_staging.patents ( patent_id, type, number, country, date, year, abstract, title, kind, num_claims
                                    , num_foreign_documents_cited, num_us_applications_cited, num_us_patents_cited
                                    , num_total_documents_cited, num_times_cited_by_us_patents
                                    , earliest_application_date, patent_processing_days
                                    , uspc_current_mainclass_average_patent_processing_days
                                    , cpc_current_group_average_patent_processing_days, term_extension
                                    , detail_desc_length, gi_statement, patent_zero_prefix)
select
    p.patent_id
  , type
  , number
  , country
  , date
  , year
  , abstract
  , title
  , kind
  , num_claims
  , num_foreign_documents_cited
  , num_us_applications_cited
  , num_us_patents_cited
  , num_total_documents_cited
  , num_times_cited_by_us_patents
  , earliest_application_date
  , patent_processing_days
  , uspc_current_mainclass_average_patent_processing_days
  , cpc_current_group_average_patent_processing_days
  , term_extension
  , detail_desc_length
  , gi_statement
  , pe.patent_id_eight_char
from
    PatentsView_20211230.patent p
        left join PatentsView_20211230.government_interest gi on gi.patent_id = p.patent_id
        join patent.patent_to_eight_char pe on pe.id = p.patent_id
where
     (p.year = 2021
         and month(p.date) = 12)
  or (p.year = 2012
    and month(p.date) = 1);


INSERT INTO elastic_staging.patent_application( application_id, patent_id, type, number, country, date, series_code
                                              , rule_47_flag)
select
    a.application_id
  , p.patent_id
  , a.type
  , a.number
  , a.country
  , a.date
  , pa.series_code_transformed_from_type
  , x.rule_47_flag
from
    PatentsView_20211230.application a
        join patent.application pa on pa.patent_id = a.patent_id
        join (select
                  patent_id
                , case
                      when max(rule_47) = '0' then 'FALSE'
                      when max(rule_47) = '1' then 'TRUE'
                      else max(rule_47) end rule_47_flag
              from
                  patent.rawinventor ri
              group by
                  patent_id) x on x.patent_id = a.patent_id
        join elastic_staging.patents p on p.patent_id = a.patent_id;

TRUNCATE table elastic_staging.patent_assignee;


INSERT INTO elastic_staging.patent_assignee( assignee_id, type, name_first, name_last, organization, city, state
                                           , country, sequence, location_id, patent_id, persistent_location_id
                                           , persistent_assignee_id)

select
    pa.assignee_id
  , a.type
  , a.name_first
  , a.name_last
  , a.organization
  , l.city
  , l.state
  , l.country
  , pa.sequence
  , l.location_id
  , pa.patent_id
  , tima.old_assignee_id
  , timl.old_location_id
from
    PatentsView_20211230.patent_assignee pa
        join elastic_staging.patents p on p.patent_id = pa.patent_id
        join PatentsView_20211230.assignee a on a.assignee_id = pa.assignee_id
        join PatentsView_20211230.temp_id_mapping_assignee tima on tima.new_assignee_id = a.assignee_id
        left join PatentsView_20211230.location l on l.location_id = pa.location_id
        left join PatentsView_20211230.temp_id_mapping_location timl on timl.new_location_id = l.location_id;

TRUNCATE table elastic_staging.patent_inventor;

insert into elastic_staging.patent_inventor ( inventor_id, patent_id, sequence, name_first, name_last, city, state
                                            , country, location_id, persistent_inventor_id, persistent_location_id)

select
    pi.inventor_id
  , pi.patent_id
  , pi.sequence
  , i.name_first
  , i.name_last
  , l.city
  , l.state
  , l.country
  , pi.location_id
  , timi.old_inventor_id
  , timl.old_location_id
from
    PatentsView_20211230.patent_inventor pi
        join PatentsView_20211230.inventor i on i.inventor_id = pi.inventor_id
        join PatentsView_20211230.temp_id_mapping_inventor timi on timi.new_inventor_id = i.inventor_id
        left join PatentsView_20211230.location l on l.location_id = pi.location_id
        left join PatentsView_20211230.temp_id_mapping_location timl on timl.new_location_id = l.location_id
        join elastic_staging.patents p on p.patent_id = pi.patent_id;



insert into elastic_staging.patent_cpc_current( patent_id, sequence, cpc_section, cpc_class, cpc_subclass, cpc_group
                                              , cpc_type)
SELECT
    c.patent_id
  , c.sequence
  , c.section_id
  , c.subsection_id
  , c.group_id
  , c.subgroup_id
  , c.category ``
from
    PatentsView_20211230.cpc_current c
        join elastic_staging.patents p on p.patent_id = c.patent_id;


insert into elastic_staging.granted_pregrant_crosswalk(patent_id, document_number, application_number)

select
    p.patent_id
  , gpc.document_number
  , gpc.application_number
from
    elastic_staging.patents p
        join pregrant_publications.granted_patent_crosswalk gpc on gpc.patent_number = p.patent_id;



insert into elastic_staging.patent_cpc_at_issue( patent_id, sequence, cpc_section, cpc_class, cpc_subclass, cpc_group
                                               , cpc_type)
select
    x.patent_id
  , row_number() over (partition by x.patent_id order by x.source desc,x.sequence) - 1
  , x.section_id
  , x.subsection_id
  , x.group_id
  , x.subgroup_id
  , x.category
from
    (SELECT
         c.patent_id
       , c.sequence
       , section                                                          as section_id
       , concat(section, class)                                           as subsection_id
       , concat(section, class, subclass)                                 as group_id
       , concat(section, class, subclass, main_group, '/', subgroup)      as subgroup_id
       , case when c.value = 'I' then 'inventional' else 'additional' end as category
       , 'main'                                                           as source
     from
         patent.main_cpc c
             join elastic_staging.patents p
                  on p.patent_id = c.patent_id
     union
     SELECT
         c.patent_id
       , c.sequence
       , section                                                          as section_id
       , concat(section, class)                                           as subsection_id
       , concat(section, class, subclass)                                 as group_id
       , concat(section, class, subclass, main_group, '/', subgroup)      as subgroup_id
       , case when c.value = 'I' then 'inventional' else 'additional' end as category
       , 'further'                                                        as source
     from
         patent.further_cpc c
             join elastic_staging.patents p
                  on p.patent_id = c.patent_id) x;



insert into elastic_staging.patent_foreign_priority(patent_id, sequence, foreign_doc_number, date, country, kind)

select
    f.patent_id
  , f.sequence
  , f.foreign_doc_number
  , f.date
  , f.country
  , f.kind
from
    PatentsView_20211230.foreignpriority f
        join elastic_staging.patents p on f.patent_id = p.patent_id



insert into elastic_staging.patent_ipcr ( patent_id, sequence, section, ipc_class, subclass, main_group, subgroup
                                        , symbol_position, classification_value, classification_data_source
                                        , action_date)
select
    i.patent_id
  , i.sequence
  , i.section
  , i.ipc_class
  , i.subclass
  , i.main_group
  , i.subgroup
  , i.symbol_position
  , i.classification_value
  , i.classification_data_source
  , i.action_date
from
    PatentsView_20211230.ipcr i
        join elastic_staging.patents p on i.patent_id = p.patent_id;



insert into elastic_staging.patent_applicant( patent_id, lname, fname, organization, sequence, designation
                                            , applicant_type
                                            , location_id, persistent_location_id)

select
    nia.patent_id
  , nia.lname
  , nia.fname
  , nia.organization
  , nia.sequence
  , nia.designation
  , nia.applicant_type
  , l.location_id
  , timl.old_location_id
from
    patent.non_inventor_applicant nia
        join elastic_staging.patents p on nia.patent_id = p.patent_id
        left join patent.rawlocation rl on rl.id = nia.rawlocation_id
        left join PatentsView_20211230.temp_id_mapping_location timl on timl.old_location_id = rl.location_id
        left join PatentsView_20211230.location l on l.location_id = timl.new_location_id



insert into elastic_staging.patent_pct_data(patent_id, doc_type, kind, doc_number, date, `102_date`, `371_date`)
select
    p.patent_id
  , p.doc_type
  , p.kind
  , p.doc_number
  , p.date
  , p.`102_date`
  , p.`371_date`
from
    PatentsView_20211230.pctdata p
        join elastic_staging.patents p2 on p.patent_id = p2.patent_id;



insert into elastic_staging.patent_uspc_at_issue(patent_id, sequence, mainclass_id, subclass_id)
select
    u.patent_id
  , sequence
  , mainclass_id
  , subclass_id
from
    patent.uspc u
        join elastic_staging.patents p on p.patent_id = u.patent_id;



insert into elastic_staging.patent_wipo(patent_id, field_id, sequence)
select
    w.patent_id
  , w.field_id
  , w.sequence
from
    PatentsView_20211230.wipo w
        join elastic_staging.patents p on p.patent_id = w.patent_id;



insert into elastic_staging.patent_botanic(patent_id, latin_name, variety)
select
    b.patent_id
  , b.latin_name
  , b.variety
from
    patent.botanic b
        join elastic_staging.patents p on p.patent_id = b.patent_id;



insert into elastic_staging.patent_figures(patent_id, num_figures, num_sheets)
select
    f.patent_id
  , f.num_figures
  , f.num_sheets
from
    patent.figures f
        join elastic_staging.patents p on f.patent_id = p.patent_id
;



insert into elastic_staging.patent_attorneys( patent_id, lawyer_id, sequence, name_first, name_last, organization
                                            , persistent_lawyer_id)
select
    pl.patent_id
  , pl.lawyer_id
  , pl.sequence
  , l.name_first
  , l.name_last
  , l.organization
  , timl.old_lawyer_id
from
    PatentsView_20211230.patent_lawyer pl
        join PatentsView_20211230.lawyer l on pl.lawyer_id = l.lawyer_id
        join PatentsView_20211230.temp_id_mapping_lawyer timl on timl.new_lawyer_id = l.lawyer_id
        join elastic_staging.patents p on pl.patent_id = p.patent_id;



insert into elastic_staging.patent_examiner( patent_id, examiner_id, name_first, name_last, role, `group`
                                           , persistent_examiner_id)
select
    pe.patent_id
  , pe.examiner_id
  , e.name_first
  , e.name_last
  , e.role
  , e.`group`
  , `time`.old_examiner_id
from
    PatentsView_20211230.patent_examiner pe
        join PatentsView_20211230.examiner e on pe.examiner_id = e.examiner_id
        join PatentsView_20211230.temp_id_mapping_examiner `time` on `time`.new_examiner_id = e.examiner_id
        join elastic_staging.patents p on p.patent_id = pe.patent_id;



insert into elastic_staging.patent_us_term_of_grant( patent_id, disclaimer_date, term_disclaimer, term_grant
                                                   , term_extension)
select
    u.patent_id
  , u.disclaimer_date
  , u.term_disclaimer
  , u.term_grant
  , u.term_extension
from
    patent.us_term_of_grant u
        join elastic_staging.patents p
             on p.patent_id = u.patent_id;


insert into elastic_staging.patent_gov_interest_organizations(patent_id, name, level_one, level_two, level_three)
select
    pgi.patent_id
  , name
  , level_one
  , level_two
  , level_three
from
    PatentsView_20211230.government_organization go
        join PatentsView_20211230.patent_govintorg pgi on pgi.organization_id = go.organization_id
        join elastic_staging.patents p on p.patent_id = pgi.patent_id;

insert into elastic_staging.patent_gov_contract(patent_id, award_number)
select
    c.patent_id
  , contract_award_number
from
    PatentsView_20211230.patent_contractawardnumber c
        join elastic_staging.patents p on p.patent_id = c.patent_id;

CREATE TABLE `ipcr`
(
    `ipcr_id`   int(11) unsigned NOT NULL AUTO_INCREMENT,
    `section`   varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `ipc_class` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `subclass`  varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`ipcr_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 8192
  DEFAULT CHARSET = latin1;


insert into elastic_staging.ipcr(section, ipc_class, subclass)
select
    section
  , ipc_class
  , subclass
from
    elastic_staging.ipcr
order by
    section
  , ipc_class
  , subclass;


update elastic_staging.patent_ipcr i join elastic_staging.ipcr i2 on i2.section = i.section and
                                                                     i2.ipc_class = i.ipc_class and
                                                                     i2.subclass = i.subclass
set i.ipcr_id=i2.ipcr_id;


select
    a.application_id
  , a.type
  , a.date
  , a.series_code
  , case when a.rule_47_flag = 0 then 'false' else 'true' end
  , a.type
  , a.patent_id
from
    elastic_staging.patent_application a
        join (select patent_id from elastic_staging.patents order by patent_id limit 10 offset 0) p
             on p.patent_id = a.patent_id;

insert into elastic_staging.patent_us_related_documents( patent_id, doctype, relkind, reldocno, country, date, status
                                                       , sequence, kind)
select
    p.patent_id
  , doctype
  , relkind
  , reldocno
  , u.country
  , u.date
  , status
  , sequence
  , u.kind
from
    patent.usreldoc u
        join elastic_staging.patents p on p.patent_id = u.patent_id;

select
    c.sequence
  , c.cpc_section
  , c.cpc_class
  , c.cpc_class
  , c.cpc_subclass
  , c.cpc_subclass
  , c.cpc_group
  , c.cpc_group
  , c.cpc_type
  , c.patent_id
from
    elastic_staging.patent_cpc_current as c
        join (select patent_id from elastic_staging.patents order by patent_id limit 10 offset 0) p
             on p.patent_id = c.patent_id;


update
    elastic_staging.patents p
        left join patent.patent_to_eight_char pe on pe.id = p.patent_id
set p.patent_zero_prefix =pe.patent_id_eight_char;

update elastic_staging.patent_applicant pa
    join patent.non_inventor_applicant nia on nia.patent_id = pa.patent_id
    join elastic_staging.selected_rawlocations rl on rl.id = nia.rawlocation_id
    join PatentsView_20211230.temp_id_mapping_location timl on timl.old_location_id = rl.location_id
set pa.location_id=timl.new_location_id
  , pa.persistent_location_id=timl.old_location_id;




