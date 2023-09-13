from bs4 import BeautifulSoup
import requests
import csv
import os

zillow_link = input("Please input valid Zillow page link: ")

form_link = "https://docs.google.com/forms/d/e/1FAIpQLSe-wljUznVOqzInZIX7fUwypV8xK0autYUHueNamJCZQmH7yQ/viewform?usp=sf_link"

headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Accept-Language': 'en-US'
}

response = requests.get(url=zillow_link, timeout=5, headers=headers)

response.raise_for_status()
webpage = response.text

soup = BeautifulSoup(webpage, 'html.parser')

#addresses = soup.select(selector="div a address")

'''all_addresses = [address.getText() for address in addresses]
print(all_addresses)
prices = soup.select(selector="a div div span")
all_prices = [price.getText() for price in prices]
print(all_prices)'''

prices = soup.find_all("span", {'data-test': 'property-card-price'})
all_prices = [link.getText() for link in prices]
print(all_prices)

addresses = soup.find_all("address", {'data-test': 'property-card-addr'})
all_addresses = [address.getText() for address in addresses]
print(all_addresses)

links = soup.find_all("a", {'data-test': 'property-card-link'})
all_links = []
for link in links:
    if link['href'][0] == '/':
        if f"https://www.zillow.com{link['href']}" in all_links:
            continue
        else:
            all_links.append(f"https://www.zillow.com{link['href']}")
    else:
        if link['href'] in all_links:
            continue
        else:
            all_links.append(link['href'])

print(all_links)

fields = ["Address", 'Price', 'Zillow Link']

rows = []
for i in range(len(all_links)):
    new_row = [all_addresses[i], all_prices[i], all_links[i]]
    rows.append(new_row)

if os.path.exists('listinginfo.csv'):
    with open('listinginfo.csv', 'a') as file:
        write = csv.writer(file)
        write.writerows(rows)

else:
    with open('listinginfo.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow(fields)
        write.writerows(rows)