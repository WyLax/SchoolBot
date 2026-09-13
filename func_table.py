import asyncio
import pandas as pd


async def table(name_day):

    if name_day == 'test':
        day = 'https://docs.google.com/spreadsheets/d/14l6Jd-9BfnbKGSw19BWhfFs0usYheEmfTWCZxILYh0M/export?format=csv'
    elif name_day == 'monday':
        day = 'https://docs.google.com/spreadsheets/d/1VofWY1vYGFHP-KGirs-0C84YOACDfp_rWkhJJP3Hpls/export?format=csv'
    elif name_day == 'tuesday':
        day = 'https://docs.google.com/spreadsheets/d/16a3BJvbLhm6NrzutUCxc7XpSODV2LY9RtpcHafNtQlo/export?format=csv'
    elif name_day == 'wednesday':
        day = 'https://docs.google.com/spreadsheets/d/1cHJdyoYvdI5RQAXeW3QCF5clT3MrhAVwnCIJJVQ-R1I/export?format=csv'
    elif name_day == 'thursday':
        day = 'https://docs.google.com/spreadsheets/d/1xSsWrXRtkI22AmsCN8BGro-aJQuoQXb0C3mPGIeBlzY/export?format=csv'
    elif name_day == 'friday':
        day = 'https://docs.google.com/spreadsheets/d/1OsxZ-wXKNwZzb9SYNsoboAWiYS0fp9QlM89ZoP6WA24/export?format=csv'


    df = await asyncio.to_thread(pd.read_csv, day)

    return str(df.values.flatten().tolist()) # Преобразуем DataFrame в список, но в строк



