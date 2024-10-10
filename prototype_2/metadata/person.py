
import prototype_2.value_transformations as VT

metadata = {
    'Person': {
    	# person nor patientRole have templateIDs
    	'root': {
    	    'config_type': 'ROOT',
    	    'element': "./hl7:recordTarget/hl7:patientRole"
    	},

        # Institution/file specific ROOT OIDs for person id named after the file in which they were discovered.
        # Often it's not clear these are legitimate or public  OIDs. I haven't found a definition for them.
        # TODO keep an eye on uniqueness and consider if our OMOP patient ID should be a concatination of
        # TODO (cont) root and extension...like if the extension is only unique within a system identified by the root.
    	'person_id_anna_flux': {
    	    'config_type': 'FIELD',
            'data_type': 'INTEGERHASH',
    	    'element': 'hl7:id[@root="2.16.840.1.113883.3.651.2.1"]',
    	    'attribute': "extension",
            'priority': ('person_id', 1)
    	},
    	'person_id_patient_170': {
    	    'config_type': 'FIELD',
            'data_type': 'INTEGERHASH',
    	    'element': 'hl7:id[@root="2.16.840.1.113883.3.6132"]',
    	    'attribute': "extension",
            'priority': ('person_id', 2)
    	},
    	'person_id_patient_502': {
    	    'config_type': 'FIELD',
            'data_type': 'INTEGERHASH',
    	    'element': 'hl7:id[@root="2.16.840.1.113883.19.5.99999.2"]',
    	    'attribute': "extension",
            'priority': ('person_id', 3)
    	},
    	'person_id_patient_healthconnectak': {
    	    'config_type': 'FIELD',
            'data_type': 'INTEGERHASH',
    	    'element': 'hl7:id[@root="2.16.840.1.113883.3.564.14977"]',
    	    'attribute': "extension",
            'priority': ('person_id', 4)
    	},
    	'person_id_patient_bennis_shauna': { # same OID as for eHx_Terry
    	    'config_type': 'FIELD',
            'data_type': 'INTEGERHASH',
    	    'element': 'hl7:id[@root="2.16.840.1.113883.3.7732.100"]',
    	    'attribute': "extension",
            'priority': ('person_id', 5)
    	},
        # more general types of person Ids
    	'person_id_ssn': {
    	    'config_type': 'FIELD',
            'data_type': 'INTEGERHASH',
    	    'element': 'hl7:id[@root="2.16.840.1.113883.4.1"]',
    	    'attribute': "extension",
            'priority': ('person_id', 103)
    	},
    	'person_id_npi': {
    	    'config_type': 'FIELD',
            'data_type': 'INTEGERHASH',
    	    'element': 'hl7:id[@root="2.16.840.1.113883.4.6"]',
    	    'attribute': "extension",
            'priority': ('person_id', 104) # (final field name, priority number)
    	},
    	'person_id_extension_catchall': {
            # if others fail b/c they specify roots not used, just grab an extension
    	    'config_type': 'FIELD',
            'data_type': 'INTEGERHASH',
    	    'element': 'hl7:id',
    	    'attribute': "extension",
            'priority': ('person_id', 105)
    	},
    	'person_id_root_catchall': {
            # if the  extension_catchall fails b/c there is no extension attribute, try just the root
    	    'config_type': 'FIELD',
            'data_type': 'INTEGERHASH',
    	    'element': 'hl7:id',
    	    'attribute': "root",
            'priority': ('person_id', 106)
    	},
    	'person_id_hash': {
    	    'config_type': 'HASH',
            'fields' : [ 'family_name', 'given_name', 'street_address', 'city', 'country', 'postal_code', 'gender_concept_code', 'race_concept_code', 'ethnicity_concept_code', 'date_of_birth', 'person_id_ssn', 'person_id_other' ],
            'priority': ('person_id', 107) # (final field name, priority number)
    	},

        # not for output, but to support person_id_hash creation
        'family_name': {
    	    'config_type': 'FIELD',
    	    'element': './hl7:recordTarget/hl7:patientRole/hl7:name/hl7:family',
    	    'attribute': "#text"
    	},
        'given_name': {
    	    'config_type': 'FIELD',
    	    'element': './hl7:recordTarget/hl7:patientRole/hl7:name/hl7:given',
    	    'attribute': "#text"
    	},
        'street_address': {
    	    'config_type': 'FIELD',
    	    'element': './hl7:recordTarget/hl7:patientRole/hl7:addr/hl7:streetAddressLine',
    	    'attribute': "#text"
    	},
        'city': {
    	    'config_type': 'FIELD',
    	    'element': './hl7:recordTarget/hl7:patientRole/hl7:addr/hl7:city',
    	    'attribute': "#text"
    	},
        'country': {
    	    'config_type': 'FIELD',
    	    'element': './hl7:recordTarget/hl7:patientRole/hl7:addr/hl7:country',
    	    'attribute': "#text"
    	},
        'postal_code': {
    	    'config_type': 'FIELD',
    	    'element': './hl7:recordTarget/hl7:patientRole/hl7:addr/hl7:postalCode',
    	    'attribute': "#text"
    	},

    	'gender_concept_code': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:patient/hl7:administrativeGenderCode",
    	    'attribute': "code"
    	},
    	'gender_concept_codeSystem': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:patient/hl7:administrativeGenderCode",
    	    'attribute': "codeSystem"
    	},
    	'gender_concept_id': {
    	    'config_type': 'DERIVED',
    	    'FUNCTION': VT.map_hl7_to_omop_concept_id,
    	    'argument_names': {
    		    'concept_code': 'gender_concept_code',
    		    'vocabulary_oid': 'gender_concept_codeSystem',
                'default': 8551 # unkown
    	    },
            'order': 2
    	},

        'year_of_birth': {
            'config_type': 'DERIVED',
    	    'FUNCTION': VT.extract_year_of_birth,
    	    'argument_names': {
    		    'date_string': 'birth_datetime',
    	    },
            'order': 3
        },
        'month_of_birth': {
            'config_type': 'DERIVED',
    	    'FUNCTION': VT.extract_month_of_birth,
    	    'argument_names': {
    		    'date_string': 'birth_datetime',
    	    },
            'order': 4
        },
    	'day_of_birth': {
            'config_type': 'DERIVED',
    	    'FUNCTION': VT.extract_day_of_birth,
    	    'argument_names': {
    		    'date_string': 'birth_datetime',
    	    },
            'order': 5
    	},
    	'birth_datetime': {
    	    'config_type': 'FIELD',
            'data_type':'DATE',
    	    'element': "hl7:patient/hl7:birthTime",
    	    'attribute': "value",
            'order': 6
    	},


    	'race_concept_code': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:patient/hl7:raceCode",
    	    'attribute': "code"
    	},
    	'race_concept_codeSystem': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:patient/hl7:raceCode",
    	    'attribute': "codeSystem"
    	},
    	'race_concept_id':{
    	    'config_type': 'DERIVED',
    	    'FUNCTION': VT.map_hl7_to_omop_concept_id,
    	    'argument_names': {
    		    'concept_code': 'race_concept_code',
    		    'vocabulary_oid': 'race_concept_codeSystem',
                'default': 0
    	    },
            'order': 7
    	},

    	'ethnicity_concept_code': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:patient/hl7:ethnicGroupCode",
    	    'attribute': "code"
    	},
    	'ethnicity_concept_codeSystem': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:patient/hl7:ethnicGroupCode",
    	    'attribute': "codeSystem"
    	},
    	'ethnicity_concept_id': {
    	    'config_type': 'DERIVED',
    	    'FUNCTION': VT.map_hl7_to_omop_concept_id,
    	    'argument_names': {
    		    'concept_code': 'ethnicity_concept_code',
    		    'vocabulary_oid': 'ethnicity_concept_codeSystem',
                'default': 0
    	    },
            'order': 8
    	},

    	'person_id': { # down here to bait trouble with sorting
            'config_type': 'PRIORITY',
            'data_type': 'INTEGER', # not applied here, go to the priority fields
            'order': 1
        },
        'location_id': { 'config_type': None, 'order': 9 },
        'provider_id': { 'config_type': None, 'order': 10 },
        'care_site_id': { 'config_type': None, 'order': 11 },
        'person_source_value': { 'config_type': None, 'order': 12 },
        'gender_source_value': { 'config_type': None, 'order': 13 },
        'gender_source_concept_id': { 'config_type': None, 'order': 14 },
        'race_source_value': { 'config_type': None, 'order': 15 },
        'race_source_concept_id': { 'config_type': None, 'order': 16 },
        'ethnicity_source_value': { 'config_type': None, 'order': 17 },
        'ethnicity_source_concept_id': { 'config_type': None, 'order': 18 }

    }
}
