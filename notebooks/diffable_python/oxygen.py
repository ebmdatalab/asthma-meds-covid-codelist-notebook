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

# The following notebook contains medicines codes for Oxygen sourced from the [NHS Dictionary of Medicines and Devices](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/). 

from ebmdatalab import bq
import os
import pandas as pd

# +

sql = '''
WITH dmd_codes AS (  
  SELECT id FROM dmd.vmp WHERE
  LOWER(nm) LIKE     '%oxygen%'  AND
  LOWER(nm) NOT LIKE '%mask%'   
 
  )      
   
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE id IN (SELECT * FROM dmd_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE vmp IN (SELECT * FROM dmd_codes)

ORDER BY type, nm '''

oxygen_meds = bq.cached_read(sql, csv_path=os.path.join('..','data','oxygen_meds.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
oxygen_meds
# -


