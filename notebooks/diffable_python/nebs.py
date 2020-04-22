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

# The following notebook conatins Snomed/[NHS dm+d codes](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/) medicines from chapter 3 - respiratory of the BNF that are delivered by nebuliser macines. Treatment with nebulisers generally indicates more severe disease or this route may be prefered if people cannot use inhalers.
#
# Propose we exclude dornase alpha ([10k scripts per annum](https://openprescribing.net/analyse/#org=CCG&numIds=0303010Q0AAAEAE&denom=nothing&selectedTab=summary)) and sodium cromgicate ([zero prescribing](https://openprescribing.net/analyse/#org=CCG&numIds=0303010Q0AAAEAE&denom=nothing&selectedTab=summary)) as we are looking specifically at meds used in asthma/COPD

from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''WITH bnf_codes AS (
 SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
    bnf_code LIKE '03%'          #BNF respiratrry chapter
    AND 
    form_route LIKE '%neb%'     #limit to nebules through name search
   
  )

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

nebs_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','nebs_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
nebs_codelist
# -

# Propose we exclude dornase alpha ([10k scripts per annum](https://openprescribing.net/analyse/#org=CCG&numIds=0303010Q0AAAEAE&denom=nothing&selectedTab=summary)) and sodium cromgicate ([zero prescribing](https://openprescribing.net/analyse/#org=CCG&numIds=0303010Q0AAAEAE&denom=nothing&selectedTab=summary)) as we are looking specifically at meds used in asthma/COPD


