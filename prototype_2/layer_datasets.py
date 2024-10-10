#!/usr/bin/env python3

import argparse
import os
import pandas as pd



import logging
import prototype_2.data_driven_parse as DDP
from prototype_2.metadata import get_meta_dict


import lxml
print(lxml.__file__)

logger = logging.getLogger(__name__)


def show_column_dict(column_dict):
    for key,val in column_dict.items():
        print(f" key:{key} length(val):{len(val)}")

def create_omop_domain_dataframes(omop_data, filepath):
    """ transposes the rows into columns,
        creates a Pandas dataframe
    """
    df_dict = {}
    for domain_name, domain_list in omop_data.items():
        # Transpose to a dictoinary of named columns.

        # Initialize a dictionary of columns from the first row
        column_dict = {}
        if domain_list is None or len(domain_list) < 1:
            logger.error(f"No data for {domain_name} from {filepath}")
        else:
            for field, parts in domain_list[0].items():
                column_dict[field] = []

        # Add the data from all the rows
        if domain_list is None or len(domain_list) < 1:
            logger.error(f"No data for {domain_name} from {filepath}")
        else:
            for domain_data_dict in domain_list:
                for field, parts in domain_data_dict.items():
                    column_dict[field].append(parts[0])

        # create a Pandas dataframe from the data_dict
        try:
            domain_df = pd.DataFrame(column_dict)
        except ValueError as ve:
            logger.error(f"ERROR {ve}")
            show_column_dict(column_dict)
        df_dict[domain_name] = domain_df

    return df_dict


def write_csvs_from_dataframe_dict(df_dict, file_name, folder):
    """ writes a CSV file for each dataframe
        uses the key of the dict as filename
    """
    for domain_name, domain_dataframe in df_dict.items():
        domain_dataframe.to_csv(f"{folder}/{file_name}__{domain_name}.csv",
                                sep=",", header=True, index=False)


def process_file(filepath):
    """ processes file, creates dataset and writes csv
        returns dataset
    """
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

    omop_data = DDP.parse_doc(filepath, get_meta_dict())
    # DDP.print_omop_structure(omop_data)
    if omop_data is not None or len(omop_data) < 1:
        dataframe_dict = create_omop_domain_dataframes(omop_data, filepath)
    else:
        logger.error(f"no data from {filepath}")
    write_csvs_from_dataframe_dict(dataframe_dict, base_name, "output")
    
    return dataframe_dict

def dict_summary(my_dict):
    for key in my_dict:
        logger.info(f"Summary {key} {len(mh_dict[key])}")

def main():

    parser = argparse.ArgumentParser(
        prog='CCDA - OMOP Code Snooper',
        description="finds all code elements and shows what concepts the represent",
        epilog='epilog?')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--directory', help="directory of files to parse")
    group.add_argument('-f', '--filename', help="filename to parse")
    args = parser.parse_args()

    omop_data_dict = {}
    if args.filename is not None:
        process_file(args.filename)
    elif args.directory is not None:
        only_files = [f for f in os.listdir(args.directory) if os.path.isfile(os.path.join(args.directory, f))]
        for file in (only_files):
            if file.endswith(".xml"):
                new_data_dict = process_file(os.path.join(args.directory, file))
                for key in new_data_dict:
                    if key in omop_data_dict and omop_data_dict[key] is not None:
                        if new_data_dict[key] is  not None:
                            omop_data_dict[key] = pd.concat([omop_data_dict[key], new_data_dict[key]])
                    else:
                        omop_data_dict[key]= new_data_dict[key]
                    logger.info(f"{file} {key} {len(omop_data_dict)} {omop_data_dict[key].shape} {new_data_dict[key].shape}")
    else:
        logger.error("Did args parse let us  down? Have neither a file, nor a directory.")

        ## ccd_ambulatory_path = ccd_ambulatory_files['CCDA_CCD_b1_Ambulatory_v2.xml']  ## FIX oddity from a merge?


    for key in omop_data_dict:
        logger.info(f"Summary {key} {omop_data_dict[key].shape}")

    # EXPORT VARS
    export_person = omop_data_dict['Person']
    from foundry.transforms import Dataset
    # person = Dataset.get("person")
    person = Dataset.get("person_second_try")
    person.write_table(export_person)


    export_observation = omop_data_dict['Observation']
    observation = Dataset.get("observation")
    observation.write_table(export_observation)
    
    export_measurement = omop_data_dict['Measurement']
    measurement = Dataset.get("measurement")
    measurement.write_table(export_measurement)
    
    export_visit = omop_data_dict['Visit']
    visit = Dataset.get("visit")
    visit.write_table(export_visit)

if __name__ == '__main__':
    main()
