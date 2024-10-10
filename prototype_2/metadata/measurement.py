
import prototype_2.value_transformations as VT

metadata = {
    'Measurement': {
    	'root': {
    	    'config_type': 'ROOT',
    	    'element':
    		  ("./hl7:component/hl7:structuredBody/hl7:component/hl7:section/"
    		   "hl7:templateId[@root='2.16.840.1.113883.10.20.22.2.3.1']"
    		   "/../hl7:entry/hl7:organizer/hl7:component/hl7:observation")
    		    # FIX: another template at the observation level here: "2.16.840.1.113883.10.20.22.4.2
        },

    	'measurement_id_basic': {  # FIX, these IDs come up the same for all 3 observations in the CCD Ambulatory doc.
            'config_type': 'FIELD',
            'element': 'hl7:id',
            'attribute': 'root',
            'priority': ('measurement_id', 9999) # rejected, last in priority
    	},
    	'measurement_id_hash': {
    	    'config_type': 'HASH',
            'fields' : ['person_id', 'visit_occurrence_id', 'measurement_concept_id', 'measurement_time', 'value_as_string'],
            'priority': ('measurement_id', 100)
    	},
        'measurement_id': {
            'config_type': 'PRIORITY',
            'order': 1
        },

    	'person_id': {
    	    'config_type': 'FK',
    	    'FK': 'person_id',
            'order': 2
    	},

    	'measurement_concept_code': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:code" ,
    	    'attribute': "code"
    	},
    	'measurement_concept_codeSystem': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:code",
    	    'attribute': "codeSystem"
    	},
    	'measurement_concept_id': {
    	    'config_type': 'DERIVED',
    	    'FUNCTION': VT.map_hl7_to_omop_concept_id,
    	    'argument_names': {
    		    'concept_code': 'measurement_concept_code',
    		    'vocabulary_oid': 'measurement_concept_codeSystem',
                'default': 0
    	    },
            'order': 3
    	},

    	'measurement_concept_domain_id': {
    	    'config_type': 'DOMAIN',
    	    'FUNCTION': VT.map_hl7_to_omop_domain_id,
    	    'argument_names': {
    		    'concept_code': 'measurement_concept_code',
    		    'vocabulary_oid': 'measurement_concept_codeSystem',
                'default': 0
    	    }
    	},
    	# FIX same issue as above. Is it always just a single value, or do we ever get high and low?
        'measurement_date': {
    	    'config_type': 'FIELD',
            'data_type':'DATETIME',
    	    'element': "hl7:effectiveTime",
    	    'attribute': "value",
            'order': 4
    	},
        'measurement_datetime': { 'config_type': None, 'order': 5 },
        'measurement_time': { 'config_type': None, 'order': 6 },
        'measurement_type_concept_id': {
            'config_type': 'CONSTANT',
            'constant_value' : 32035,
            'order': 8
        },
        'operator_concept_id': { 'config_type': None, 'order': 8 },

    	'value_type': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:value",
    	    'attribute': "{http://www.w3.org/2001/XMLSchema-instance}type",
    	},

    	#'value_as_string': {
    	#    'config_type': 'FIELD',
    	#    'element': 'hl7:value[@xsi:type="ST"]' ,
    	#    'attribute': "#text",
        #    # field not present in measurement table
    	#},


    	'value_as_number_pq': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:value[@xsi:type="PQ"]' ,
    	    'attribute': "value",
            'priority': ['value_as_number', 1]
        },
    	'value_as_number_na': {
    	    'config_type': 'CONSTANT',
    	    'constant_value': "0",
            'priority': ['value_as_number', 100]
        },
    	'value_as_number': {
    	    'config_type': 'PRIORITY',
            'order': 9
    	},


    	'value_as_code_CD': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:value[@xsi:type="CD"]' ,
    	    'attribute': "code",
        },
    	'value_as_codeSystem_CD': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:value[@xsi:type="CD"]' ,
    	    'attribute': "codeSystem",
        },
    	'value_as_concept_id_CD': {
    	    'config_type': 'DERIVED',
    	    'FUNCTION': VT.map_hl7_to_omop_concept_id,
    	    'argument_names': {
    		    'concept_code': 'value_as_code_CD',
    		    'vocabulary_oid': 'value_as_codeSystem_CD',
                'default': None
            },
            'priority': ['value_as_concept_id', 2]
    	},
    	'value_as_code_CE': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:value[@xsi:type="CE"]' ,
    	    'attribute': "code",
        },
    	'value_as_codeSystem_CE': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:value[@xsi:type="CE"]' ,
    	    'attribute': "codeSystem",
        },
    	'value_as_concept_id_CE': {
    	    'config_type': 'DERIVED',
    	    'FUNCTION': VT.map_hl7_to_omop_concept_id,
    	    'argument_names': {
    		    'concept_code': 'value_as_code_CE',
    		    'vocabulary_oid': 'value_as_codeSystem_CE',
                'default': None
            },
            'priority': ['value_as_concept_id', 1]
    	},
        'value_as_concept_id_na': {
            'config_type': 'CONSTANT',
            'constant_value' : 0,
            'priority': ['value_as_concept_id', 100]
        },
    	'value_as_concept_id': {
    	    'config_type': 'PRIORITY',
            'order':  10
    	},


    	'unit_concept_id': { 'config_type': None, 'order':  11 },
    	'range_low': { 'config_type': None, 'order':  12 },
    	'range_high': { 'config_type': None, 'order':  13 },
    	'provider_id': { 'config_type': None, 'order':  14 },

    	'visit_occurrence_id':	{
    	    'config_type': 'FK',
    	    'FK': 'visit_occurrence_id',
            'order':  15
    	},
    	'visit_detail_id':	{ 'config_type': None, 'order':  16 },

    	'measurement_source_value':	{
    	    'config_type': 'FIELD',
    	    'element': "hl7:code" ,
    	    'attribute': "code",
            'order':  17
        },

    	'measurement_source_concept_id':	{ 'config_type': None, 'order':  18 },

    	'unit_source_value':	{ 'config_type': None, 'order':  19 },

    	'value_source_value_constant': {
    	    'config_type': 'CONSTANT',
            'constant_value': 'n/a',
            'priority': ['value_source_value', 4],
        },
    	'value_source_value_text': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:value[@xsi:type="ST"]' ,
    	    'attribute': "#text",
            'priority': ['value_source_value', 3],
        },
    	'value_source_value_code': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:value[@xsi:type="CD"]' ,
    	    'attribute': "code",
            'priority': ['value_source_value', 2],
        },
    	'value_source_value_value': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:value[@xsi:type="PQ"]' ,
    	    'attribute': "value",
            'priority': ['value_source_value', 1],
        },
        'value_source_value' : {
            'config_type': 'PRIORITY',
            'order':20
        }
    }
}
