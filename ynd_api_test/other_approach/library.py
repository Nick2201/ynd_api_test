from yadirstat import yadirstat
token = 'y0_AgAAAABu2xF5AAZAOQAAAADmHGKSqpIbga_1RRimuZuJtFZj-87Ff2Q'
# client_id = 'f45705b3078e4c8396e168c9427a3f3e'
client_id = 'nick-analyst'
# uery_report =yadirstat.yadirstat.query(
#     token,client_id,'2023-06-22','2023-06-23')
# print(query_report)
headers = {
    # OAuth token. The word Bearer must be used
    "Authorization": "Bearer " + token,
    # Login of the advertising agency client
    "Client-Login": clientLogin,
    # Language for response messages
    "Accept-Language": "en",
    # Mode for report generation
    "processingMode": "auto",
    # Format for monetary values in the report
    # "returnMoneyInMicros": "false",
    # Don't include the row with the report name and date range in the report
    "skipReportHeader": "true",
    # Don't include the row with column names in the report
    # "skipColumnHeader": "true",
    # Don't include the row with the number of statistics rows in the report
    "skipReportSummary": "true"
}

expense = f"https://api-metrika.yandex.net/management/v1/counter/{client_id}/expense/upload?provider=no example"
