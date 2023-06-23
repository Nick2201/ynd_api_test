
from io import StringIO
import numpy as np
from dotenv import load_dotenv
import os
from src.etl_metrics.extract import Yandex_Direct_API
load_dotenv()
token = os.getenv("TOKEN")
clientLogin = os.getenv("CLENT_LOGIN")
# Определение ID цели
goalID = [300987728]  # замените это на реальный ID цели
# Определение дат начала и окончания отчетного периода
date1 = '2023-05-25'
date2 = '2023-05-31'
yandex_direct_api = Yandex_Direct_API()
headers = yandex_direct_api.get_headers(token, clientLogin)
body = yandex_direct_api.get_body(date1, date2, goalID)
df = yandex_direct_api.get_report(headers, body)
print(df.to_string())
