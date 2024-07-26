#!/usr/bin/env python3

import data_driven_parse as DDP
import pandas as PD

def create_omop_domain_dataframes(omop_data):
    """ transposes the rows into columns, 
        creates a Pandas dataframe
    """
    df_dict = {}
    for domain_name, domain_list in omop_data.items():
        # Transpose to a dictoinary of named columns.

        # Initialize a dictionary of columns from the first row
        column_dict = {}
        for field, parts in domain_list[0].items():
            column_dict[field] = []

        # Add the data from all the rows
        for domain_data_dict in domain_list:
            for field, parts in domain_data_dict.items():
                column_dict[field].append(parts)


        # create a Pandas dataframe from the data_dict
        domain_df = PD.DataFrame(column_dict)
        df_dict[domain_name] = domain_df

    return df_dict

def write_csvs_from_dataframe_dict(df_dict):
    """ writes a CSV file for each dataframe 
        uses the key of the dict as filename
    """
    for domain_name, domain_dataframe in df_dict.items():
        domain_dataframe.to_csv(domain_name + ".csv", sep=",", header=True, index=False)

if __name__ == '__main__':
    ccd_ambulatory_path = '../resources/CCDA_CCD_b1_Ambulatory_v2.xml'
    if False: # set True when in Foundry. FIX make this a config value?
        # how to find the file path in Foundry,
        from foundry.transforms import Dataset
        ccd_ambulatory = Dataset.get("ccda_ccd_b1_ambulatory_v2")
        ccd_ambulatory_files = ccd_ambulatory.files().download()
        ccd_ambulatory_path = ccd_ambulatory_files['CCDA_CCD_b1_Ambulatory_v2.xml']
 
    omop_data = DDP.parse_doc(ccd_ambulatory_path) 
    DDP.print_omop_structure(omop_data) 
    dataframe_dict = create_omop_domain_dataframes(omop_data)
    write_csvs_from_dataframe_dict(dataframe_dict)


