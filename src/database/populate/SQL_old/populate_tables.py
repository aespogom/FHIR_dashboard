'''
    This module contains the logic to create and populate all SQL database tables
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost if RESET_TABLES = True.
'''

import allergies
import careplans
import claims_transactions
import claims
import conditions
import devices
import encounters
import imaging_studies
import immunizations
import medications
import observations
import organizations
import patients
import payer_transitions
import payers
import procedures
import providers
import suppliers

RESET_TABLES = True

allergies.populate_table(reset_table=RESET_TABLES)
print('allergies')
careplans.populate_table(reset_table=RESET_TABLES)
print('careplans')
claims_transactions.populate_table(reset_table=RESET_TABLES)
print('claims trans')
claims.populate_table(reset_table=RESET_TABLES)
print('claims')
conditions.populate_table(reset_table=RESET_TABLES)
print('conditions')
devices.populate_table(reset_table=RESET_TABLES)
print('devices')
encounters.populate_table(reset_table=RESET_TABLES)
print('encounters')
imaging_studies.populate_table(reset_table=RESET_TABLES)
print('imaging')
immunizations.populate_table(reset_table=RESET_TABLES)
print('immun')
medications.populate_table(reset_table=RESET_TABLES)
print('medication')
observations.populate_table(reset_table=RESET_TABLES)
print('observ')
organizations.populate_table(reset_table=RESET_TABLES)
print('org')
patients.populate_table(reset_table=RESET_TABLES)
print('pat')
payer_transitions.populate_table(reset_table=RESET_TABLES)
print('payer trans')
payers.populate_table(reset_table=RESET_TABLES)
print('payer')
procedures.populate_table(reset_table=RESET_TABLES)
print('procedures')
providers.populate_table(reset_table=RESET_TABLES)
print('provider')
suppliers.populate_table(reset_table=RESET_TABLES)
print('supplier')

