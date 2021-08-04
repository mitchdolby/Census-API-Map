#import the following libraries and api key from config script
import requests
import json
import pandas as pd
from argparse import ArgumentParser
from config import api_key, url
from states import states
from arcgis.gis import GIS

def clean(df, value_input: str):
    df.columns = ['index', 'NAME', 'GEO_ID', value_input, 'state', 'county', 'tract', 'block group']
    geoid = df['GEO_ID']
    df[['US_Code', 'GEO_ID']] = geoid.str.split("US", n=1, expand=True)
    del df['US_Code']
    del df['index']
    df.drop(df.index[0], inplace=True)
    df = df[df[value_input] != '-666666666']
    return df

#def gis():


def main():
    parser = ArgumentParser()
    parser.add_argument('state', help='2 letter abbreviation of state (DC and Puerto Rico included) of choice', type=str)
    #parser.add_argument('geog', help='enter the geographic level: state, county, tract, or block group')
    parser.add_argument('var', help='find a variable from the ACS 5-year detailed tables')
    parser.add_argument('--overwrite', help='overwrite raw file or save as new file', action='store_true')
    #parser.add_argument('--gislog', help='options: online, pro')
    args, unknown = parser.parse_known_args()
    if args.state.upper() not in states:
        print('Abbreviation is invalid')
        exit(0)
    response = requests.get(url+f"?get=NAME,GEO_ID,{args.var}&for=block%20group:*&in=state:{states[args.state.upper()]}&in=county:*&in=tract:*&key={api_key}")
    print(response)
    print('Status Code: ', response.status_code)
    result = json.loads(response.text)
    print(result)
    pd.DataFrame(result).to_csv(f'income_bg_{args.state.upper()}.csv')
    df = pd.read_csv(f'income_bg_{args.state.upper()}.csv')
    df = clean(df, args.var)
    if args.overwrite:
        df.to_csv(f'income_bg_{args.state.upper()}.csv')
    else:
        df.to_csv(f'income_bg_{args.state.upper()}_clean.csv')

if __name__ == '__main__':
    main()