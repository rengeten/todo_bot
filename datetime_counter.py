import datetime
def cdate_count(user_text):
    user_text = user_text.replace("/set", "")
    user_text = user_text.replace(" ", "")
    if ':' in user_text:
        user_text_list = user_text.split(':')
        ndt = datetime.datetime.strptime(user_text_list[0], '%Y/%m/%d/%H/%M')
        dt_now = datetime.datetime.now()
        new_date = ndt - dt_now
        result = new_date.total_seconds()
        listlist = user_text_list[1]
        answer = str(listlist)
        return user_text_list
    else:    
        ndt = datetime.datetime.strptime(user_text, '%Y/%m/%d/%H/%M')
        dt_now = datetime.datetime.now()
        new_date = ndt - dt_now
        result = new_date.total_seconds()
        return int(result)
