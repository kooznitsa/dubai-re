#!/usr/bin/python

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2.extras
from clean_data import create_new_df
from db_info import *


def create_table():
    psycopg2.extras.register_uuid()
    
    try:
        connection = psycopg2.connect(**db_connection_info)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        cursor.execute('DROP TABLE IF EXISTS dubai_flats;')
        connection.commit()
        print('Existing table is deleted')

        cursor.execute("""CREATE TABLE dubai_flats (
                id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
                listing_id INTEGER,
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
                owner_id INTEGER,
                featured_image VARCHAR(255) NULL,
                created VARCHAR(255),
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
                luxury INTEGER
            );""")
        connection.commit()
        print('Table is created')

        df = create_new_df()
        print('File is cleaned')

        for index, row in df.iterrows():
            id = row.iloc[0]
            listing_id = int(row.iloc[1])
            URL = row.iloc[2] or ''
            building = row.iloc[3] or ''
            district = row.iloc[4] or ''
            neighborhood = row.iloc[5] or ''
            price = int(row.iloc[6])
            beds = float(row.iloc[7])
            baths = int(row.iloc[8])
            surface = float(row.iloc[9])
            lat = float(row.iloc[10])
            long = float(row.iloc[11])
            highlights = row.iloc[12] or ''
            furnishing = row.iloc[13] or ''
            amenities = row.iloc[14] or ''
            owner_id = int(row.iloc[15])
            featured_image = row.iloc[16] or ''
            created = row.iloc[17] or ''
            completion_year = row.iloc[18] or ''
            floor = row.iloc[19] or ''
            views = int(row.iloc[20])
            discounted = int(row.iloc[21])
            cheap = int(row.iloc[22])
            distressed = int(row.iloc[23])
            investment = int(row.iloc[24])
            tenanted = int(row.iloc[25])
            vacant = int(row.iloc[26])
            metro = int(row.iloc[27])
            furnished = int(row.iloc[28])
            condition = int(row.iloc[29])
            upgraded = row.iloc[30] or ''
            luxury = int(row.iloc[31])

            cursor.execute("""INSERT INTO dubai_flats VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", \
                (id, listing_id, URL, building, district, neighborhood, price, beds, baths, surface, lat, long, \
                highlights, furnishing, amenities, owner_id, featured_image, created, completion_year, floor, \
                views, discounted, cheap, distressed, investment, tenanted, vacant, metro, furnished, condition, \
                upgraded, luxury))

        connection.commit()
        print('Data is inserted into table')

        connection.close()
        cursor.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    create_table()