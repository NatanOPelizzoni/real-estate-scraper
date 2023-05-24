import re
import math
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36'}

data = {}

links = {
    'Sales': {
        'https://www.conceitoimoveistapejara.com.br/comprar-imoveis/apartamentos-tapejara/',
        'https://www.conceitoimoveistapejara.com.br/comprar-imoveis/casas-tapejara/',
        'https://www.conceitoimoveistapejara.com.br/comprar-imoveis/comercial-tapejara/',
        'https://www.conceitoimoveistapejara.com.br/comprar-imoveis/terrenos-tapejara/',
    },
    'Rents': {
        'https://www.conceitoimoveistapejara.com.br/alugar-imoveis/apartamentos-tapejara/',
        'https://www.conceitoimoveistapejara.com.br/alugar-imoveis/casas-tapejara/',
        'https://www.conceitoimoveistapejara.com.br/alugar-imoveis/comercial-tapejara/',
        'https://www.conceitoimoveistapejara.com.br/alugar-imoveis/terrenos-tapejara/',
    }
}

for group_type in links:
    if not group_type in data:
        data[group_type] = {}

    for link in links[group_type]:
        link_parts = link.split('-')
        category_type = link_parts[-2].split('/')[-1]
        
        link_parts = link.split('.')
        real_estate_name = link_parts[1]
        
        if not category_type in data[group_type]:
            data[group_type][category_type] = {}

        site = requests.get(link, headers=headers)
        soup = BeautifulSoup(site.content, 'html.parser')

        quantity_text_items = soup.find('h2', {'class': 'titulo-encontrados'}).get_text().strip()
        index = quantity_text_items.find(' ')
        quantity_items = quantity_text_items[:index]
        last_page = math.ceil(int(quantity_items) / 24)
        
        properties_links = []
        
        for i in range(1, last_page+1):
            url_page = f'{link}&pg={i}'
            site_page = requests.get(url_page, headers=headers)
            soup_page = BeautifulSoup(site_page.content, 'html.parser')
            properties = soup_page.find_all('a', {'class': 'listing-img-container'})
            for property in properties:
                properties_links.append(property['href'])
        
        category_data = []
        
        for link_property in properties_links:
            site_property = requests.get(link_property, headers=headers)
            soup_property = BeautifulSoup(site_property.content, 'html.parser')
            
            div_price = soup_property.find('div', {'class': 'col-price-and-print'})
            span_price = soup_property.find('span', {'class': 'value-real-number'})
            if(span_price):
                property_price = float(
                    span_price.get_text().strip()
                    .replace('R$ ', '')
                    .replace('.', '')
                    .replace(',', '.')
                )
            else:
                property_price = None
            
            div_title = soup_property.find('div', {'class': 'property-title'})
            
            div_title.h2.span.extract()
            property_name = div_title.h2.get_text().strip()
            
            span_address = div_title.find('span', {'class': 'sp-address-property'}).get_text().strip()
            address_parts = span_address.split(',')
            local_parts = address_parts[1].split('-')
            
            city_name = local_parts[1].split('/')[0].strip()
            abbreviation_uf = local_parts[1].split('/')[1].strip()
            neighborhood_name = local_parts[0].strip()
            address = address_parts[0].strip()
            
            string_bedrooms = div_title.find(class_="fa-bed")
            if string_bedrooms:
                partes_quartos = string_bedrooms.parent.get_text().strip().split('.')
                bedrooms_number = int(re.findall(r'\d+', partes_quartos[0])[0])
                if len(partes_quartos[1]) > 0:
                    suites_number = int(re.findall(r'\d+', partes_quartos[1])[0])

            bedrooms_number = bedrooms_number or None
            suites_number = suites_number or None
            
            div_characteristics = soup_property.find('div', {'class': 'property-description'})
            
            ul_information = div_characteristics.find('ul', {'class':'listing-features'})

            string_vacancies = ul_information.find('li', {'class':'vagas'})
            if string_vacancies:
                car_vacancies_number = int(re.findall(r'\d+', string_vacancies.get_text().strip())[0])
            car_vacancies_number = car_vacancies_number or None

            string_property_area = ul_information.find('li', {'class':'area'})
            if string_property_area:
                property_area_size = float(
                    string_property_area.get_text()
                    .strip()
                    .split(':')[1]
                    .replace(' m²', '')
                    .replace('.', '')
                    .replace(',', '.')
                )
            property_area_size = property_area_size or None

            string_private_property_area = ul_information.find('li', {'class':'area-privativa'})
            if string_private_property_area:
                private_property_area = float(
                    string_private_property_area.get_text()
                    .strip()
                    .split(':')[1]
                    .replace(' m²', '')
                    .replace('.', '')
                    .replace(',', '.')
                )
            private_property_area = private_property_area or None

            string_furniture = ul_information.find('li', {'class':'mobilia'})
            if string_furniture:
                furniture = string_furniture.get_text().split(':')[1].strip()
            furniture = furniture or None

            string_floor = ul_information.find('li', {'class':'previsao'})
            if string_floor:
                floor = string_floor.get_text().split(':')[1].strip()
            floor = floor or None
            
            category_data.append({
                'real_estate_name':real_estate_name,
                'property_price':property_price,
                'property_name':property_name,
                'city_name':city_name,
                'abbreviation_uf':abbreviation_uf,
                'neighborhood_name':neighborhood_name,
                'address':address,
                'bedrooms_number':bedrooms_number,
                'suites_number':suites_number,
                'car_vacancies_number':car_vacancies_number,
                'property_area_size':property_area_size,
                'private_property_area':private_property_area,
                'furniture':furniture,
                'floor':floor,
            })

        data[group_type][category_type] = category_data