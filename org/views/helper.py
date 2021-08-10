import datetime


def get_formatted_date(year, month, day):
    day_s = ''
    month_s = ''
    if day != '':
        day_s = day + ' '
    if month != '':
        month_s = month + ', '
    f_date = "{0}{1}{2}".format(day_s, month_s, year)
    return f_date


def get_date(year, month, day):
    print(year)
    print(month)
    print(day)
    if year == "":
        return None
    if month == "":
        month = "January"
    if day == "":
        day = "1"
    print(year + "-" + month + "-" + day)
    d = datetime.datetime.strptime(year + "-" + month + "-" + day, '%Y-%B-%d')
    return d


def get_date_d(year, month, day):
    if year == "":
        return None
    if month == "":
        month = "1"
    if day == "":
        day = "1"
    d = datetime.datetime.strptime(year + "-" + month + "-" + day, '%Y-%m-%d')
    return d
