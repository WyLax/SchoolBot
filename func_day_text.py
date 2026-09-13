async def day_text(name_day):

    if name_day == 'test':
        day = 'тест'
    if name_day == 'monday':
        day = 'понедельник'
    elif name_day == 'tuesday':
        day = 'вторник'
    elif name_day == 'wednesday':
        day = 'среда'
    elif name_day == 'thursday':
        day = 'четверг'
    elif name_day == 'friday':
        day = 'пятница'


    return day
