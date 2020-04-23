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

# The following chapter contains all combiation inhalers used in COPD and asthma and the associated codes from SnoMed/[NHS Dictionary of Medicines and Devices](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/). 

from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''
WITH bnf_codes AS (  
  SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
  bnf_name LIKE '%/%/%'  ##I think all combination inhalers have / at least twice in their name
  AND
  bnf_code LIKE '03%'
  AND
  (bnf_code NOT LIKE '0309%' AND # cough preps
   bnf_code NOT LIKE '0310%')    # systemic nasal decongestants
  AND 
  form_route NOT LIKE '%neb%'
  )
   
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

resp_combination_products = bq.cached_read(sql, csv_path=os.path.join('..','data','resp_combination_products.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
resp_combination_products
