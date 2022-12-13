from datetime import datetime


def datetime_to_iso_str(o):
    if isinstance(o, datetime):
        return o.isoformat()
    return o.__dict__

def parseList(list):
    newList = []
    for element in list:
        newList.append(element.unescape().__dict__)
    return newList

def parseElement(element):
    return element.unescape().__dict__