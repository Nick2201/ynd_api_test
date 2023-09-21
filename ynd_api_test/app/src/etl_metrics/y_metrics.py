from tapi_yandex_metrika import YandexMetrikaStats
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
ACCESS_TOKEN = os.getenv("TOKEN")
COUNTER_ID = " 94085606" # for example
# https://metrika.yandex.ru/stat/sites?chart_type=stacked-chart&period=week&accuracy=1&id=94085606&stateHash=650c433cc190dd000c5b7dad
client = YandexMetrikaStats(access_token=ACCESS_TOKEN)

params = dict(
    ids=COUNTER_ID,
    date1="2023-01-01",
    date2="2023-01-31",
    metrics="ym:s:visits",
    dimensions="ym:s:date, ym:s:isRobot", # parametr for ident Robots(robots=True)
    sort="ym:s:date",
    lang="en",
    #Другие параметры Метрики -> https://yandex.ru/dev/metrika/doc/api2/api_v1/data.html
)
report = client.stats().get(params=params)
result = report().to_values()
df = pd.DataFrame (result, columns = ['ym:s:date', 'ym:s:isRobot', 'ym:s:visits'])
print (df)