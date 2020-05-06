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
    bnf_code LIKE '0301011U0%'  )           #BNF Salmeterol
    AND
    bnf_code  NOT LIKE '0301011B0%'         #BNF Bambuterol Hydrochloride
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

# ## LABA + ICS <a id='ics'></a>

# +
sql = '''WITH vmp_codes AS (
SELECT DISTINCT id FROM dmd.vmp WHERE 
  nm LIKE '%/%/%'  ##I think all combination inhalers have / at least twice in their name
  AND
  bnf_code LIKE '0302%'
  AND
  (bnf_code NOT LIKE '0302000V0B%A0'  AND        #BNF triple therapy
   bnf_code NOT LIKE '0301011AB%') #triple therapy
     )

SELECT "vmp" AS type, id, vmp.bnf_code, nm
FROM dmd.vmp as vmp
INNER JOIN
measures.dmd_objs_with_form_route as dmd
ON
vmp.id = dmd.snomed_id
WHERE id IN (SELECT * FROM vmp_codes)
AND  form_route NOT LIKE '%neb%'

UNION ALL

SELECT "amp" AS type, id, amp.bnf_code, descr
FROM dmd.amp
INNER JOIN
measures.dmd_objs_with_form_route as dmd
ON
amp.id = dmd.snomed_id
WHERE vmp IN (SELECT * FROM vmp_codes)
AND  form_route NOT LIKE '%neb%'

ORDER BY type, nm, bnf_code, id'''

laba_ics_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','laba_ics_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
laba_ics_codelist
# +


