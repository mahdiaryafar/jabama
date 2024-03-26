import requests
import json


def request(city, start_date, end_date, capacity,  page_number=1, page_size=16):  #

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Referer': 'https://www.jabama.com/',
        'ab-channel': 'GuestDesktop,2.34.1,Windows,10,undefined,ac367cbd-7b8b-4c74-a35b-cd2d3777075a',
        'X-User-Experiments': '1706603592491000-TEST_EXPERIMENT,DUMMY_EXPERIMENT,CANCELLATION_RESELL',
        'Origin': 'https://www.jabama.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Connection': 'keep-alive',
    }

    params = {
        'allowEmptyCity': 'true',
        'hasUnitRoom': 'true',
        'guarantees': 'false',
        'platform': 'desktop',
    }

    json_data = {
        'page-size': page_size,
        'capacity': capacity,
        'page-number': page_number,
        'date': {
            'start': start_date,
            'end': end_date,
        },
    }

    response = requests.post(
        f'https://gw.jabama.com/api/v4/keyword/{city}', params=params, headers=headers, json=json_data)
    return response.json()

# ----------------------------------------------------------------------------------------------------


def extract_data(json):
    items = []
    for item in json['result']['items']:
        data = {}

        data['areaSize'] = item['accommodationMetrics']['areaSize']
        data['bathroomsCount'] = item['accommodationMetrics']['bathroomsCount']
        data['bedroomsCount'] = item['accommodationMetrics']['bedroomsCount']
        data['buildingSize'] = item['accommodationMetrics']['buildingSize']
        data['iranianToiletsCount'] = item['accommodationMetrics']['iranianToiletsCount']
        data['toiletsCount'] = item['accommodationMetrics']['toiletsCount']

        data['amenities'] = item['amenities']
        data['name'] = item['name']
        data['kind'] = item['kind']
        data['min_night'] = item['min_night']
        data['min_price'] = item['min_price']
        data['payment_type'] = item['payment_type']
        data['region'] = item['region']
        data['reservation_type'] = item['reservation_type']
        data['payment_type'] = item['payment_type']
        data['payment_type'] = item['payment_type']
        data['type'] = item['type']
        data['verified'] = item['verified']
        data['status'] = item['status']
        data['placeType'] = item['placeType']

        data['province'] = item['location']['province']
        data['city'] = item['location']['city']
        data['geo'] = item['location']['geo']

        data['rate_count'] = item['rate_review']['count']
        data['rate_score'] = item['rate_review']['score']

        data['capacity_base'] = item['capacity']['base']
        data['capacity_extra'] = item['capacity']['extra']

        data['mainPrice'] = item['price']['mainPrice']
        data['discountedPrice'] = item['price']['discountedPrice']
        data['price_perNight'] = item['price']['perNight']

        code = item['code']
        item_type = data['type']

        data['url'] = f'https://www.jabama.com/stay/{item_type}-{code}'

        items.append(data)

    return items

# ----------------------------------------------------------------------------------------------------


def write(text):
    with open("sample.json", "a") as File:
        json.dump(text, File)

# ----------------------------------------------------------------------------------------------------


def for_all_items(input_data):
    done = False
    result = []
    page_num = 1
    while not done:
        json_data = request(**input_data, page_number=page_num)

        if not json_data['result']['items']:
            done = True
        else:
            result += extract_data(json_data)
            page_num += 1
    return result

# ----------------------------------------------------------------------------------------------------


list_of_provinces = [
    #     'Ardabil',
    #     'Alborz',
    #     'west_Azerbaijan',
    #     'east_azerbaijan',
    #     'boushehr',
    #     'ChaharMahal_Bakhtiari',
    #     'Fars',
    #     'Gilan',
    #     'Golestan',
    #     'Hamadan',
    #     'Hormozgan',
    #     'Ilam',
    #     'Isfahan',
    #     'Kerman',
    #     'Kermanshah',
    #     'North_Khorasan',
    #     'Razavi_Khorasan',
    #     'South _Khorasan',
    #     'Khuzestan',
    #     'kohgiluyeh_boyer_ahmad',
    #     'Kurdistan',
    #     'Lorestan',
    #     'Markazi',
    #     'Mazandaran',
    #     'Qazvin',
    #     'Qom',
    #     'Semnan',
    #     'Sistan and Baluchestan',
    #     'Tehran',
    #     'Yazd',
    #     'Zanjan',
]


def for_all_cities(input_data):
    for city in list_of_provinces:
        data = for_all_items(input_data)
        write(data)

# ----------------------------------------------------------------------------------------------------


def set_max(lst):
    maximom_bedroomsCount = max( lst, key=lambda place: place['bedroomsCount'] )
    maximom_toiletsCount = max( lst, key=lambda place: place['toiletsCount'] )
    maximom_discountedPrice = max( lst, key=lambda place: place['discountedPrice']) 

    return maximom_bedroomsCount['bedroomsCount'], maximom_toiletsCount['toiletsCount'], maximom_discountedPrice['discountedPrice']


def best_places(input_data):
    city_data = for_all_items(input_data['primary inputs'])
    secondary_inputs = input_data['secondary inputs']
    scores = {}
    score = 0
    maximom = set_max(city_data)

    for item in city_data:
        score += (secondary_inputs['bedroomsCount']['importance'])*((secondary_inputs['bedroomsCount']['value'])-(item['bedroomsCount']))/(maximom[0])
        score += (secondary_inputs['toiletsCount']['importance'])*((secondary_inputs['toiletsCount']['value'])-(item['toiletsCount']))/(maximom[1])
        score += (secondary_inputs['price']['importance'])*((secondary_inputs['price']['value'])-(item['discountedPrice']))/(maximom[2])

        for amenity in secondary_inputs['amenities']:
            if amenity['value'] not in [ name['name'] for name in item['amenities'] ]:
                score -= amenity['importance']
        
        for _type in secondary_inputs['types']:
            if _type['value'] != item['type']:
                score -= _type['importance']
        
        scores[item['url']] = score
    
    return sorted(scores.items(), key= lambda place: place[1])[:10]


                

# ----------------------------------------------------------------------------------------------------


inp = {
    'primary inputs': {
        'city': "city-kerman",
        'start_date': 20240304,
        'end_date': 20240306,
        'capacity': 5,
    },
    'secondary inputs': {
        'bedroomsCount': {'value': 2, 'importance': 70},
        'toiletsCount': {'value': 1, 'importance': 90},
        'amenities': [
            {'value': 'water', 'importance': 70},
            {'value': 'cabinet', 'importance': 70}
        ],
        'types':
        [
            {'value': 'villa', 'importance': 70},
            {'value': 'apartment', 'importance': 40}
        ],
        'price': {'value': 4500000, 'importance': 70}
    }
}


list_of_best_places = best_places(inp)
for place in list_of_best_places:
    print(place[0])
