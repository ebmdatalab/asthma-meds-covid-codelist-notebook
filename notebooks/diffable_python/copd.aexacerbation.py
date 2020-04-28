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

# ## COPD Exacerbation - Prescription of COPD-specific antibiotic combined with OCS for 5–14 days
#
# One aspect of a strategy to identify COPD exacerbations is to use prescription of COPD-specific antibiotic combined with oral corticosteroid for 5–14 days. This strategy is described in [_Validation of the Recording of Acute
# Exacerbations of COPD in UK Primary Care Electronic Healthcare Record_](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0151357&type=printable) by Rothie et al (2016). We have seperate codelists for each componen
#
# The following notebooks contains SnoMed/[NHS Dictionary of Medicines and Devices](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/) codes to identify these medicines in a electronic health record. When applying to an EHR we should identify presence of a steroid and antibiotic issued on the same day. NICE currently recommends five days but we will use a week to be pragmatic in case a GP has chose to give slightly longer. We should also look for 10-14 days as some practices may issue two rescue packs on a single prescription which is aproach used in the study above.
#
# - [Steroids](#pred)
# - [Antibiotics](#abx)

# #### A note on COPD "Rescue Packs"
# A COPD "rescue pack" is a prescription for a short course of steroids and antibiotics that are issued in advance and a person with COPD keeps on-hand to use when they identify and self-diagnose an exacerbation in line with a their management plan. A [Cochrane review](https://www.cochrane.org/CD011682/AIRWAYS_self-management-interventions-including-action-plans-patients-chronic-obstructive-pulmonary-disease) has found  _the number of people who had at least one hospital admission related to lung disease was reduced among those who participated in a self-management intervention (moderate-quality evidence)_. In the event of an exacerbation [NICE recommends prescription](https://www.nice.org.uk/guidance/ng115/resources/chronic-obstructive-pulmonary-disease-in-over-16s-diagnosis-and-management-pdf-66141600098245) of a short course of oral steroids and antibiotics to treat an exacerbation. Where appropriate these may be issued in advance to people with self management plans. As rescue packs are given in advance we cannot take the date of their issue as definitely the date of exacerbation. They would most likely be given out at COPD annual review or have asscoiated code like `Anticipatory medicine supply procedures simple reference set` in the record.
#

#import libraries
from ebmdatalab import bq
import os
import pandas as pd

# + [markdown]
# ## Steroid <a id='pred'></a>
#
# NICE guidance advises 30 mg oral prednisolone once daily for 5 days.
#
# We have [defined oral steroids in a here](https://github.com/ebmdatalab/steroids-covid-codelist-notebook/blob/master/notebooks/oral.pred.ipynb) for a seperate study.
#
#
# -


# ## Antibioitcs <a id='abx'></a>
#
# Amoxicillin, Doxycycline and Clarithromycin are generally the first choice antibiotics [recommended by NICE](https://cks.nice.org.uk/chronic-obstructive-pulmonary-disease#!scenarioRecommendation:16) and other local organisations for COPD exacerbations. NICE does recommend using sputum cultures to inform choice of antibiotic so for individual cases other antibiotics may be used. Rothie et al (linked above) do have a list which we will include below. 

# +
sql = '''
WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
  bnf_code LIKE '0501013%' OR #bnf antibacterial penicillins
  bnf_code LIKE '050102%'  OR #bnf antibacterial cephalosporins
  bnf_code LIKE '0501030%'    #bnf antibacterials tetracyclines

)

SELECT *
FROM measures.dmd_objs_with_form_route
WHERE bnf_code IN (SELECT * FROM bnf_codes) 
AND 
obj_type IN ('vmp', 'amp')
AND
form_route LIKE '%.oral%' 
ORDER BY obj_type, bnf_code, snomed_id
'''


copd_abx_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','copd_abx_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
copd_abx_codelist
# -


