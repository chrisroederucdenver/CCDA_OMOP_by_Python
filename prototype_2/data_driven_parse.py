#!/usr/bin/env python3

""" Table-Driven ElementTree parsing in Python

 This version puts the paths into a data structure and explores using
 one function driven by the data.
 - The mapping_dict is hard-coded here. An next step would be to read that in from a file.
 - Value transformation is stubbed out waiting for vocabularies to be loaded, and to
   figure out how to use them once there.

 Chris Roeder

2024-07-31: visit_concept_id is incorrect, It's picking up pnemonia a Condition
               when we want a Visit domain_id
"           need to run on multiple files, need to bring over the test script and correct_files,
"           test script needs sophistication to correlate input with expected output
"""

# import pandas as pd
# mamba install -y -q lxml

import argparse
import datetime
import logging
import os
import hashlib
from lxml import etree as ET
from prototype_2.metadata import get_meta_dict

logger = logging.getLogger(__name__)


ns = {
   '': 'urn:hl7-org:v3',  # default namespace
   'hl7': 'urn:hl7-org:v3',
   'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
   'sdtc': 'urn:hl7-org:sdtc'
}


PK_dict = {}


def cast_to_date(string_value):
    # TODO does CCDA always do dates as YYYYMMDD ?
    # TODO  when  is it date and when datetime

    # Step 1 : put dashes in  to make ISO-8601 happy, b/c python insists on dashes.
    iso_8601_string = f"{string_value[0:4]}-{string_value[4:6]}-{string_value[6:8]}"
    #print(f"DATE iso8601 string {string_value} {iso_8601_string}")

    # Step 2: dont' both with fancy date classes that can't help us here.

    return iso_8601_string


def cast_to_datetime(string_value):
    # TODO does CCDA always do dates as YYYYMMDD ? ...without dashes?
    if len(string_value) > 8:
        iso_8601_string = f"{string_value[0:4]}-{string_value[4:6]}-{string_value[6:8]} {string_value[8:10]}:{string_value[10:12]}"
        #print(f"DATETIME iso8601 string {string_value}  {iso_8601_string}")
        return iso_8601_string
    else:
        #print(f"{string_value} too short for DATETIME")
        return cast_to_date(string_value)



def parse_field_from_dict(field_details_dict, domain_root_element, domain, field_tag, root_path):
    """ Retrieves a value for the field descrbied in field_details_dict that lies below
        the domain_root_element.
        Domain and field_tag are here for error messages.
    """

    if 'element' not in field_details_dict:
        logger.error(("FIELD could find key 'element' in the field_details_dict:"
                     f" {field_details_dict} root:{root_path}"))
        return None

    logger.info(f"    FIELD {field_details_dict['element']} for {domain}/{field_tag}")
    field_element = domain_root_element.find(field_details_dict['element'], ns)
    if field_element is None:
        logger.error((f"FIELD could not find field element {field_details_dict['element']}"
                      f" for {domain}/{field_tag} root:{root_path}"))
        return None

    if 'attribute' not in field_details_dict:
        logger.error((f"FIELD could not find key 'attribute' in the field_details_dict:"
                     f" {field_details_dict} root:{root_path}"))
        return None

    logger.info((f"       ATTRIBUTE   {field_details_dict['attribute']} "
                 f"for {domain}/{field_tag} {field_details_dict['element']} "))
    attribute_value = field_element.get(field_details_dict['attribute'])
    if field_details_dict['attribute'] == "#text":
        attribute_value = field_element.text
    if attribute_value is None:
        logger.warning((f"no value for field element {field_details_dict['element']} "
                        f"for {domain}/{field_tag} root:{root_path}"))

    if 'data_type' in field_details_dict:
        if field_details_dict['data_type'] == 'DATE':
            attribute_value = cast_to_date(attribute_value)
        if field_details_dict['data_type'] == 'DATETIME':
            attribute_value = cast_to_datetime(attribute_value)

    return attribute_value


def do_basic_fields(output_dict, root_element, root_path, domain,  domain_meta_dict, error_fields_set):
    for (field_tag, field_details_dict) in domain_meta_dict.items():
        logger.info((f"     FIELD domain:'{domain}' field_tag:'{field_tag}'"
                     f" {field_details_dict}"))
        type_tag = field_details_dict['config_type']
        if type_tag == 'FIELD':
            logger.info(f"     FIELD for {domain}/{field_tag}")
            attribute_value = parse_field_from_dict(field_details_dict, root_element,
                                                    domain, field_tag, root_path)
            output_dict[field_tag] = (attribute_value, root_path + "/" +
                                      field_details_dict['element'] + "/@" +
                                      field_details_dict['attribute'])
        elif type_tag == 'PK':
            logger.info(f"     PK for {domain}/{field_tag}")
            attribute_value = parse_field_from_dict(field_details_dict, root_element,
                                                    domain, field_tag, root_path)
            output_dict[field_tag] = (attribute_value, root_path + "/" +
                                      field_details_dict['element'] + "/@" +
                                      field_details_dict['attribute'])
            PK_dict[field_tag] = attribute_value
        elif type_tag == 'FK':
            logger.info(f"     FK for {domain}/{field_tag}")
            if field_tag in PK_dict:
                output_dict[field_tag] = (PK_dict[field_tag], 'FK')
            else:
                logger.error(f"FK could not find {field_tag}  in PK_dict for {domain}/{field_tag}")
                path = root_path + "/"
                if 'element' in field_details_dict:
                    path = path + field_details_dict['element'] + "/@"
                else:
                    path = path + "no element/"
                if 'attribute' in field_details_dict:
                    path = path + field_details_dict['attribute']
                else:
                    path = path + "no attribute/"
                output_dict[field_tag] = (None, path)
                error_fields_set.add(field_tag)


def do_derived_fields(output_dict, root_element, root_path, domain,  domain_meta_dict, error_fields_set):
    # Do derived values now that their inputs should be available in the output_dict
    for (field_tag, field_details_dict) in domain_meta_dict.items():
        if field_details_dict['config_type'] == 'DERIVED':
            logger.info(f"     DERIVING {field_tag}, {field_details_dict}")
            # NB Using an explicit dict here instead of kwargs because this code here
            # doesn't know what the keywords are at 'compile' time.
            args_dict = {}
            for arg_name, field_name in field_details_dict['argument_names'].items():
                logger.info(f"     -- {field_tag}, arg_name:{arg_name} field_name:{field_name}")
                if field_name not in output_dict:
                    error_fields_set.add(field_tag)
                    logger.error((f"DERIVED domain:{domain} field:{field_tag} could not "
                                  f"find {field_name} in {output_dict}"))
                try:
                    args_dict[arg_name] = output_dict[field_name][0]
                except Exception:
                    error_fields_set.add(field_tag)
                    logger.error((f"DERIVED {field_tag} arg_name: {arg_name} field_name:{field_name}"
                                  f" args_dict:{args_dict} output_dict:{output_dict}"))
            try:
                function_value = field_details_dict['FUNCTION'](args_dict)
                output_dict[field_tag] = (function_value, 'DERIVED')
                logger.info((f"     DERIVED {function_value} for "
                                f"{field_tag}, {field_details_dict} {output_dict[field_tag]}"))
            except TypeError as e:
                error_fields_set.add(field_tag)
                logger.error(f"DERIVED exception: {e}")
                logger.error((f"DERIVED {field_tag} possibly calling something that isn't a function"
                              f" {field_details_dict['FUNCTION']}. You may have quotes "
                              "around it in  a python mapping structure if this is a "
                              f"string: {type(field_details_dict['FUNCTION'])}"))
                output_dict[field_tag] = (None, field_details_dict['config_type'])


def do_domain_fields(output_dict, root_element, root_path, domain,  domain_meta_dict, error_fields_set):
    # nearly the same as derived above, but returns the domain for later filtering
    domain_id = None
    for (field_tag, field_details_dict) in domain_meta_dict.items():
        if field_details_dict['config_type'] == 'DOMAIN':
            logger.info(f"     Deriving DOMAIN {field_tag}, {field_details_dict}")

            # Collect args for the function
            args_dict = {}
            for arg_name, field_name in field_details_dict['argument_names'].items():
                logger.info(f"     -- {field_tag}, arg_name:{arg_name} field_name:{field_name}")
                if field_name not in output_dict:
                    error_fields_set.add(field_tag)
                    logger.error((f"DERIVED domain:{domain} field:{field_tag} could not "
                                  f"find {field_name} in {output_dict}"))
                try:
                    args_dict[arg_name] = output_dict[field_name][0]
                except Exception:
                    error_fields_set.add(field_tag)
                    logger.error((f"DERIVED {field_tag} arg_name: {arg_name} field_name:{field_name}"
                                  f" args_dict:{args_dict} output_dict:{output_dict}"))
            # Derive the value
            try:
                function_value = field_details_dict['FUNCTION'](args_dict)
                domain_id = function_value
                output_dict[field_tag] = (function_value, 'DOMAIN') ##########
                logger.info((f"     DOMAIN captured as {function_value} for "
                                 f"{field_tag}, {field_details_dict}"))
            except TypeError as e:
                error_fields_set.add(field_tag)
                logger.error(f"DERIVED exception: {e}")
                logger.error((f"DERIVED {field_tag} possibly calling something that isn't a function"
                              f" {field_details_dict['FUNCTION']}. You may have quotes "
                              "around it in  a python mapping structure if this is a "
                              f"string: {type(field_details_dict['FUNCTION'])}"))
                output_dict[field_tag] = (None, field_details_dict['config_type'])

            #print(f"     DOMAIN-2  {field_tag} {domain} {domain_id} {len(domain_meta_dict.items())} ")
    return domain_id


def do_hash_fields(output_dict, root_element, root_path, domain,  domain_meta_dict, error_fields_set):
    """ These are basically derived, but the argument is a lsit of field names, instead of
        a fixed number of individually named fields.
    """
    for (field_tag, field_details_dict) in domain_meta_dict.items():
        if field_details_dict['config_type'] == 'HASH':
            hash_input =  "-".join(field_details_dict['fields'])
            hash_value = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
            output_dict[field_tag] = (hash_value, 'HASH')
            logger.info((f"     HASH {hash_value} for "
                         f"{field_tag}, {field_details_dict} {output_dict[field_tag]}"))


def do_priority_fields(output_dict, root_element, root_path, domain,  domain_meta_dict, error_fields_set):
    """
        Returns the list of  priority_names so they can be added to "output" fields
        Also, adds this field to the PK list?
        within the domain_meta_dict, find all fields tagged with priority and group them by their priority names in a dictionary keyed by that name
        Ex. { 'person_id': [ ('person_id_ssn', 1), ('person_id_unknown', 2) ]
    """

    # Create Ref Data
    # for each new field, create a list of source fields and their priority:
    # Ex. [('person_id_other', 2), ('person_id_ssn', 1)]
    priority_fields = {}
    for field_key, config_parts in domain_meta_dict.items():
        if  'priority' in config_parts:
            new_field_name = config_parts['priority'][0]
            priority_number = config_parts['priority'][1]
            if new_field_name in priority_fields:
                priority_fields[new_field_name].append( (field_key, config_parts['priority'][1]))
            else:
                priority_fields[new_field_name] = [ (field_key, config_parts['priority'][1]) ]

    # Choose Fields
    # first field in each set with a non-null value in the output_dict adds that value to the dict with it's priority_name
    for priority_name, priority_contents in priority_fields.items():
        sorted_contents = sorted(priority_contents, key=lambda x: x[1])
        # Ex. [('person_id_ssn', 1), ('person_id_other, 2)]

        for value_field_pair in sorted_contents:
            if value_field_pair[0] in output_dict and output_dict[value_field_pair[0]][0] is not None:
                output_dict[priority_name] = output_dict[value_field_pair[0]]
                PK_dict[priority_name] = output_dict[value_field_pair[0]][0]
                break

    return priority_fields


def clean_dict(output_dict, priority_field_names, domain_meta_dict):
    # Clean the dict by removing fields with a False output tag
    clean_output_dict = {}
    for key in output_dict:
        if key in priority_field_names:
            clean_output_dict[key] = output_dict[key]
        elif key in domain_meta_dict:
            field_details_dict = domain_meta_dict[key]
            if field_details_dict['output']:
                clean_output_dict[key] = output_dict[key]
        elif key != 'root_path':
            print(f"ERROR found key {key} that's neither a priority key nor in the domain_meta_dict. Impossible error #42")
    return clean_output_dict


def parse_domain_for_single_root(root_element, root_path, domain, domain_meta_dict, error_fields_set):
    """  Parses for each field in the metadata for a domain out of the root_element passed in.
         You may have more than one such root element, each making for a row in the output.

        If the configuration includes a field of config_type DOMAIN, the value it generates
        will be compared to the domain passed in. If they are different, null is returned.
        This is how  OMOP "domain routing" is implemented here.
    """
    output_dict = {}
    domain_id = None
    logger.info((f"  ROOT for domain:{domain}, we have tag:{root_element.tag}"
                 f" attributes:{root_element.attrib}"))

    do_basic_fields(output_dict, root_element, root_path, domain,  domain_meta_dict, error_fields_set)
    do_derived_fields(output_dict, root_element, root_path, domain,  domain_meta_dict, error_fields_set)
    domain_id = do_domain_fields(output_dict, root_element, root_path, domain,  domain_meta_dict, error_fields_set)
    do_hash_fields(output_dict, root_element, root_path, domain,  domain_meta_dict, error_fields_set)
    priority_field_names = do_priority_fields(output_dict, root_element, root_path, domain,  domain_meta_dict, error_fields_set)


    # Add a "root" column to show where this came from
    output_dict['root_path'] = (root_path, 'root_path')

    if (domain == domain_id or domain_id is None):
        clean_output_dict = clean_dict(output_dict, priority_field_names, domain_meta_dict)
        return (clean_output_dict, error_fields_set)
    else:
        return (None, None)


def parse_domain_from_dict(tree, domain, domain_meta_dict, filename):
    """ The main logic is here.
        Given a tree from ElementTree representing a CCDA document
        (ClinicalDocument, not just file),
        parse the different domains out of it, linking PK and FKs between them.
        Returns a list, output_list, of dictionaries, output_dict, keyed by field name,
        containing a list of the value and the path to it:
            [ { field_1 : (value, path), field_2: (value, path)},
              { field_1: (value, path)}, {field_2: (value, path)} ]
        It's a list of because you might have more than one instance of the root path, like when you
        get many observations.
    """

    # log to a file per file/domain
    base_name = os.path.basename(filename)
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        filename=f"logs/log_domain_{base_name}_{domain}.log",
        force=True, level=logging.WARNING)

    # Find root
    if 'root' not in domain_meta_dict:
        logger.error(f"DOMAIN {domain} lacks a root element.")
        return None

    if 'element' not in domain_meta_dict['root']:
        logger.error(f"DOMAIN {domain} root lacks an 'element' key.")
        return None

    root_path = domain_meta_dict['root']['element']
    logger.info((f"DOMAIN >>  domain:{domain} root:{domain_meta_dict['root']['element']}"
                 f"   ROOT path:{root_path}"))
    root_element_list = tree.findall(domain_meta_dict['root']['element'], ns)
    if root_element_list is None or len(root_element_list) == 0:
        logger.error((f"DOMAIN couldn't find root element for {domain}"
                      f" with {domain_meta_dict['root']['element']}"))
        return None

    output_list = []
    error_fields_set = set()
    logger.info(f"NUM ROOTS {domain} {len(root_element_list)}")
    print(f"NUM ROOTS {domain} {len(root_element_list)}")
    for root_element in root_element_list:
        (output_dict, element_error_set) = parse_domain_for_single_root(root_element, root_path, domain, domain_meta_dict, error_fields_set)
        if output_dict is not None:
            output_list.append(output_dict)
        if element_error_set is not None:
            error_fields_set.union(element_error_set)

    # report fields with errors
    if len(error_fields_set) > 0:
        logger.error(f"DOMAIN Fields with errors in domain {domain} {error_fields_set}")

    return output_list


def parse_doc(file_path, metadata):
    """ Parses many domains from a single file, collects them
        into a dict to return.
    """
    omop_dict = {}
    tree = ET.parse(file_path)
    base_name = os.path.basename(file_path)
    for domain, domain_meta_dict in metadata.items():
        domain_data_dict = parse_domain_from_dict(tree, domain, domain_meta_dict, base_name)
        omop_dict[domain] = domain_data_dict
    return omop_dict


def print_omop_structure(omop):
    """ prints a dict of parsed domains as returned from parse_doc()
        or parse_domain_from_dict()
    """
    print(f"PK_dict: {PK_dict}")
    for domain, domain_list in omop.items():
        if domain_list is None:
            logger.warning(f"no data for domain {domain}")
        else:
            for domain_data_dict in domain_list:
                n = 0
                if domain_data_dict is None:
                    print(f"\n\nERROR DOMAIN: {domain} is NONE")
                else:
                    print(f"\n\nDOMAIN: {domain}")
                    for field, parts in domain_data_dict.items():
                        print(f"    FIELD:{field}")
                        print(f"        VALUE:{parts[0]}")
                        print(f"        PATH:{parts[1]}")
                        n = n+1
                    print(f"\n\nDOMAIN: {domain} {n}\n\n")


def process_file(filepath):
    print(f"PROCESSING {filepath} ")
    logger.info(f"PROCESSING {filepath} ")
    base_name = os.path.basename(filepath)

    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        filename=f"logs/log_file_{base_name}.log",
        force=True,
        # level=logging.ERROR
        level=logging.WARNING
        # level=logging.INFO
        # level=logging.DEBUG
    )

    omop_data = parse_doc(filepath, get_meta_dict())
    # DDP.print_omop_structure(omop_data)
    if omop_data is not None or len(omop_data) < 1:
        print_omop_structure(omop_data)
    else:
        logger.error(f"FILE no data from {filepath}")


def main() :
    parser = argparse.ArgumentParser(
        prog='CCDA - OMOP Code Snooper',
        description="finds all code elements and shows what concepts the represent",
        epilog='epilog?')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--directory', help="directory of files to parse")
    group.add_argument('-f', '--filename', help="filename to parse")
    args = parser.parse_args()

    if args.filename is not None:
        process_file(args.filename)
    elif args.directory is not None:
        only_files = [f for f in os.listdir(args.directory) if os.path.isfile(os.path.join(args.directory, f))]
        for file in (only_files):
            if file.endswith(".xml"):
            	process_file(os.path.join(args.directory, file))
    else:
        logger.error("Did args parse let us  down? Have neither a file, nor a directory.")


    if False:  # for getting them on the Foundry
        from foundry.transforms import Dataset
        ccd_ambulatory = Dataset.get("ccda_ccd_b1_ambulatory_v2")
        ccd_ambulatory_files = ccd_ambulatory.files().download()
        ccd_ambulatory_path = ccd_ambulatory_files['CCDA_CCD_b1_Ambulatory_v2.xml']



if __name__ == '__main__':
    main()
