
import prototype_2.value_transformations as VT

metadata = {
    'Observation': {
    	'root': {
    	    'config_type': 'ROOT',
    	    'element':
    		  ("./hl7:component/hl7:structuredBody/hl7:component/hl7:section/"
    		   "hl7:templateId[@root='2.16.840.1.113883.10.20.22.2.3.1']"
    		   "/../hl7:entry/hl7:organizer/hl7:component/hl7:observation")
    		    # FIX: another template at the observation level here: "2.16.840.1.113883.10.20.22.4.2
    		 },

    	'observation_id': {  # FIX, these IDs come up the same for all 3 observations in the CCD Ambulatory doc.
    	    'config_type': 'FIELD',
    	    'element': 'hl7:id',
    	    'attribute': 'root',   ### FIX ????
            'order': 1
    	},
    	'person_id': {
    	    'config_type': 'FK',
    	    'FK': 'person_id',
            'order': 2
    	},

    	'observation_concept_code': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:code" ,
    	    'attribute': "code"
    	},
    	'observation_concept_codeSystem': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:code",
    	    'attribute': "codeSystem"
    	},
    	'observation_concept_id': {
    	    'config_type': 'DERIVED',
    	    'FUNCTION': VT.map_hl7_to_omop_concept_id,
    	    'argument_names': {
    		    'concept_code': 'observation_concept_code',
    		    'vocabulary_oid': 'observation_concept_codeSystem',
                'default': 0
    	    },
            'order': 3
    	},
    	'observation_concept_domain_id': {
    	    'config_type': 'DOMAIN',
    	    'FUNCTION': VT.map_hl7_to_omop_domain_id,
    	    'argument_names': {
    		    'concept_code': 'observation_concept_code',
    		    'vocabulary_oid': 'observation_concept_codeSystem',
                'default': 0
    	    }
    	},
    	# FIX same issue as above. Is it always just a single value, or do we ever get high and low?
    	'observation_date': {
    	    'config_type': 'FIELD',
            'data_type':'DATETIME',
    	    'element': "hl7:effectiveTime",
    	    'attribute': "value",
            'order': 4
    	},
    	# FIX same issue as above. Is it always just a single value, or do we ever get high and low?
    	'observation_datetime': { 'config_type': None, 'order': 5 },
    	'observation_type_concept_id': {
            'config_type': 'CONSTANT',
            'constant_value' : 32035,
            'order': 8
        },

    	'visit_occurrence_id':	{
    	    'config_type': 'FK',
    	    'FK': 'visit_occurrence_id'
    	},

    	'value_type': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:value",
    	    'attribute': "{http://www.w3.org/2001/XMLSchema-instance}type",
    	},


    	'value_as_string': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:value[@{http://www.w3.org/2001/XMLSchema-instance}type="ST"]' ,
    	    'attribute': "#text",
            'order': 7
    	},


    	'value_as_number': {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:value[@xsi:type="PQ"]' ,
    	    'attribute': "value",
            'order':8
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
            'order':  9
    	},



        'value_unit':  {
    	    'config_type': 'FIELD',
    	    'element': 'hl7:value',
    	    'attribute': 'unit'
    	},
        'unit_concept_id': { 'config_type': None, 'order': 10 },
        'provider_id': { 'config_type': None, 'order': 11 },
        'visit_occurence_id': { 'config_type': None, 'order': 12 },
        'visit_detail_id': { 'config_type': None, 'order': 13 },

        'observation_source_value': {
    	    'config_type': 'FIELD',
    	    'element': "hl7:code" ,
    	    'attribute': "code",
            'order': 14
        },

        'observation_source_concept_id': { 'config_type': None, 'order': 15 },


        'unit_source_value': { 'config_type': None, 'order': 16 },
        'qualifier_source_value': { 'config_type': None, 'order': 17 }
    }
}





