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

# The following list is of products containing long acting beta agonists (LABA) ingredients (see [prescribing here](https://openprescribing.net/bnf/030101/)).
#
#
# - [Single Ingredient LABAs](#single)
# - [All Multi Ingredent Preparations including LABA](#multi)
# - [LAMA + LABA + ICS containing preparations](#triple)
# - [LABA + ICS](#ics)

from ebmdatalab import bq
import os
import pandas as pd

# ## Single Ingredient LABAs <a id='single'></a>

# +
sql = '''WITH bnf_codes AS (
 SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
   (bnf_code LIKE '0301011E0%'  OR          #BNF Formoterol Fumarate
    bnf_code LIKE '0301011X0%'  OR          #BNF Indacaterol Maleate 
    bnf_code LIKE '0301011Z0%'  OR          #BNF Olodaterol
    bnf_code LIKE '0301011U0%'  OR          #BNF Salmeterol
    bnf_code LIKE '0301011B0%'  )          #BNF Bambuterol Hydrochloride
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

laba_single_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','laba_single_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
laba_single_codelist
# -


