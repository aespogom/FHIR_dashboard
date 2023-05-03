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
careplans.populate_table(reset_table=RESET_TABLES)
claims_transactions.populate_table(reset_table=RESET_TABLES)
claims.populate_table(reset_table=RESET_TABLES)
conditions.populate_table(reset_table=RESET_TABLES)
devices.populate_table(reset_table=RESET_TABLES)
encounters.populate_table(reset_table=RESET_TABLES)
imaging_studies.populate_table(reset_table=RESET_TABLES)
immunizations.populate_table(reset_table=RESET_TABLES)
medications.populate_table(reset_table=RESET_TABLES)
observations.populate_table(reset_table=RESET_TABLES)
organizations.populate_table(reset_table=RESET_TABLES)
patients.populate_table(reset_table=RESET_TABLES)
payer_transitions.populate_table(reset_table=RESET_TABLES)
payers.populate_table(reset_table=RESET_TABLES)
procedures.populate_table(reset_table=RESET_TABLES)
providers.populate_table(reset_table=RESET_TABLES)
suppliers.populate_table(reset_table=RESET_TABLES)