#!/usr/bin/env python
#
# We can read a edited SQL export from Oracle, but CSV is probably easier.
# In Oracle SQL Developer, export without DDL in US-ASCII format.
# We have to convert dates from 20-MAR-04 to 2004-03-20.
#
# WARNING: there's some serious hack code in here because:
# - we can't find all the fields we need from the CSV columns
# - our references to foreign keys (e.g., Center) won't match the export's
# - etc etc; see the comments in the dict data filling code below.
#
# We need: ANN_DA, A_EMAIL, CONTACT_EMAIL
# What are: ANN_LVL, APP_C, CODE, C_HECK, DA_CAN, KEYS, MNRTY_CODE, MOD_BY,
#   M_EMAIL, NCENT, POSITION_TITLE, REASON, SELECTEE, SEL_DA, SEX, S_BACK,
#   S_GRADE, T_REQ, COMMENTS
# Where do we get: grade_levels, nasa_centers, nasa_center,status,
#   cancel_date, office_id, pay_plan
#
#
# To use, do something like::
#   python importpave.py > importpave.json
#   ./manage.py loaddata ~/importpave.json
#
# Sample row from CSV::
# {'ANN_DA': '22-SEP-03',
#  'ANN_LVL': '',
#  'APP_C': '2',
#  'A_CLOSE': '21-OCT-03',
#  'A_EMAIL': 'phuonglan.t.huyen@nasa.gov',
#  'B_DESC': 'The Program Executive for ISS Utilization Management, ...',
#  'CLEARANCE': '',
#  'CODE': 'CS',
#  'COMMENTS': '',
#  'CONTACT': 'Mrs. Betsy Parks',
#  'CONTACT_EMAIL': 'phuonglan.t.huyen@nasa.gov',
#  'C_HECK': 'n',
#  'DA_CAN': '',
#  'D_DESC': 'Time required:  LEAD . 15 month assignment; full time for 12 months, ...',
#  'KEYS': '0',
#  'MNRTY_CODE': '',
#  'MOD_BY': '',
#  'M_EMAIL': 'phuonglan.t.huyen@nasa.gov',
#  'NCENT': '1000',
#  'OBJ': 'Staff the Procurement Development Team and SEB for the upcoming ....',
#  'OFFICE_TITLE': '',
#  'POSITION_TITLE': '',
#  'P_ENDS': '30-DEC-04',
#  'P_KEY': 'PAVE-03-CS-1408',
#  'P_NUM': '(202) 358-0824',
#  'P_START': '14-OCT-03',
#  'REASON': '',
#  'SELECTEE': 'No',
#  'SEL_DA': '',
#  'SERIES': '',
#  'SEX': '',
#  'SKILL': 'Prior experience in the past 3 years reviewing cost proposals ...',
#  'S_BACK': '',
#  'S_GRADE': '',
#  'T_REQ': '15 months'}

from sys import stderr
import csv
import json
from pprint import pprint as pp

def fix_date(ddmmmyy):
    months = {'JAN': ('01', 31), 'FEB': ('02', 28), 'MAR': ('03', 31),
              'APR': ('04', 30), 'MAY': ('05', 31), 'JUN': ('06', 30),
              'JUL': ('07', 31), 'AUG': ('08', 31), 'SEP': ('09', 30),
              'OCT': ('10', 31), 'NOV': ('11', 30), 'DEC': ('12', 31)}
    (dd, mmm, yyy) = ddmmmyy.split("-")
    (month, days) = months[mmm]
    if int(dd) > days:
        print >> stderr, "fix_date!! ddmmyyy=%s mday=%s days=%s" % (ddmmmyy, month, days)
        dd = days
    return "%4s-%2s-%2s" % (int(yyy) + 2000, month, dd)

f = open('export.csv', 'r')
pavereader = csv.DictReader(f)
projs = []
for d in pavereader:
    projs.append(
        {'pk': None,
         'model': 'project.project',
         'fields': {"grade_levels": [1,2,3], #??FIX INTS: d['S_GRADE'].split(','), # ??
                    "skill_mix": d['SKILL'],
                    "project_number": d['P_KEY'],
                    "position_title": d['POSITION_TITLE'],# | "UNSPECIFIED",
                    "owner": 1,
                    "contact_name": d['CONTACT'],
                    "project_starts": fix_date(d['P_START']),
                    "project_ends":   fix_date(d['P_ENDS']),
                    "detail_description": d['D_DESC'],
                    "objectives": d['OBJ'],
                    "nasa_centers": [1,2,3,4], # ??where do we get these?
                    "nasa_center": int(d['APP_C']), # ?? and we'd need to map urPAVE's FKs
                    "contact_phone": d['P_NUM'],
                    "status": 1,         # ??
                    "cancel_reason": "", # ??
                    "cancel_date": None,
                    "series_codes": [1,2,3], #d['SERIES'].split(','), # split on comma?
                    "office_title": d['OFFICE_TITLE'],
                    "security_clearance_required": (d['CLEARANCE'] != ""),
                    "applicant": None,
                    "announcement_closes": fix_date(d['A_CLOSE']),
                    "office_id": d['CODE'], # ??
                    "brief_description": d['B_DESC'],
                    "pay_plan": "GS" # ??
                    }
         })
print json.dumps(projs, indent=4)



