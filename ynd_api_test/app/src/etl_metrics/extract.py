import requests
from requests.exceptions import ConnectionError
from time import sleep
import json
import random
import pandas as pd
from io import StringIO
import numpy as np
from dotenv import load_dotenv
import os
class Yandex_Direct_API:
    """
    Класс, представляющий API Yandex Direct, с методами для выполнения запросов и обработки ответов.
    """

    def get_headers(self, token:str,clientLogin:str) -> dict: # TASK: OAuth-токен Getter ynd_api_test\utils\oath_token_getter.py
        """
        Получение заголовков для API запроса.

        Аргументы:
        token (str): OAuth-токен.
        clientLogin (str): Логин клиента рекламного агентства.

        Возвращает:
        dict: Заголовки для запроса к API.
        """
        headers_direct = {
            # OAuth-токен. Использование слова Bearer обязательно
            "Authorization": "Bearer " + token,
            # Логин клиента рекламного агентства
            "Client-Login": clientLogin,
            # Язык ответных сообщений
            "Accept-Language": "ru",
            # Режим формирования отчета
            "processingMode": "auto",
            # Формат денежных значений в отчете
            "returnMoneyInMicros": "false",
            #Не выводить в отчете строку с названием отчета и диапазоном дат
            "skipReportHeader": "true",
            # Не выводить в отчете строку с названиями полей
            # "skipColumnHeader": "true",
            # Не выводить в отчете строку с количеством строк статистики
            "skipReportSummary": "true"
        }
        return headers_direct

    #новая функция с лимитами
    def get_body(
        self,
        date1:str,date2:str,
        goalID:int,
        FieldNames:list=[
                    'CampaignName', 'AdGroupName','Device','Date',
                    'Gender','Age','TargetingLocationName','Impressions',
                    'Clicks','Cost','Conversions'
                    ]):


        """
        Создание тела запроса.

        Аргументы:
        date1 (str): Дата начала отчетного периода.
        date2 (str): Дата окончания отчетного периода.
        fields_direct (list): Список полей для отчета.
        goalID (int): ID цели.

        Возвращает:
        str: Тело запроса в формате JSON.
        """
        # боди для директа
        reportNumber = random.randrange(1, 200000)
        # Создание тела запроса
        body = {
            "params": {
                "SelectionCriteria": {
                    "DateFrom": date1,
                    "DateTo": date2
                },
                "Goals": goalID,
                "FieldNames": FieldNames,

                "ReportName": f'Отчет №{reportNumber}',
                "ReportType": "CUSTOM_REPORT",
                "DateRangeType": "CUSTOM_DATE",
                "Format": "TSV",
                "IncludeVAT": "YES",
                "IncludeDiscount": "NO"
            }
        }

        # Кодирование тела запроса в JSON
        body = json.dumps(body, indent=4)
        return body


    def get_report(self,headers:dict,body:str):
        """
        Получение отчета из API.

        Аргументы:
        headers (dict): Заголовки для запроса.
        body (str): Тело запроса в формате JSON.

        Возвращает:
        DataFrame: DataFrame pandas с данными отчета или None, если возникла ошибка.
        """
        url = 'https://api.direct.yandex.com/json/v5/reports'
        retryIn = int(3)
        while True:  # TASK: Turn to match case
            try:
                req = requests.post(url, body, headers=headers)
                req.encoding = 'utf-8'

                match req.status_code:
                    case 400:
                        print("Параметры запроса указаны неверно или достигнут лимит отчетов в очереди.\n")
                        print(f"JSON-код ответа сервера: \n{req.json()['error']['error_detail']}\n")
                        break
                    case 200:
                        print("Данные выгружены.\n")
                        df = pd.read_csv(StringIO(req.text), sep='\t')
                        print(df.to_string())
                        return df
                    case 201:
                        print("Отчет успешно поставлен в очередь в режиме офлайн. \nЗагрузка может занять до 3-х минут.\n")
                        sleep(retryIn)
                    case 202:
                        sleep(retryIn)
                    case 500:
                        print("При формировании отчета произошла ошибка. Пожалуйста, попробуйте повторить запрос позднее.\n")
                        print(f"JSON-код ответа сервера: \n{req.json()['error']['error_detail']}\n")
                        break
                    case 502:
                        print("Время формирования отчета превысило серверное ограничение.")
                        print("Пожалуйста, попробуйте изменить параметры запроса - уменьшить период и количество запрашиваемых данных.\n")
                        print(f"JSON-код ответа сервера: \n{req.json()['error']['error_detail']}\n")
                        break
                    case _:
                        break
            except ConnectionError:
                print('Ошибка соединения')
                break
            except Exception as ex:
                print(ex)
                break


if __name__ == '__main__':
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