def convert_datetime_format(datetime_value):
    months =['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    try:    
        month = months[int(datetime_value.strftime("%m"))-1]
        day = datetime_value.strftime("%d")
        year = datetime_value.strftime("%Y")
        hour = int(datetime_value.strftime("%H"))
        minute = datetime_value.strftime("%M")
        
        if 0<=hour<12 :
            datetime_output = f'{month} {day}, {year}, {hour}:{minute} a.m.'
        else:
            datetime_output = f'{month} {day}, {year}, {hour-12}:{minute} p.m.' 
    except:
        datetime_output = ' '

    return datetime_output