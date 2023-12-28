from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import openpyxl
from db import query
from datetime import timedelta, date, datetime
from logging_handling import error_logging, info_logging
import requests
import os
from functions import generate_chart

try:
    init_total_akses_menu_file = "init_akses_menu_vedita.xlsx"
    df_init = pd.read_excel(init_total_akses_menu_file, sheet_name='Sheet1')

    sql = "select client_ip, app_name, endpoint, access_time FROM VEDITA_LOG_APP WHERE (endpoint LIKE '/vedita-cs-list-subcategory?id_category=%' OR endpoint LIKE '/open-ai%' OR endpoint LIKE '/antrean%') AND app_name = 'VEDITA' AND client_ip = '10.87.7.101' OR client_ip = '10.87.11.29' AND access_time BETWEEN '2023-11-15 00:00:00' AND CURRENT_TIMESTAMP  AND methods = 'GET' order by endpoint ASC;"
    data = query(sql)

    tmp = []

    for i, val in enumerate(data):
        if val['endpoint'] == '/antrean':
            data[i]['endpoint'] = 'AntreAja'
        elif val['endpoint'] == '/vedita-cs-list-subcategory?id_category=1':
            data[i]['endpoint'] = 'Kartu SIM'
        elif val['endpoint'] == '/vedita-cs-list-subcategory?id_category=2':
            data[i]['endpoint'] = 'Roaming'
        elif val['endpoint'] == '/vedita-cs-list-subcategory?id_category=3':
            data[i]['endpoint'] = 'Indihome'
        elif val['endpoint'] == '/vedita-cs-list-subcategory?id_category=4':
            data[i]['endpoint'] = 'Telkomsel One'
        elif val['endpoint'] == '/open-ai':
            data[i]['endpoint'] = 'ChatGPT'

        d = {
            "Nama Menu": data[i]['endpoint'],
            "Timestamp": data[i]['access_time'].strftime('%Y-%m-%d %H:%M:%S')
        }
        tmp.append(d)

    df_new = pd.DataFrame(tmp)
    df_init = pd.concat([df_init, df_new], ignore_index=True)
    df_init.sort_values(by=['Timestamp', 'Nama Menu'])
    start_date = datetime(2023, 10, 19, 0, 0, 0)
    end_date = datetime.now()

    df_init['Timestamp'] = pd.to_datetime(df_init['Timestamp'], dayfirst=True)

    # df1 = df_init['Timestamp'].dt.date.value_counts().sort_index().reset_index()
    df_init['Timestamp'] = pd.to_datetime(df_init['Timestamp'])

    # Extract the date from the 'timestamp' column
    df_init['Tanggal'] = df_init['Timestamp'].dt.date
    df1 = df_init.groupby(['Tanggal', 'Nama Menu']).size().reset_index(name='Count')

    current_date = start_date
    index = 0
    while current_date <= end_date:
        df_tmp_date = pd.to_datetime(df_init['Timestamp'])
        tmp_date = date(current_date.year, current_date.month, current_date.day)
        if not ((df_init['Nama Menu'] == "Kartu SIM") & (df_tmp_date.dt.date.values == tmp_date)).any():
            new_row = pd.DataFrame([{
                'Tanggal': tmp_date,
                'Nama Menu': 'Kartu SIM',
                'Count': 0
            }])
            df1 = pd.concat([df1, new_row], ignore_index=True)
        if not ((df_init['Nama Menu'] == "Roaming") & (df_tmp_date.dt.date.values == tmp_date)).any():
            new_row = pd.DataFrame([{
                'Tanggal': tmp_date,
                'Nama Menu': 'Roaming',
                'Count': 0
            }])
            df1 = pd.concat([df1, new_row], ignore_index=True)
        if not ((df_init['Nama Menu'] == "Indihome") & (df_tmp_date.dt.date.values == tmp_date)).any():
            new_row = pd.DataFrame([{
                'Tanggal': tmp_date,
                'Nama Menu': 'Indihome',
                'Count': 0
            }])
            df1 = pd.concat([df1, new_row], ignore_index=True)
        if not ((df_init['Nama Menu'] == "Telkomsel One") & (df_tmp_date.dt.date.values == tmp_date)).any():
            new_row = pd.DataFrame([{
                'Tanggal': tmp_date,
                'Nama Menu': 'Telkomsel One',
                'Count': 0
            }])
            df1 = pd.concat([df1, new_row], ignore_index=True)
        if not ((df_init['Nama Menu'] == "AntreAja") & (df_tmp_date.dt.date.values == tmp_date)).any():
            new_row = pd.DataFrame([{
                'Tanggal': tmp_date,
                'Nama Menu': 'AntreAja',
                'Count': 0
            }])
            df1 = pd.concat([df1, new_row], ignore_index=True)
        if not ((df_init['Nama Menu'] == "ChatGPT") & (df_tmp_date.dt.date.values == tmp_date)).any():
            new_row = pd.DataFrame([{
                'Tanggal': tmp_date,
                'Nama Menu': 'ChatGPT',
                'Count': 0
            }])
            df1 = pd.concat([df1, new_row], ignore_index=True)
        current_date += timedelta(days=1)
        index += 1

    df1 = df1.sort_values(by=['Tanggal', 'Nama Menu', 'Count'])

    menu_names = df1.groupby(['Nama Menu'])['Nama Menu'].apply(lambda x: x.unique())

    columns = ['Date']
    all_columns = [value[0] for value in menu_names]
    columns.extend(all_columns)
    df2 = pd.DataFrame()
    index = 0
    while index < len(df1):
        column_data = ["Date"]
        column_data.extend(df1['Nama Menu'][index:index+6].to_list())
        count_data = df1['Count'][index:index+6].tolist()
        tmp_data = [df1['Tanggal'][index:index+6].to_list()[0]]
        tmp_data.extend(count_data)
        df_tmp = pd.DataFrame([tmp_data], columns=column_data)
        df2 = pd.concat([df2, df_tmp], ignore_index=True)
        index += 6

    file_name = f"Vedita_Summary_Menu_{end_date.strftime('%Y-%m-%d')}.xlsx"
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Summary')
    writer.sheets['Summary'] = worksheet
    df2.to_excel(writer, sheet_name='Summary', index=False, startrow=1, header=False)

    header_format = workbook.add_format({
        'bg_color': '#d8db0d',  # your setting
        'bold': True,           # additional stuff...
        'text_wrap': True,
        'valign': 'top',
        'align': 'center',
        'border': 1})

    max_width = max([len(str(col)) for col in df_init.columns]) + 2
    for col_num, value in enumerate(df2.columns.values):
        worksheet.write(0, col_num, value, header_format)
        worksheet.set_column(col_num, col_num, max_width)

    worksheet = workbook.add_worksheet('RAW')
    df_init = df_init.drop('Tanggal', axis=1)
    df_init = df_init.sort_values(by=['Timestamp', 'Nama Menu'])
    df_init.to_excel(writer, sheet_name="RAW", index=False, startrow=1, header=False)
    max_width = max([len(str(col)) for col in df_init.columns]) + 6
    for col_num, value in enumerate(df_init.columns.values):
        worksheet.write(0, col_num, value, header_format)
        worksheet.set_column(col_num, col_num, max_width)
    # writer.save
    writer._save()
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", None)
    CHAT_ID = os.environ.get("TARGET_CHAT", None)
    PROXY_SAKTI = os.environ.get('PROXY_SAKTI', None)
    if TELEGRAM_TOKEN is not None and CHAT_ID is not None:
        bulan = [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        files = {'document': open(file_name, 'rb')}
        params = {
            "chat_id": CHAT_ID,
            "caption": f"Semangat pagi berikut report untuk Vedita per tanggal {end_date.day} {bulan[end_date.month - 1]} {end_date.year}"
        }
        proxies = None
        if PROXY_SAKTI is not None or PROXY_SAKTI != "":
            proxies = {
                'http': PROXY_SAKTI,
                'https': PROXY_SAKTI
            }
        telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
        res = requests.post(f"{telegram_api_url}/sendDocument", files=files, params=params, proxies=proxies)
        if res.status_code == 200:
            print("Berhasil kirim file")
            info_logging("Berhasil kirim file")
            filename = generate_chart(df2.copy(), end_date)
            files = {'photo': open(filename, 'rb')}
            params = {
                "chat_id": CHAT_ID,
            }
            res = requests.post(f"{telegram_api_url}/sendPhoto", params=params, files=files, proxies=proxies)
            if res.status_code == 200:
                print("Berhasil kirim gambar")
                info_logging("Berhasil kirim gambar")
            else:
                print("Gagal kirim gambar")
                info_logging('Gagal kirim gambar')
        else:
            print("Gagal kirim file")
            info_logging("Gagal kirim file")

    
except Exception as e:
    error_logging()