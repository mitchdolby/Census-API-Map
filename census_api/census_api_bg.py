#import the following libraries and api key from config script
import requests
import json
import pandas as pd
from argparse import ArgumentParser
from config import api_key
from states import states

def clean(df):
    del df['Unnamed: 0']
    df['1'] = df['1'].str.replace("1500000US", "")
    df.rename(columns={'1': 'GEO_ID'})
    df.columns = df.iloc[0]
    df = df.replace('-666666666', pd.NA)
    df.drop(df.index[0], inplace=True)
    return df

def main():
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
    #print('Status Code: ', response.status_code)
    result = json.loads(response.text)
    pd.DataFrame(result).to_csv(f'income_bg_{args.state.upper()}.csv')
    df = pd.read_csv(f'income_bg_{args.state.upper()}.csv')
    df = clean(df)
    if args.overwrite:
        df.to_csv(f'income_bg_{args.state.upper()}.csv', index=False)
    else:
        df.to_csv(f'income_bg_{args.state.upper()}_clean.csv', index=False)

if __name__ == '__main__':
    main()