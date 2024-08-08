import logging
import pandas as pd
logger = logging.getLogger(__name__)

oid_df = pd.read_csv("prototype_2/config/oid.csv")
concept_df = pd.read_csv("prototype_2/config/concept.csv")


def cast_string_to_float(args_dict):
    sv = 0
    string_value = args_dict['input']
    try:
        sv = float(string_value)
    except ValueError:
        logger.error(f"Value error casting {string_value} as integer")
    return sv


def cast_string_to_int(args_dict):
    sv = 0
    string_value = args_dict['input']
    try:
        sv = int(string_value)
    except ValueError:
        logger.error(f"Value error casting {string_value} as integer")
    return sv


def cast_string_to_concept_id(args_dict):
    # string_value = args_dict['input']
    # immediate qustion is if the string_value is a concept_code, which vocabulary_id do you use?
    # next question is at a larger scope, what is the string?
    return ""


def map_oid(codeSystem):
    """ maps an OID used in CCDA to indicate the vocabulary
    to an OMOP vocabulary_id.
    FIX: needs the data, needs written
    """
    try:
        vocabulary_id = oid_df[oid_df['oid'] == codeSystem].vocabulary_id.iloc[0]
        logger.info(" mapping codeSystem \"{codeSystem}\" to \"{vocabulary_id}\" ")
        return vocabulary_id
    except IndexError as e:
        logger.warning(f"no vocab for \"{codeSystem}\" type:{type(e)}")
        return None

def map_to_standard_omop_concept_id(vocabulary_id, concept_code):
    """ Maps vocabulary_id, concept_code to a standard OMOP
    concept_id by joining through concept_relationship.
    FIX: needs the data, needs written
    """
    return 2


def map_hl7_to_omop(vocabulary_oid, concept_code, return_col, return_type):
    """ This would map an HL7 vocabulary_oid to an OMOP vocabulary_id,
    then map both vocabulary_id and concept_code to an OMOP concept_id
    """


def map_hl7_to_omop_w_dict_args(args_dict):
    """ expects: vocabulary_oid, concept_code, return_col, return_type
    Simply maps vocabulary_id, concept_code to an OMOP concept_id.
    Somewhat redundant in that map_to_standard_omop_concept_id
    is much more useful and likely to be used.
    """
    vocabulary_oid = args_dict['vocabulary_oid']
    concept_code = args_dict['concept_code']
    return_col = args_dict['return_col']
    return_type = args_dict['return_type']

    vocabulary_id = map_oid(vocabulary_oid)
    try:
        df = concept_df[(concept_df['vocabulary_id'] == vocabulary_id) &
                        (concept_df['concept_code'] == concept_code)]

        if len(df) > 1:
            logger.warning(
                f"more than one concept for \"{vocabulary_id}\" \"{concept_code}\"")

        if len(df) < 1:
            logger.warning(f"no concept for \"{vocabulary_id}\" \"{concept_code}\"")

        concept = df.iloc[0]
        ret = concept[return_col].astype(return_type)
        return ret

    except IndexError as e:
        logger.warning(f"{type(e)} error {e} mapping \"{vocabulary_id}\" \"{concept_code}\"")
        return None
