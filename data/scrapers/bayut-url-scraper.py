from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import pandas as pd

def get_urls(page_url, file_name):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
		
    links_list = []

    for pg in page_url:
        try:
            req = Request(url = pg, headers = headers)
            page = urlopen(req)
            soup = BeautifulSoup(page, 'html.parser')
        except:
            continue

        # collect href links
        links = soup.find_all('a', attrs = {'class' : '_287661cb'})
        for link in links:
            links_list.append(link['href'])

    # write links to a file
    with open(file_name, 'w', encoding='utf-8', errors='ignore') as csv_file:
        for link in links_list:
            write = csv.writer(csv_file, lineterminator='\n')
            write.writerow(['https://www.bayut.com' + link])

    # drop duplicated values
    data = pd.read_csv(file_name)
    data.drop_duplicates(keep='first', inplace=True)
    data.to_csv(file_name, index=False)


# flats_ready = ['https://www.bayut.com/for-sale/apartments/dubai/?completion_status=ready']
# for num in range(2, 1575):
#     url = f'https://www.bayut.com/for-sale/apartments/dubai/page-{num}/?completion_status=ready'
#     flats_ready.append(url)

# flats_offp = ['https://www.bayut.com/for-sale/apartments/dubai/?completion_status=off-plan']
# for num in range(2, 585):
#     url = f'https://www.bayut.com/for-sale/apartments/dubai/page-{num}/?completion_status=off-plan'
#     flats_offp.append(url)

# villas = ['https://www.bayut.com/for-sale/villas/dubai/']
# for num in range(2, 700):
#     url = f'https://www.bayut.com/for-sale/villas/dubai/page-{num}/'
#     villas.append(url)

# townhouses = ['https://www.bayut.com/for-sale/townhouses/dubai/']
# for num in range(2, 358):
#     url = f'https://www.bayut.com/for-sale/townhouses/dubai/page-{num}/'
#     townhouses.append(url)

# penthouses = ['https://www.bayut.com/for-sale/penthouse/dubai/']
# for num in range(2, 55):
#     url = f'https://www.bayut.com/for-sale/penthouse/dubai/page-{num}/'
#     penthouses.append(url)

# villa_comp = ['https://www.bayut.com/for-sale/villa-compound/dubai/']
# for num in range(2, 3):
#     url = f'https://www.bayut.com/for-sale/villa-compound/dubai/page-{num}/'
#     villa_comp.append(url)

# hotel_ap = ['https://www.bayut.com/for-sale/hotel-apartments/dubai/']
# for num in range(2, 19):
#     url = f'https://www.bayut.com/for-sale/hotel-apartments/dubai/page-{num}/'
#     hotel_ap.append(url)

# res_plots = ['https://www.bayut.com/for-sale/residential-plots/dubai/']
# for num in range(2, 60):
#     url = f'https://www.bayut.com/for-sale/residential-plots/dubai/page-{num}/'
#     res_plots.append(url)

# res_floors = ['https://www.bayut.com/for-sale/residential-floors/dubai/']
# for num in range(2, 4):
#     url = f'https://www.bayut.com/for-sale/residential-floors/dubai/page-{num}/'
#     res_floors.append(url)

# res_bldgs = ['https://www.bayut.com/for-sale/residential-building/dubai/']
# for num in range(2, 10):
#     url = f'https://www.bayut.com/for-sale/residential-building/dubai/page-{num}/'
#     res_bldgs.append(url)

# com_props = ['https://www.bayut.com/for-sale/commercial/dubai/']
# for num in range(2, 153):
#     url = f'https://www.bayut.com/for-sale/commercial/dubai/page-{num}/'
#     com_props .append(url)

rent_res = ['https://www.bayut.com/to-rent/property/dubai/?rent_frequency=any']
for num in range(2, 1970):
    url = f'https://www.bayut.com/to-rent/property/dubai/page-{num}/?rent_frequency=any/'
    rent_res .append(url)

# get_urls(flats_ready, '../data/bayut/urls/flats_ready.csv')
# get_urls(flats_offp, '../data/bayut/urls/flats_offp.csv')
# get_urls(villas, '../data/bayut/urls/villas.csv')
# get_urls(townhouses, '../data/bayut/urls/townhouses.csv')
# get_urls(penthouses, '../data/bayut/urls/penthouses.csv')
# get_urls(villa_comp, '../data/bayut/urls/villa_comp.csv')
# get_urls(hotel_ap, '../data/bayut/urls/hotel_ap.csv')
# get_urls(res_plots, '../data/bayut/urls/res_plots.csv')
# get_urls(res_floors, '../data/bayut/urls/res_floors.csv')
# get_urls(res_bldgs, '../data/bayut/urls/res_bldgs.csv')
# get_urls(com_props, '../data/bayut/urls/com_props.csv')

get_urls(rent_res, '../data/bayut/rent/urls/rent_res.csv')