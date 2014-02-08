import datetime

def dateformat(value, format="%d-%b-%Y"):
    if isinstance(value, datetime.date):
        return value.strftime(format)
    return value

def mepkind(item):
    if item['mep'] < 100:
        return 'Info'
    elif item['status'] == 'Final': 
        return 'Final' 
    else: 
        return 'Open' 

def taskkind(item):
    if item['task'] == 0:
        return 'Info'
    elif 'status' in item and item['status'][:9] == 'Completed': 
        return 'Completed' 
    else: 
        return 'Open' 

filters = {}
filters['dateformat'] = dateformat
filters['mepkind'] = mepkind
filters['taskkind'] = taskkind

