#import the following libraries and api key from config script
import requests
import json
import pandas as pd
from argparse import ArgumentParser
from config import api_key
from states import states

def main():
    parser = ArgumentParser()
    parser.add_argument('state', help='2 letter abbreviation of state/territory of choice', type=str)
    parser.add_argument('--overwrite', help='overwrite raw file or save as new file', action='store_true') 
    args, unknown = parser.parse_known_args() 
    if args.state not in states and args.state.lower() not in states:
        print('Abbreviation is invalid')
        exit(0)
    state_fips = states[args.state]
    response = requests.get("https://api.census.gov/data/2019/acs/acs5?get=NAME,GEO_ID,B19013_001E&for=block group:*&in=state:{}&in=county:*&in=tract:*&key={}".format(state_fips, api_key))
    print(response.status_code)
    result = json.loads(response.text)
    print(result)
    pd.DataFrame(result).to_csv(f'income_bg_{args.state.upper()}.csv')
    df = pd.read_csv(f'income_bg_{args.state.upper()}.csv')
    df.columns
    df.columns = ['index', 'NAME', 'GEO_ID', 'INCOME', 'state', 'county', 'tract', 'block_group']
    GEO_ID = df['GEO_ID']
    df[['US_Code', 'GEO_ID']] = GEO_ID.str.split("US", n=1, expand=True)
    del df['US_Code']
    df = df.drop(df.index[0])
    del df['index']
    if args.overwrite:
        df.to_csv(f'income_bg_{args.state.upper()}.csv')
    else:
        df.to_csv(f'income_bg_{args.state.upper()}_clean.csv')

if __name__ == '__main__':
    main()