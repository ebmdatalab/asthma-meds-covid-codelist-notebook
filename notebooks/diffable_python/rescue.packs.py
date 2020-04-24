# -*- coding: utf-8 -*-
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

# ## COPD "Rescue Packs"
# A COPD "rescue pack" is a prescriptin for a short course of steroids and antibiotics that are issued in advance and a person with COPD keeps on-hand to use when they identify and self-diagnose an exacerbation in line with a their management plan. A [Cochrane review](https://www.cochrane.org/CD011682/AIRWAYS_self-management-interventions-including-action-plans-patients-chronic-obstructive-pulmonary-disease) has found  _the number of people who had at least one hospital admission related to lung disease was reduced among those who participated in a self-management intervention (moderate-quality evidence)_.

# In the event of an exacerbation [NICE recommends prescription](https://www.nice.org.uk/guidance/ng115/resources/chronic-obstructive-pulmonary-disease-in-over-16s-diagnosis-and-management-pdf-66141600098245) of a short course of oral steroids and antibiotics to treat an exacerbation. Where appropriate these may be issued in advance to people with self management plans. The following notebooks contains SnoMed/[NHS Dictionary of Medicines and Devices](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/) codes to identify these medicines in a electronic health record. When applying to an EHR we should identify presence of a steroid and antibiotic issued on the same day. NICE currently recommends five days but we will use a week to be pragmatic in case a GP has chose to give slightly longer. We should also look for 10 days as sme practices may issue two rescue packs on a single prescription.
#
# - [Steroids](#pred)
# - [Antibiotics](#abx)

from ebmdatalab import bq
import os
import pandas as pd

# +
## Steroid <a id='pred'></a>

NICE guidance advises 30 mg oral prednisolone once daily for 5 days — discuss adverse effects of prolonged therapy.
Consider the need for osteoporosis prophylaxis for people requiring frequent courses of oral corticosteroids (3–4 courses per year).


# -



# +
sql = '''WITH bnf_codes AS (
 SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
    (bnf_code LIKE '0301020U0%' OR        #BNF Aclidinium Brom/Formoterol
    bnf_code LIKE '0301040W0%'  OR        #BNF Umeclidinium bromide / Vilanterol
    bnf_code LIKE '0301040X0%'  OR        #BNF Tiotropium bromide  / Olodaterol
    bnf_code LIKE '0302000V0%'  OR        #BNF Fluticasone + Umeclidinium bromide + Vilanterol
    bnf_code LIKE '0301011AB%'  OR        #BNF Beclometasone + Formoterol + Glycopyrronium bromide
    bnf_code LIKE '0301040Y0%')          #BNF Indacaterol 85micrograms/dose / Glycopyrronium bromide
    AND 
    form_route NOT LIKE '%neb%'     #exclude to nebules through name search

  )
  
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm, bnf_code, id'''

lama_multi_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','lama_multi_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
lama_multi_codelist
# -

# ## Antibioitcs <a id='abx'></a>
#
#
# Amoxicillin 500 mg three times a day for 5 days.
# Doxycycline 200 mg on first day, then 100mg once a day for 5-day course in total.
# Clarithromycin 500 mg twice a day for 5 days.

Amoxicillin 500 mg three times a day for 5 days.
Doxycycline 200 mg on first day, then 100mg once a day for 5-day course in total.
Clarithromycin 500 mg twice a day for 5 days.


