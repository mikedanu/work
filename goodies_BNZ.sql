---------------------------------------------
--reconcile all columns & rows using MD5
---------------------------------------------

--1. query to extract/build concat of column names
select table_schema, table_name, concat('NVL(CAST(', column_name, ' AS VARCHAR), ''''), ') zz, column_name
from db_lending_uat02.information_schema.columns cols
inner join tab_ms_target_table_list_md tgt
on tgt.target_table = cols.table_name
where table_schema = 'SD_CLONE_28FEB2025_BACKUP'
order by table_schema, table_name, ordinal_position

--2. concatenate the above in here:
create or replace temp table PL_TMP_ACCOUNTS_INITIAL_ORG AS 
select md5_binary(MD5_RAW) as MD5_CHECKSUM, *
from (
    select 
        CONCAT_WS('|', 
            NVL(CAST(ACCOUNT_ID AS VARCHAR), ''), 
			...
            NVL(CAST(AUDIT_MODIFIED_USER AS VARCHAR), '')
        ) AS MD5_RAW, *
    from FICO_SD_4.PL_TMP_ACCOUNTS_INITIAL
)

--3. query to reconcile expected vs actual
SELECT NVL(SUM(
        CASE WHEN NVL(CAST(A.MD5_CHECKSUM AS VARCHAR), '??') = NVL(CAST(B.MD5_CHECKSUM AS VARCHAR), '??') THEN 1 ELSE 0 END), 0) CHK_MATCH,
    NVL(SUM(
        CASE WHEN NVL(CAST(A.MD5_CHECKSUM AS VARCHAR), '??') <> NVL(CAST(B.MD5_CHECKSUM AS VARCHAR), '!!') THEN 1 ELSE 0 END), 0) CHK_NOTMATCH,
    COUNT(*) ROW_CNT,
    CASE WHEN ROW_CNT = 0 THEN 100 
         ELSE CAST(DIV0(100*CHK_MATCH, ROW_CNT) AS NUMBER(6,2)) END PCT_MATCH,
    CAST('' AS VARCHAR(100)) RECONCILE_RUN_COMMENT
    --select B.MD5_CHECKSUM EXPECTED_MD5, b.md5_raw expected_md5raw, a.*
FROM PL_TMP_ACCOUNTS_INITIAL_MD_OUTCOME B --where cast(md5_checksum as varchar) = ''
FULL OUTER JOIN PL_TMP_ACCOUNTS_INITIAL_ORG A
--INNER JOIN PL_TMP_ACCOUNTS_INITIAL_ORG A
ON A.MD5_CHECKSUM = B.MD5_CHECKSUM 
where NVL(CAST(A.MD5_CHECKSUM AS VARCHAR), '??') <> NVL(CAST(B.MD5_CHECKSUM AS VARCHAR), '!!')


schemas/tx/ddl/tables/permanent/tx_staging_tables.sql

--******** output to CSV in AWS from SF table
use schema fico_sd_od_orchestration
COPY INTO @SD_STAGE_SERVE_OD_ORCHESTRATION/file/OD-MS/FULL/20260326/OD-PostProcess-Extract-20260326_MAY25_DEV02.CSV.gz
FROM 
(
SELECT * from fico_sd_od_orchestration.od_post_output_summary_MAY25
)
OVERWRITE = TRUE 
SINGLE = TRUE
HEADER = TRUE
FILE_FORMAT=(TYPE = CSV ESCAPE_UNENCLOSED_FIELD=NONE FIELD_OPTIONALLY_ENCLOSED_BY = '"' COMPRESSION='gzip')
MAX_FILE_SIZE=4900000000
;

--****** clone to local
1. Open VS Studio Terminal
2. Create a new folder in "git clone" folder, name it the same as the branch eg. 
3. Grab the https link from git site for the repository
4. In VS Studio terminal, issue this command:

	git clone -b dev02_to_develop_odsm_20260804 https://github.com/bnz-dap/bdh-lending-airflow-dags.git

--***** get top 10 lines and append it to zz.txt
PS C:\Users\017680\Downloads> Get-Content TEST_FL08228_20260430_NOV25_UAT02.CSV -TotalCount 10 >> zz10.txt

--******** extract CSV from file in AWS to SF table
copy into FICO_SD_STAGING.TEST_TX_PD_DATA_MAR26_CSV_20260331_BASELINE 
from (
    select
    t.*
    from '@SD_STAGE_RAW/BUS_TEST/TX_OD/20260504/TX_PD_Data_Mar26.csv' t
)
    file_format = (
    type = csv
    field_optionally_enclosed_by = '"'
    empty_field_as_null = TRUE
    field_delimiter = ','
    error_on_column_count_mismatch=false
    ESCAPE='\\'
    SKIP_HEADER = 1
)
;

copy into ODSM.ODSM_CUSTOMER_BASELINE_20260331
from (
    select
    t.*
    from '@sd_stage_raw/odsm/odsm_account_customer_table_data.csv' t
)
file_format = (
    type = csv
    field_optionally_enclosed_by = '"'
    empty_field_as_null = TRUE
    field_delimiter = ','
    error_on_column_count_mismatch=false
    ESCAPE='\\'
    SKIP_HEADER = 1
)
ON_ERROR = CONTINUE
;
