
import prototype_2.value_transformations as VT

""" The meatadata is 3 nested dictionaries:
    - meta_dict: the dict of all domains
    - domain_dict: a dict describing a particular domain
    - field_dict: a dict describing a field component of a domain
    These names are used in the code to help orient the reader
    
    An output_dict is created for each domain. The keys are the field names,
    and the values are the values of the attributes from the elements.

    FIX: the document as a whole has a few template IDs:
    root="2.16.840.1.113883.10.20.22.1.1"
    root="2.16.840.1.113883.10.20.22.1.2"
"""
meta_dict = {
    # domain: { field: [ element, attribute, value_transformation_function ] }
    'person': {
        # person nor patientRole have templateIDs
        'root': {
            'output': False,
            'type': 'ROOT',
            'element': "./recordTarget/patientRole"
        },
        'person_other_id': {
            'output': True,
            'type': 'FIELD',
            'element': 'id[@root="2.16.840.1.113883.4.6"]',
            'attribute': "extension"
        },
        'person_id': {
            'output': True,
            'type': 'PK',
            'element': 'id[@root="2.16.840.1.113883.4.1"]',
            'attribute': "extension"
        },
        'gender_concept_code': {
            'output': False,
            'type': 'FIELD',
            'element': "patient/administrativeGenderCode",
            'attribute': "code"
        },
        'gender_concept_codeSystem': {
            'output': False,
            'type': 'FIELD',
            'element': "patient/administrativeGenderCode",
            'attribute': "codeSystem"
        },
        'gender_concept_id': {
            'output': True,
            'type': 'DERIVED',
            'FUNCTION': VT.map_hl7_to_omop_w_dict_args,
            'argument_names': {
                'concept_code': 'gender_concept_code',
                'vocabulary_oid': 'gender_concept_codeSystem',
                'return_col': 'concept_id',
                'return_type': int,
            }
        },
        'date_of_birth': {
            'output': True,
            'type': 'FIELD',
            'element': "patient/birthTime",
            'attribute': "value"
        },
        'race_concept_code': {
            'output': False,
            'type': 'FIELD',
            'element': "patient/raceCode",
            'attribute': "code"
        },
        'race_concept_codeSystem': {
            'output': False,
            'type': 'FIELD',
            'element': "patient/raceCode",
            'attribute': "codeSystem"
        },
        'race_concept_id':{
            'output': True,
            'type': 'DERIVED',
            'FUNCTION': VT.map_hl7_to_omop_w_dict_args,
            'argument_names': {
                'concept_code': 'race_concept_code',
                'vocabulary_oid': 'race_concept_codeSystem',
                'return_col': 'concept_id',
                'return_type': int,
            }
        },
        'ethnicity_concept_code': {
            'output': False,
            'type': 'FIELD',
            'element': "patient/ethnicGroupCode",
            'attribute': "code"
        },
        'ethnicity_concept_codeSystem': {
            'output': False,
            'type': 'FIELD',
            'element': "patient/ethnicGroupCode",
            'attribute': "codeSystem"
        },
        'ethnicity_concept_id': {
            'output': True,
            'type': 'DERIVED',
            'FUNCTION': VT.map_hl7_to_omop_w_dict_args, # not the string representing the name, but function itself in Python space.
            'argument_names': {
                'concept_code': 'ethnicity_concept_code',
                'vocabulary_oid': 'ethnicity_concept_codeSystem',
                'return_col': 'concept_id',
                'return_type': int,
            }
        },
    },

    'visit_occurrence': {
        # FIX: there's a code for what might be admitting diagnosis here
        'root': {
            'output': False,
            'type': 'ROOT',
            'element': "./componentOf/encompassingEncounter"
        },
        'person_id': {
            'output': True,
            'type': 'FK',
            'FK': 'person_id'
        },
        'visit_occurrence_id_170': {   # for the 170.314...file
            # FIX: why would an occurence_id be an NPI????!!!!!!!
            'output': False,
            'type': 'PK',
            'element': 'id[@root="1.3.6.1.4.1.42424242.4.99930.4.3.4"]',
            # The root says "NPI". The extension is the actual NPI
            'attribute': "extension",
        },
        'visit_occurrence_id': {
            # FIX: why would an occurence_id be an NPI????!!!!!!!
            'output': True,
            'type': 'PK',
            'element': 'id[@root="2.16.840.1.113883.4.6"]',
            # The root says "NPI". The extension is the actual NPI
            'attribute': "extension",
        },
        'visit_concept_code': {
            'output': False,
            'type': 'FIELD',
            'element': "code",     # FIX ToDo is this what I think it is?,
            'attribute': "code"
        },
        'visit_concept_codeSystem': {
            'output': False,
            'type': 'FIELD',
            'element': "code",
            'attribute': "codeSystem"
        },
        'visit_concept_id': {
            'output': True,
            'type': 'DERIVED',
            'FUNCTION': VT.map_hl7_to_omop_w_dict_args, # not the string representing the name, but function itself in Python space.
            'argument_names': {
                'concept_code': 'visit_concept_code',
                'vocabulary_oid': 'visit_concept_codeSystem',
                'return_col': 'concept_id',
                'return_type': int,
            }
        },
        'care_site_id': {
            'output': True,
            'type': 'FIELD',
            'element': "location/healthCareFacility/id",
            'attribute': "root"
        },
        # FIX TODO sometimes a document will have more than one encounterParticipant. The way this is configured, they will be awkwardly merged.
        'provider_id_ep_170': {
            'output': False,
            'type': 'FIELD',
            'element': 'encounterParticipant/assignedEntity/id[@root="1.3.6.1.4.1.42424242.4.99930.4"]',
            'attribute': "extension"
        },
        'provider_id_ep_npi_170': {
            'output': False,
            'type': 'FIELD',
            'element': 'encounterParticipant/assignedEntity/id[@root="2.16.840.1.113883.4.6"]',
            'attribute': "extension"
        },
        'provider_id': {
            'output': True,
            'type': 'FIELD',
            'element': "responsibleParty/assignedEntity/id",
            'attribute': "root"
        },
        # leaving these here more for testing how to pull #text
        'provider_prefix_ep': {
            'output': False,
            'type': 'FIELD',
            'element': "encounterParticipant/assignedEntity/assignedPerson/name/prefix",
            'attribute': "#text"
        },
        'provider_given_ep': {
            'output': False,
            'type': 'FIELD',
            'element': "encounterParticipant/assignedEntity/assignedPerson/name/given",
            'attribute': "#text"
        },
        'provider_family_ep': {
            'output': False,
            'type': 'FIELD',
            'element': "encounterParticipant/assignedEntity/assignedPerson/name/family",
            'attribute': "#text"
        },
        'provider_suffix_ep': {
            'output': False,
            'type': 'FIELD',
            'element': "encounterParticipant/assignedEntity/assignedPerson/name/suffix",
            'attribute': "#text"
        },
        # leaving these here more for testing how to pull #text
        'provider_prefix': {
            'output': False,
            'type': 'FIELD',
            'element': "responsibleParty/assignedEntity/assignedPerson/name/prefix",
            'attribute': "#text"
        },
        'provider_given': {
            'output': False,
            'type': 'FIELD',
            'element': "responsibleParty/assignedEntity/assignedPerson/name/given",
            'attribute': "#text"
        },
        'provider_family': {
            'output': False,
            'type': 'FIELD',
            'element': "responsibleParty/assignedEntity/assignedPerson/name/family",
            'attribute': "#text"
        },
        # FIX is it consistenly a high/low pair? do we sometimes get just effectiveTime@value ?
        'start_time': {
            'output': True,
            'type': 'FIELD',
            'element': "effectiveTime/low",
            'attribute': "value"
        },
        'end_time':  {
            'output': True,
            'type': 'FIELD',
            'element': "effectiveTime/high",
            'attribute': "value"
        }
    },

    'Measurement': {
        'root': {
            'output': False,
            'type': 'ROOT',
            'element':
              ("./component/structuredBody/component/section/"
               "templateId[@root='2.16.840.1.113883.10.20.22.2.3.1']"
               "/../entry/organizer/component/observation")
                # FIX: another template at the observation level here: "2.16.840.1.113883.10.20.22.4.2
             },
        'person_id': {
            'output': True,
            'type': 'FK',
            'FK': 'person_id'
        },
        'visit_occurrence_id':    {
            'output': True,
            'type': 'FK',
            'FK': 'visit_occurrence_id'
        },
        'measurement_id': {  # FIX, these IDs come up the same for all 3 observations in the CCD Ambulatory doc.
            'output': True,
            'type': 'FIELD',
            'element': 'id',
            'attribute': 'root'   ### FIX ????
        },
        'measurement_concept_code': {
            'output': False,
            'type': 'FIELD',
            'element': "code" ,
            'attribute': "code"
        },
        'measurement_concept_codeSystem': {
            'output': False,
            'type': 'FIELD',
            'element': "code",
            'attribute': "codeSystem"
        },
        'measurement_concept_id': {
            'output': True,
            'type': 'DERIVED',
            'FUNCTION': VT.map_hl7_to_omop_w_dict_args, # not the string representing the name, but function itself in Python space.
            'argument_names': {
                'concept_code': 'measurement_concept_code',
                'vocabulary_oid': 'measurement_concept_codeSystem',
                'return_col': 'concept_id',
                'return_type': int,
            }
        },
        'measurement_concept_domain_id': {
            'output': True,
            # 'type': 'DOMAIN',
            'type': 'DERIVED',
            'FUNCTION': VT.map_hl7_to_omop_w_dict_args, # not the string representing the name, but function itself in Python space.
            'argument_names': {
                'concept_code': 'measurement_concept_code',
                'vocabulary_oid': 'measurement_concept_codeSystem',
                'return_col': 'domain_id',
                'return_type': str,
            }
        },
        'measurement_concept_displayName': {
            'output': False,
            'type': 'FIELD',
            'element': "code",
            'attribute': "displayName"
        },
        # FIX same issue as above. Is it always just a single value, or do we ever get high and low?
        'time': {
            'output': True,
            'type': 'FIELD',
            'element': "effectiveTime",
            'attribute': "value"
        },
        'value_as_string': {
            'output': True,
            'type': 'FIELD',
            'element': "value" ,
            'attribute': "value"
        },
        'value_type': {
            'output': True,
            'type': 'FIELD',
            'element': "value",
            'attribute': "type"
        },
        'value_as_number': {
            'output': True,
            'type': 'DERIVED',
            # 'FUNCTION': VT.cast_string_to_int,
            'FUNCTION': VT.cast_string_to_float,
            'argument_names': {
                'input': 'value_as_string',
                'type': 'value_type'
            }
        },
        'value_as_concept_id': {
            'output': True,
            'type': 'DERIVED',
            'FUNCTION': VT.cast_string_to_concept_id,
            'argument_names': {
                'input': 'value_as_string',
                'type': 'value_type'
            }
        },
        'value_unit':  {
            'output': True,
            'type': 'FIELD',
            'element': 'value',
            'attribute': 'unit'
        }
    },
    'Observation': {
        'root': {
            'output': False,
            'type': 'ROOT',
            'element':
              ("./component/structuredBody/component/section/"
               "templateId[@root='2.16.840.1.113883.10.20.22.2.3.1']"
               "/../entry/organizer/component/observation")
                # FIX: another template at the observation level here: "2.16.840.1.113883.10.20.22.4.2
             },
        'person_id': {
            'output': True,
            'type': 'FK',
            'FK': 'person_id'
        },
        'visit_occurrence_id':    {
            'output': True,
            'type': 'FK',
            'FK': 'visit_occurrence_id'
        },
        'observation_id': {  # FIX, these IDs come up the same for all 3 observations in the CCD Ambulatory doc.
            'output': True,
            'type': 'FIELD',
            'element': 'id',
            'attribute': 'root'   ### FIX ????
        },
        'observation_concept_code': {
            'output': False,
            'type': 'FIELD',
            'element': "code" ,
            'attribute': "code"
        },
        'observation_concept_codeSystem': {
            'output': False,
            'type': 'FIELD',
            'element': "code",
            'attribute': "codeSystem"
        },
        'observation_concept_id': {
            'output': True,
            'type': 'DERIVED',
            'FUNCTION': VT.map_hl7_to_omop_w_dict_args, # not the string representing the name, but function itself in Python space.
            'argument_names': {
                'concept_code': 'observation_concept_code',
                'vocabulary_oid': 'observation_concept_codeSystem',
                'return_col': 'concept_id',
                'return_type': int,
            }
        },
        'observation_concept_domain_id': {
            'output': True,
            # 'type': 'DOMAIN',
            'type': 'DERIVED',
            'FUNCTION': VT.map_hl7_to_omop_w_dict_args, # not the string representing the name, but function itself in Python space.
            'argument_names': {
                'concept_code': 'observation_concept_code',
                'vocabulary_oid': 'observation_concept_codeSystem',
                'return_col': 'domain_id',
                'return_type': str,
            }
        },
        'observation_concept_displayName': {
            'output': False,
            'type': 'FIELD',
            'element': "code",
            'attribute': "displayName"
        },
        # FIX same issue as above. Is it always just a single value, or do we ever get high and low?
        'time': {
            'output': True,
            'type': 'FIELD',
            'element': "effectiveTime",
            'attribute': "value"
        },
        'value_as_string': {
            'output': True,
            'type': 'FIELD',
            'element': "value" ,
            'attribute': "value"
        },
        'value_type': {
            'output': True,
            'type': 'FIELD',
            'element': "value",
            'attribute': "type"
        },
        'value_as_number': {
            'output': True,
            'type': 'DERIVED',
            #'FUNCTION': VT.cast_string_to_int,
            'FUNCTION': VT.cast_string_to_float,
            'argument_names': {
                'input': 'value_as_string',
                'type': 'value_type'
            }
        },
        'value_as_concept_id': {
            'output': True,
            'type': 'DERIVED',
            'FUNCTION': VT.cast_string_to_concept_id,
            'argument_names': {
                'input': 'value_as_string',
                'type': 'value_type'
            }
        },
        'value_unit':  {
            'output': True,
            'type': 'FIELD',
            'element': 'value',
            'attribute': 'unit'
        }
    }
}


def x():
    z = {

    }

def get_meta_dict():
    return meta_dict
