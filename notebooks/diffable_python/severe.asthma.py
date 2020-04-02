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

# NHS Digital have published their [methodology for high risk shielded patient list identification](https://digital.nhs.uk/coronavirus/shielded-patient-list/methodology/medicines-data). They provided the list as BNF codes and following notebook generates codes compliant with the NHS Dictionary of Medicines and Devices which is the local UK Snomed drug extension. We will use this rule to identify severe asthma

from ebmdatalab import bq
import os
import pandas as pd

# ### Inclusion Criteria
# NHS Digital inclusion criteria rule 1 states "Patients with asthma were identified as being prescribed Long acting beta2-agonist (LABA) as either a LABA or in combination with an inhaled corticosteroid (LABA/ICS) OR prescriptions for a leukotriene receptor antagonist (e.g. monteluekast).""

# +
## The following is written based on version 1 frm March 27th and 
## is archived at https://web.archive.org/save/https://digital.nhs.uk/coronavirus/shielded-patient-list/methodology/medicines-data

sql = '''
WITH bnf_codes AS (  
  SELECT bnf_code FROM hscic.presentation WHERE 
  (bnf_code LIKE '030302%' OR #BNF leukotriene antagonists
  bnf_code LIKE '0301011B0%' OR #BNF bambuterol
  bnf_code LIKE '0301011E0%' OR #BNF formoterol
  bnf_code LIKE '0301011U0%' OR #BNF salmeterol
  bnf_code LIKE '0302000C0%' OR #BNF Beclometasone dipropionate
  bnf_code LIKE '0302000K0%' OR #BNF budesonide
  bnf_code LIKE '0302000V0%' OR #BNF Fluticasone furoate 
  bnf_code LIKE '0302000N0%') #BNF Fluticasone propionate 
   )
   
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)'''

severe_asthma_inc_rule1 = bq.cached_read(sql, csv_path=os.path.join('..','data','severe_asthma_inc_rule1.csv'))
pd.set_option('display.max_rows', None)
severe_asthma_inc_rule1.head(10)
# -

# NHS Digital inclusion criteria rule 2 states "From the above list of patients, those who had been dispensed 4 or more prescriptions for prednisolone between July 2019 and December 2019 were identified and considered to have severe asthma. "
#
# We may wish to consider a different criteria for dispensed. e.g. we could do must have had at least 60 x 5mg prenisolone tabs in last three months

# +
sql = '''
WITH bnf_codes AS (  
  SELECT bnf_code FROM hscic.presentation WHERE 
  bnf_code LIKE '0603020T0%' #BNF oral prednisolone
   )
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)'''

severe_asthma_inc_rule2 = bq.cached_read(sql, csv_path=os.path.join('..','data','severe_asthma_inc_rule2.csv'))
pd.set_option('display.max_rows', None)
severe_asthma_inc_rule2.head(10)

# -

# **Severe Asthma**  = <br/> 
# Presence of at least one from `severe_asthma_inc_rule1` in last three months <br/>
# AND <br/>
# X issues of at least one from `severe_asthma_inc_rule2` in the last three months



