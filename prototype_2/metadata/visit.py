
import prototype_2.value_transformations as VT
# converted to encouter from encompassingEncounter. The encompassingEncounter attributes are commented out
metadata = {
    'Visit': {
    	# FIX: there's a code for what might be admitting diagnosis here
    	'root': {
    	    'config_type': 'ROOT',
    	    'element': "./hl7:componentOf/hl7:encompassingEncounter"
    	},
    	'visit_occurrence_id': {
            'config_type': 'PRIORITY',
            'order': 1
        },
    	'visit_occurrence_id_170': {   # for the 170.314...file
    	    'config_type': 'PK',
    	    'element': 'hl7:id[@root="1.3.6.1.4.1.42424242.4.99930.4.3.4"]',
    	    'attribute': "extension",
            'priority': ['visit_occurrence_id', 1]
    	},
    	'visit_occurrence_id_other': {
    	    'config_type': 'PK',
    	    'element': 'hl7:id[@root="2.16.840.1.113883.4.6"]',
    	    'attribute': "extension",
            'priority': ['visit_occurrence_id', 2]
    	},
    	'visit_occurrence_id_catchall': {
    	    'config_type': 'PK',
    	    'element': 'hl7:id',
    	    'attribute': "extension",
            'priority': ['visit_occurrence_id', 3]
    	},
       	'visit_occurrence_id_catchall_2': {
    	    'config_type': 'PK',
    	    'element': 'id',
    	    'attribute': "root",
            'priority': ['visit_occurrence_id', 4]
    	},
        'visit_occurrence_id_na': {
    	    'config_type': 'CONSTANT',
            'constant_value': "0",
            'priority': ['visit_occurrence_id', 100]
    	},

    	'person_id': {
    	    'config_type': 'FK',
    	    'FK': 'person_id',
            'order': 2
    	},

    	'visit_concept_code': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:code",	 # FIX ToDo is this what I think it is?,
    	    'attribute': "code"
    	},
    	'visit_concept_codeSystem': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:code",
    	    'attribute': "codeSystem"
    	},
    	'visit_concept_id': {
    	    'config_type': 'DERIVED',
    	    'FUNCTION': VT.map_hl7_to_omop_concept_id,
    	    'argument_names': {
    		    'concept_code': 'visit_concept_code',
    		    'vocabulary_oid': 'visit_concept_codeSystem',
                'default': 0
    	    },
            'order': 3
    	},

    	# FIX is it consistenly a high/low pair? do we sometimes get just effectiveTime@value ?
    	'visit_start_date': {
    	    'config_type': 'PRIORITY',
            'order':4
    	},
    	'visit_start_date_low': {
    	    'config_type': 'FIELD',
            'data_type':'DATE',
    	    'element': "hl7:effectiveTime/hl7:low",
    	    'attribute': "value",
            'priority':  ['visit_start_date', 1]
    	},
    	'visit_start_date_value': {
    	    'config_type': 'FIELD',
            'data_type':'DATE',
    	    'element': "effectiveTime",
    	    'attribute': "value",
            'priority':  ['visit_start_date', 2]
    	},
        'visit_start_datetime' : {  'config_type': None, 'order': 5 },
    	'visit_end_date':  {
    	    'config_type': 'PRIORITY',
            'order':6
    	},
    	'visit_end_date_high':  {
    	    'config_type': 'FIELD',
            'data_type':'DATE',
    	    'element': "hl7:effectiveTime/hl7:high",
    	    'attribute': "value",
            'priority': ['visit_end_date', 1]
    	},
      	'visit_end_date_na':  {
    	    'config_type': 'CONSTANT',
            'constant_value': "",
            'priority': ['visit_end_date', 100]
    	},
        'visit_end_datetime' : {  'config_type': None, 'order': 7 },

        'visit_type_concept_id' : {  
            'config_type': 'CONSTANT', 
            'constant_value' : 32035,
            'order': 8 
        },

    	# FIX TODO sometimes a document will have more than one encounterParticipant. The way this is configured, they will be awkwardly merged.
    	'provider_id': {
    	    'config_type': 'PRIORITY',
            'order': 9
    	},
    	'provider_id_catchall': {
    	    'config_type': 'FIELD',
            #'element': "performer/assignedEntity/id",
    	    'element': "hl7:responsibleParty/hl7:assignedEntity/hl7:id",
    	    'attribute': "root",
            'priority': ['provider_id', 100]
    	},
    	'provider_id_ep_170': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:encounterParticipant/hl7:assignedEntity/hl7:id[@root="1.3.6.1.4.1.42424242.4.99930.4"]',
    	    'attribute': "extension",
            'priority': ['provider_id', 1]
    	},
    	'provider_id_ep_npi_170': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:encounterParticipant/hl7:assignedEntity/hl7:id[@root="2.16.840.1.113883.4.6"]',
    	    'attribute': "extension",
            'priority': ['provider_id', 2]
    	},

    	'care_site_id': {
    	    'config_type': 'FIELD',
            #'element': "participant/participantRole/playingEntity", # not payingEntity? FIX 
    	    'element': "hl7:location/hl7:healthCareFacility/hl7:id",
    	    'attribute': "root",
            'order': 10
    	},

        'visit_source_value': { 'config_type': None, 'order': 11},
        'visit_source_concept_id': { 'config_type': None, 'order': 12},
        'admitting_source_concept_id': { 'config_type': None, 'order': 13},
        'admitting_source_value': { 'config_type': None, 'order': 14},
        'discharge_to_source_concept_id': { 'config_type': None, 'order': 15},
        'discharge_to_source_value': { 'config_type': None, 'order': 16},
        'preceding_visit_occurrence_id': { 'config_type': None, 'order': 17}
        
        # 'custodian_id' : {
        #     'config_type': 'PRIORITY',
        #     'orider': 18
        # }
        #,'custodian_id_constant' : {
        #    'config_type': 'CONSTANT_PK', # new type
        #    'constant_value': "unknown", # place holder
        #    'priority' : ['custodian_id', 100]
        #}
        #, 'custodian_id_field_ext' : {
        #    'config_type': 'FIELD',
        #    'element_no_root': "./custodian/id",  # new attribute, conditional on lack of just 'element'
        #    'attribute' : 'extension',
        #    'priority' : ['custodian_id', 1]  
        #  }
        #, 'custodian_id_field_root' : {
        #    'config_type': 'FIELD',
        #    'element_no_root': "./custodian/id", 
        #    'attribute' : 'extension',
        #    'priority' : ['custodian_id' 2]
        #  }
        # TODO: add custodian_id to person, and as a FK to the domains
    }
}
