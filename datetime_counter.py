import datetime
def cdate_count(user_text):
    user_text = user_text.replace("/set", "")
    user_text = user_text.replace(" ", "")
    ndt = datetime.datetime.strptime(user_text, '%Y/%m/%d/%H/%M')
    dt_now = datetime.datetime.now()
    new_date = ndt - dt_now
    result = new_date.total_seconds()
    return int(result)