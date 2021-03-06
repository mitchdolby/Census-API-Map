import requests
import json
import os
import pandas as pd
from argparse import ArgumentParser
from config import api_key
from state_dict import states

def clean(df):
    """This clean function drops an index column, removes the unusable half of the GEO ID, renames the
    columns, gives the nulls no value from -666666666, and drops an unneeded row"""
    del df['Unnamed: 0']
    df['1'] = df['1'].str.replace("1500000US", "")
    df.rename(columns={'1': 'GEO_ID'})
    df.columns = df.iloc[0]
    df = df.replace('-666666666', pd.NA)
    df.drop(df.index[0], inplace=True)
    return df

def main():
    """The 3 current arguments require the user to input the state/territory code, their desired variables,
    and the options to include specific words for the file name and to overwrite their inital raw file to 
    prevent cluttering. After parsing the arguments, it will then run a get request using the 2 requirements and the API key from the config file as format
    variables. This data will save as a csv into the directory with the inital raw data, which will then
    run through the 'clean' function as a dataframe. The new cleaned file will either save as a separate
    csv into the directory or will overwrite the raw file. The data will save in a new folder for its respective state"""
    parser = ArgumentParser()
    parser.add_argument('state', help="2 letter abbreviation of state (DC and Puerto Rico included) of choice", type=str)
    parser.add_argument('var', help="Find a variable from the ACS 5-year detailed tables and enter the variable"+
                                " code (i.e. B19013_001E). If you want multiple variables separate by a comma with NO SPACE.")
    parser.add_argument('--name', help="include key words in place (such as the variables) to make file name more "+ 
                                        "understandable. Write in the same format as the --var argument", type=str)
    parser.add_argument('--overwrite', help="overwrite raw file or save as new file", action='store_true')
    args, unknown = parser.parse_known_args()
    if args.state.upper() not in states:
        print('Abbreviation is invalid')
        exit(0)
    response = requests.get(f"https://api.census.gov/data/2019/acs/acs5?get=NAME,GEO_ID,{args.var}&for=block%20group:*&in=state:{states[args.state.upper()]}&in=county:*&in=tract:*&key={api_key}")
    if response.status_code == 400:
        print('Status Code 400- request failed')
    result = json.loads(response.text)
    if args.name is not None:
        name = args.name.replace(",", "_")
    state = args.state.lower()
    current_path = os.getcwd()
    data_path = os.path.join(current_path, r'states_data')
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    state_path = os.path.join(data_path, fr'{state}')
    if not os.path.exists(state_path):
        os.makedirs(state_path)
    os.chdir(state_path)
    #save raw
    if args.name is not None:
        pd.DataFrame(result).to_csv(fr'{state}_{name}_acs.csv')
        df = pd.read_csv(fr'{state}_{name}_acs.csv')
    else:
        pd.DataFrame(result).to_csv(fr'{state}_acs.csv')
        df = pd.read_csv(fr'{state}_acs.csv')
    df = clean(df)
    #save clean
    if args.name is not None:
        if args.overwrite:
            df.to_csv(fr'{state}_{name}_acs.csv', index=False)
        else:
            df.to_csv(fr'{state}_{name}_acs_clean.csv', index=False)
    else:
        if args.overwrite:
            df.to_csv(fr'{state}_acs.csv', index=False)
        else:
            df.to_csv(fr'{state}_acs_clean.csv', index=False)

if __name__ == '__main__':
    main()