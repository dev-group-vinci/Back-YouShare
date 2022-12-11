from datetime import datetime


def datetime_to_iso_str(o):
    if isinstance(o, datetime):
        return o.isoformat()
    return o.__dict__
