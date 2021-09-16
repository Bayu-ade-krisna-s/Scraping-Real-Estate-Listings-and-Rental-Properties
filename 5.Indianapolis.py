from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.parse

address = []
bedrooms = []
bathrooms = []
area = []
year_built = []
parking = []
price = []

# url part 1
url_part_1 = 'https://www.trulia.com'

for i in range(1, 26):

    # website
    website = 'https://www.trulia.com/IN/Indianapolis/' + str(i) + '_p/'

    # request
    response = requests.get(website)

    # soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # result container
    result_container = soup.find_all('li', {'class': 'SearchResultsList__WideCell-b7y9ki-2'})

    # results update
    results_update = []

    # only results with attribute "data-testid"
    for r in result_container:
        if r.has_attr('data-testid'):
            results_update.append(r)

    # relative url
    relative_url = []

    # loop thorugh results
    for item in results_update:

        for link in item.find_all('div', {'data-testid': 'property-card-details'}):
            relative_url.append(link.find('a').get('href'))

    # empty list (url joined)
    url_joined = []

    for link_2 in relative_url:
        url_joined.append(urllib.parse.urljoin(url_part_1, link_2))

    # loop through all joined links
    for link in url_joined:
        response = requests.get(link)

        # create soup object
        soup = BeautifulSoup(response.content, 'html.parser')

        # address
        try:
            address.append(soup.find('span', {'data-testid': 'home-details-summary-headline'}).get_text())
        except:
            address.append('')

        # bedrooms
        try:
            bedrooms.append(soup.find('li', {'data-testid': 'bed'}).get_text())
        except:
            bedrooms.append('')

        # bathrooms
        try:
            bathrooms.append(soup.find('li', {'data-testid': 'bath'}).get_text())
        except:
            bathrooms.append('')

        # area
        try:
            area.append(soup.find('li', {'data-testid': 'floor'}).get_text())
        except:
            area.append('')

        # year_built
        try:
            year_built.append(soup.find('div', string='Year Built').findNext('div').get_text())
        except:
            year_built.append('')

        # parking
        try:
            parking.append(soup.find('div', string='Parking').findNext('div').get_text())
        except:
            parking.append('')

        # price
        try:
            price.append(soup.find('h3', {'data-testid': 'on-market-price-details'}).get_text())
        except:
            price.append('')

        # create a dictionary with results
        output = {'Address': address, 'Bedrooms': bedrooms, 'Bathrooms': bathrooms, 'Area': area,
                  'Year Built': year_built, 'Parking': parking, 'Price': price}


df = pd.DataFrame(output)
df['Location'] = 'Indianapolis'
df.to_excel('dataframe_indianapolis.xlsx', index=False)
