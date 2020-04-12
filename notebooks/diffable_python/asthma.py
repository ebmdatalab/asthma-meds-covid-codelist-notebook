# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# This is a list of SnoMed / dm+d codes for this [GitHub issue related to asthma](https://github.com/ebmdatalab/tpp-sql-notebook/issues/55)

from ebmdatalab import bq
import os
import pandas as pd

# +
##Rule 1 salbuatmol inhaler
sql = '''
WITH bnf_codes AS (  
  SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
  bnf_code LIKE '0301011R0%'  ##BNF salbutamol - excluded bnf_code LIKE '0301040R0%' as it only has comination with ipratropium in it
  AND (form_route LIKE '%pressurizedinhalation.inhalation' OR form_route LIKE 'powderinhalation.inhalation%')
   )
   
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

sabutamol_asthma = bq.cached_read(sql, csv_path=os.path.join('..','data','sabutamol_asthma.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
sabutamol_asthma

# +
##rule 2 ICS

sql = '''
WITH bnf_codes AS (  
  SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
  (bnf_code LIKE '0302000C0%' OR #BNF Beclometasone dipropionate
  bnf_code LIKE '0301011AB%'  OR #BNF BeclometDiprop/Formoterol/Glycopyrronium",
  bnf_code LIKE '0302000K0%'  OR #BNF budesonide
  bnf_code LIKE '0302000U0%'  OR #BNF Ciclesonide
  bnf_code LIKE '0302000V0%'  OR #BNF Fluticasone furoate 
  bnf_code LIKE '0302000N0%'  OR #BNF Fluticasone propionate 
  bnf_code LIKE '0302000R0%')   #BNF Mometasone Furoate
  AND
  (form_route LIKE '%pressurizedinhalation.inhalation' OR form_route LIKE 'powderinhalation.inhalation%')
   )
   
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

ics_asthma = bq.cached_read(sql, csv_path=os.path.join('..','data','ics_asthma.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
ics_asthma
