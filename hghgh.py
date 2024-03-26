import requests
import json
def request(page_number, city='ramsar', capacity=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Referer': 'https://www.jabama.com/',
        'ab-channel': 'GuestDesktop,2.31.2,Windows,10,undefined,782977d1-10ab-4d81-a4e3-875d236e71d3',
        'X-User-Experiments': '1706603592491813-TEST_EXPERIMENT',
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
        'page-size': 16,
        'capacity': capacity,
        'page-number': page_number,
    }

    response = requests.post('https://gw.jabama.com/api/v4/keyword/city-'+city, params=params, headers=headers, json=json_data)
    return response.json()

def extract(data):
    lst = []
    for item in data['result']['items']:
        dic={}
        dic['areasize'] = item['accommodationMetrics']['areaSize']
        dic['bathroomsCount'] = item['accommodationMetrics']['bathroomsCount']
        dic['bedroomsCount'] = item['accommodationMetrics']['bedroomsCount']
        dic['buildingSize'] = item['accommodationMetrics']['buildingSize']
        dic['iranianToiletsCount'] = item['accommodationMetrics']['iranianToiletsCount']
        dic['toiletsCount'] = item['accommodationMetrics']['toiletsCount']
        dic['amenities'] = list(item['amenities'])
        dic['kind'] = item['kind']
        dic['min_night'] = item['min_night']
        dic['min_price'] = item['min_price']
        dic['region'] = item['region']
        dic['reservation_type'] = item['reservation_type']
        dic['payment_type'] = item['payment_type']
        dic['province'] = item['location']['province']
        dic['city'] = item['location']['city']
        dic['geo'] = item['location']['geo']
        dic['rate_count'] = item['rate_review']['count']
        dic['rate_score'] = item['rate_review']['score']
        dic['type'] = item['type']
        dic['verified'] = item['verified']
        dic['status'] = item['status']
        dic['capacity_base'] = item['capacity']['base']
        dic['capacity_extra'] = item['capacity']['extra']
        dic['mainPrice'] = item['price']['mainPrice']
        dic['discountedPrice'] = item['price']['discountedPrice']
        dic['price_perNight'] = item['price']['perNight']
        dic['placeType'] = item['placeType']
        item_type = dic['type']
        item_code = item['code']
        dic['url'] = f'https://www.jabama.com/stay/{item_type}-{item_code}'

        lst.append(dic)

    return lst

def main():
    done = False
    result = []
    page_num = 1
    while not done:
        json_data = request(page_num)
        if not json_data['result']['items']:
            done = True
        else:
            result += extract(json_data)
            page_num += 1
    return result


def for_all()
    citys_list=[
]
print(main())


lst=["اردبیل","اصفهان","البرز", "ایلام","آذربایجان شرقی","آذربایجان غربی","بوشهر",

  },
  {
    "province": "تهران",

  },
  {
    "province": "چهارمحال وبختیاری", "خراسان جنوبی","خراسان رضوی","خراسان شمالی","province": "خوزستان","زنجان","سمنان", "سیستان وبلوچستان","فارس", "قزوین", "قم","کردستان","کرمان","کرمانشاه", "کهگیلویه وبویراحمد","گلستان", "گیلان","لرستان","مازندران","مرکزی", "هرمزگان","همدان","یزد",
