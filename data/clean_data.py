#!/usr/bin/python

import pandas as pd
from ast import literal_eval
import re
import uuid


df = pd.read_csv('data/bayut/ready_flats.csv', converters={'amenities': literal_eval})

views = ['view', 'views', 'seaview', 'overlooking', 'facing']
luxury = ['luxury', 'luxurious', 'luxuriously', 'premium']
discounted = ['reduced price', 'priced reduced', 'price reduction', 'discounted price', 'negotiable', \
            'price drop', 'price dropped']
cheap = ['affordable', 'cheap', 'cheapest', 'well-priced', 'well priced', 'economical', 'best price']
distressed = ['distress', 'distressed']
upgraded = ['upgraded', 'partially upgraded', 'fully upgraded', 'semi-upgraded', 'semi upgraded', 'renovated']
condition = ['superb condition', 'brand new', 'new building', 'high quality',\
    'well maintained', 'well-maintained', 'high-end finishing', 'excellent condition', 'great condition',\
    'pristine condition', 'immaculate condition','amazing condition', 'mint condition', 'bes condition', \
    'best condition', 'good condition', 'new condition', 'perfect condition', 'tip-top condition', \
    'turnkey condition', 'top condition', 'impeccable condition','mint condiition']
investment = ['investment', 'investor deal', 'investors deal', 'roi', 'investor visa', 'high returns']
tenanted = ['tenanted', 'rented', 'tenant']
vacant = ['vacant']
metro = ['close to metro', 'next to metro', 'near metro']
furnished = ['furnished', 'unfurnished', 'semi furnished', 'semi-furnished']
studio = ['studio']


def get_years(df):
    completion_years = []
    
    for lists in df['amenities']:
        str = ','.join(lists)
        m = re.search('Completion Year: (\d{4})', str)
        if m:
            completion_years.append(m.group(1))
        else:
            completion_years.append(0)
            
    df['completion_year'] = completion_years
    
    
def get_floors(df):
    floors = []
    
    for lists in df['amenities']:
        str = ','.join(lists)
        m = re.search('Floor: (\d+)', str)
        if m:
            floors.append(m.group(1))
        else:
            floors.append('')
            
    df['floor'] = floors
    

def get_features(df, f_list, col_name, col_list):
    for row in df['highlights'].str.lower():
        if any(x in row for x in f_list):
            col_list.append(1)
        else:
            col_list.append(0)
    
    if len(col_list) == len(df['highlights']):
        df[col_name] = col_list
        
        
def get_upgraded(df):
    upgraded_p = []
    
    for row in df['highlights'].str.lower():
        row = row.split(', ')
        y = ''
        for x in upgraded:
            if x in row:
                y = x
                break

        upgraded_p.append(y)
        
    if len(upgraded_p) == len(df['highlights']):
        df['upgraded'] = upgraded_p


def get_luxury(df):
    luxury_col = []
    
    for row in df['highlights'].str.lower():
        row = row.split(', ')
        y = 0
        for x in condition:
            if x in row:
                y = 1
                break

        luxury_col.append(y)
        
    if len(luxury_col) == len(df['highlights']):
        df['luxury'] = luxury_col


def clean_data(df):
    df = df.drop_duplicates(subset='listing_id', keep='first')
    df['id'] = [uuid.uuid4() for _ in range(len(df.index))]
    df['owner_id'] = 1
    df['featured_image'] = ''
    df['baths'] = df['baths'].apply(lambda x: x.replace('[','').replace(']','').replace("'",''))
    df['highlights'] = df['highlights'].apply(lambda x: x.replace('|',',').replace(' ,',','))
    df[['baths', 'beds']] = df[['baths', 'beds']].apply(pd.to_numeric, errors='coerce')
    
    df = df[(df['surface'] <= 4000)]
    df = df[df['beds'].notna()]
    
    global df_ready
    df_ready = df[(df['completion'] == 'Ready')]

    df_ready = df_ready[['id', 'listing_id', 'URL', 'building', 'district', 'neighborhood', \
        'price', 'beds', 'baths', 'surface', 'lat', 'long', 'highlights', 'furnishing', 'amenities', \
        'owner_id', 'featured_image', 'created']]
    df_ready = df_ready[~df_ready.index.duplicated(keep='first')]    

    get_years(df_ready)
    get_floors(df_ready)

    get_features(df_ready, views, 'views', [])
    get_features(df_ready, discounted, 'discounted', [])
    get_features(df_ready, cheap, 'cheap', [])
    get_features(df_ready, distressed, 'distressed', [])
    get_features(df_ready, investment, 'investment', [])
    get_features(df_ready, tenanted, 'tenanted', [])
    get_features(df_ready, vacant, 'vacant', [])
    get_features(df_ready, metro, 'metro', [])
    get_features(df_ready, furnished, 'furnished', [])
    get_features(df_ready, condition, 'condition', [])
    
    get_upgraded(df_ready)
    get_luxury(df_ready)
    
    return df_ready


def create_new_df():
    df_ready = clean_data(df)
    print(df_ready.info())
    return df_ready