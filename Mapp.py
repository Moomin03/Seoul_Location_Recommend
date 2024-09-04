import requests
import pprint
url = "https://dapi.kakao.com/v2/local/search/address.json" #요청할 url 주소
headers = {"Authorization": 'KakaoAK 3732ee66ab6b81c392638300d3eebbe7'}
query = {'query':'서울대학교'}
result = requests.get(url,
                      headers=headers,
                      data=query).json()
pp = pprint.PrettyPrinter(indent=5)
print(pp.pprint(result))
