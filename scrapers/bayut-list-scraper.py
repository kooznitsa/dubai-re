from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import json
from types import SimpleNamespace
import ast
import os


def get_listing(page_urls, file_name):

    data = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    for pg in page_urls:
        try:
            req = Request(url=pg, headers=headers)
            page = urlopen(req)
            print('Success: ', pg)
        except:
            print('Failed: ', pg)
            continue
        
        soup = BeautifulSoup(page, 'html.parser')

        script_text = "window['dataLayer'] = window['dataLayer'] || [];window['dataLayer'].push("
        script = soup.find(lambda tag:tag.name=='script' and script_text in tag.text).text

        for i in script_text:
            script = script.replace(i, '', 1)
        script = script.replace('"dynx_pagetype":"offerdetail"});', '"dynx_pagetype":"offerdetail"}')
        script = os.linesep.join([s for s in script.splitlines() if s])

        json_data = ast.literal_eval(json.dumps(script))
        j = json.loads(json_data, object_hook=lambda d: SimpleNamespace(**d))

        listing_id = j.listing_id or ''
        type = j.property_type or ''
        building = j.loc_4_name[1:-1] or ''
        district = j.loc_neighbourhood_name[1:-1] or ''
        neighborhood = j.loc_3_name[1:-1] or ''
        price = j.property_price or ''
        beds = j.property_beds or ''
        baths = j.property_baths_list or ''
        surface = j.property_land_area or ''
        prop_area = j.property_area or ''
        lat = j.latitude or ''
        long = j.longitude or ''
        highlights = j.listing_title or ''
        condition  = j.condition or ''
        purpose = j.purpose or ''

        desc = getattr(soup.find('span', attrs = {'class' : '_2a806e1e'}), 'text', None)
        completion = getattr(soup.find('span', attrs = {'class' : '_812aa185', 'aria-label' : 'Completion status'}), 'text', None)
        furnishing = getattr(soup.find('span', attrs = {'class' : '_812aa185', 'aria-label' : 'Furnishing'}), 'text', None)
        added_on = getattr(soup.find('span', attrs = {'class' : '_812aa185', 'aria-label' : 'Reactivated date'}), 'text', None)

        try:
            amenities = []
            am_spans = soup.findAll('span', attrs = {'class' : '_005a682a'})
            for i in am_spans:
                amenities.append(i.text)
        except:
            amenities = []

        # append data to list
        data.append((pg, listing_id, type, building, district, neighborhood, price, beds, baths, \
            surface, prop_area, lat, long, highlights, condition, purpose, \
            desc, completion, furnishing, amenities, added_on))


    # write data to CSV file
    columns = ['URL', 'listing_id', 'type', 'building', 'district', 'neighborhood', 'price', 'beds', 'baths', \
            'surface', 'prop_area', 'lat', 'long', 'highlights', 'condition', 'purpose', \
            'desc', 'completion', 'furnishing', 'amenities', 'added_on']

    with open(file_name, 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        writer.writerow((columns))
        writer.writerows(data)

    return data


path = '../data/bayut'

# # ready apartments
# ready_urls = path + '/urls/flats_ready.csv'
# with open(ready_urls, 'r', encoding='utf-8') as csv_file:
#     get_listing(csv_file, path + '/ready_flats.csv')

# # off-plan apartments
# offp_urls = path + '/urls/flats_offp.csv'
# with open(offp_urls, 'r', encoding='utf-8') as csv_file:
#     get_listing(csv_file, path + '/offp_flats.csv')

villas_urls = path + '/urls/villas.csv'
with open(villas_urls, 'r', encoding='utf-8') as csv_file:
    get_listing(csv_file, path + '/villas.csv')

townhouses_urls = path + '/urls/townhouses.csv'
with open(townhouses_urls, 'r', encoding='utf-8') as csv_file:
    get_listing(csv_file, path + '/townhouses.csv')

penthouses_urls = path + '/urls/penthouses.csv'
with open(penthouses_urls, 'r', encoding='utf-8') as csv_file:
    get_listing(csv_file, path + '/penthouses.csv')

villa_comp_urls = path + '/urls/villa_comp.csv'
with open(villa_comp_urls, 'r', encoding='utf-8') as csv_file:
    get_listing(csv_file, path + '/villa_comp.csv')

hotel_ap_urls = path + '/urls/hotel_ap.csv'
with open(hotel_ap_urls, 'r', encoding='utf-8') as csv_file:
    get_listing(csv_file, path + '/hotel_ap.csv')

res_plots_urls = path + '/urls/res_plots.csv'
with open(res_plots_urls, 'r', encoding='utf-8') as csv_file:
    get_listing(csv_file, path + '/res_plots.csv')

res_floors_urls = path + '/urls/res_floors.csv'
with open(res_floors_urls, 'r', encoding='utf-8') as csv_file:
    get_listing(csv_file, path + '/res_floors.csv')

res_bldgs_urls = path + '/urls/res_bldgs.csv'
with open(res_bldgs_urls, 'r', encoding='utf-8') as csv_file:
    get_listing(csv_file, path + '/res_bldgs.csv')

com_props_urls = path + '/urls/com_props.csv'
with open(com_props_urls, 'r', encoding='utf-8') as csv_file:
    get_listing(csv_file, path + '/com_props.csv')