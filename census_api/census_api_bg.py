import requests
import json
import pandas as pd
from argparse import ArgumentParser
from config import api_key
from states import states

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
    and the option to overwrite their inital raw file to prevent cluttering. After parsing the arguments
    it will then run a get request using the 2 requirements and the API key from the config file as format
    variables. This data will save as a csv into the directory with the inital raw data, which will then
    run through the 'clean' function as a dataframe. The new cleaned file will either save as a separate
    csv into the directory or will overwrite the raw file."""
    parser = ArgumentParser()
    parser.add_argument('state', help="2 letter abbreviation of state (DC and Puerto Rico included) of choice", type=str)
    parser.add_argument('var', help="Find a variable from the ACS 5-year detailed tables and enter the variable"+
                                " code (i.e. B19013_001E). If you want multiple variables separate by a comma with NO SPACE.")
    #add optional argument to change var columns to variable name of their choice
    parser.add_argument('--overwrite', help="overwrite raw file or save as new file", action='store_true')
    args, unknown = parser.parse_known_args()
    if args.state.upper() not in states:
        print('Abbreviation is invalid')
        exit(0)
    response = requests.get(f"https://api.census.gov/data/2019/acs/acs5?get=NAME,GEO_ID,{args.var}&for=block%20group:*&in=state:{states[args.state.upper()]}&in=county:*&in=tract:*&key={api_key}")
    #('Status Code: ', response.status_code) If the status code is 400 or any variant, print that it failed
    result = json.loads(response.text)
    #write function that saves the data into a data folder, creates one smaller folder for each state
    pd.DataFrame(result).to_csv(f'income_bg_{args.state.upper()}.csv')
    df = pd.read_csv(f'income_bg_{args.state.upper()}.csv')
    df = clean(df)
    if args.overwrite:
        df.to_csv(f'income_bg_{args.state.upper()}.csv', index=False)
    else:
        df.to_csv(f'income_bg_{args.state.upper()}_clean.csv', index=False)

if __name__ == '__main__':
    main()