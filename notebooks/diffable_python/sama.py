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

# The following notebook contains [NHS dictionary of medicines and devices codes](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/) for short acting antimuscarininc (SAMA) inhlaers (i.e. ipratropium) that are listed in the BNF.

#import libraries
from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''
WITH bnf_codes AS (  
  SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
  bnf_code LIKE '0301020I0%'  ##BNF ipratropium as only SAM currently on market
  AND (form_route LIKE '%pressurizedinhalation.inhalation' OR form_route LIKE 'powderinhalation.inhalation%')
   )
   
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

sama_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','sama_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
sama_codelist
