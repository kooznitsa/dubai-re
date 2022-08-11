#!/usr/bin/python

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from clean_data import create_new_df
from db_info import *


def create_table():
    try:
        connection = psycopg2.connect(**db_connection_info)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        cursor.execute('DROP TABLE IF EXISTS ready_flats;')
        connection.commit()
        print('Existing table is deleted')

        cursor.execute("""CREATE TABLE ready_flats (
                listing_id INTEGER PRIMARY KEY,
                URL VARCHAR(255),
                building VARCHAR(255),
                district VARCHAR(255),
                neighborhood VARCHAR(255),
                price INTEGER,
                beds FLOAT,
                baths INTEGER,
                surface FLOAT,
                lat FLOAT,
                long FLOAT,
                highlights TEXT,
                furnishing VARCHAR(255),
                amenities TEXT,
                completion_year VARCHAR(255),
                floor VARCHAR(255),
                views INTEGER,
                discounted INTEGER,
                cheap INTEGER,
                distressed INTEGER,
                investment INTEGER,
                tenanted INTEGER,
                vacant INTEGER,
                metro INTEGER,
                furnished INTEGER,
                condition INTEGER,
                upgraded VARCHAR(255),
                luxury INTEGER,
                price_sqf FLOAT,
                median_sqf FLOAT,
                diff_percent FLOAT,
                valuation VARCHAR(255)
            );""")
        connection.commit()
        print('Table is created')

        df = create_new_df()
        print('File is cleaned')

        for index, row in df.iterrows():
            listing_id = int(row.iloc[0])
            URL = row.iloc[1] or ''
            building = row.iloc[2] or ''
            district = row.iloc[3] or ''
            neighborhood = row.iloc[4] or ''
            price = int(row.iloc[5])
            beds = float(row.iloc[6])
            baths = int(row.iloc[7])
            surface = float(row.iloc[8])
            lat = float(row.iloc[9])
            long = float(row.iloc[10])
            highlights = row.iloc[11] or ''
            furnishing = row.iloc[12] or ''
            amenities = row.iloc[13] or ''
            completion_year = row.iloc[14] or ''
            floor = row.iloc[15] or ''
            views = int(row.iloc[16])
            discounted = int(row.iloc[17])
            cheap = int(row.iloc[18])
            distressed = int(row.iloc[19])
            investment = int(row.iloc[20])
            tenanted = int(row.iloc[21])
            vacant = int(row.iloc[22])
            metro = int(row.iloc[23])
            furnished = int(row.iloc[24])
            condition = int(row.iloc[25])
            upgraded = row.iloc[26] or ''
            luxury = int(row.iloc[27])
            price_sqf = float(row.iloc[28])
            median_sqf = float(row.iloc[29])
            diff_percent = float(row.iloc[30])
            valuation = row.iloc[31] or ''

            cursor.execute("""INSERT INTO ready_flats VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", \
                (listing_id, URL, building, district, neighborhood, price, beds, baths, surface, lat, long, \
                highlights, furnishing, amenities, completion_year, floor, views, discounted, cheap, \
                distressed, investment, tenanted, vacant, metro, furnished, condition, upgraded, \
                luxury, price_sqf, median_sqf, diff_percent, valuation))

        connection.commit()
        print('Data is inserted into table')

        connection.close()
        cursor.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    create_table()