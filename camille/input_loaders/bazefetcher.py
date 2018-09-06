import pandas as pd
from os import path, listdir
import dateutil
import datetime
import pytz
import re
import fnmatch


def _to_datetime(time):
    # Converts to midnight datetime if given as date
    if not isinstance(time, datetime.datetime):
        time = datetime.datetime(time.year, time.month, time.day)
    try:
        return pytz.utc.localize(time)
    except ValueError:
        return time.astimezone(pytz.utc)


def _bazefetcher_time_filter(start, end, filename):
    filename = path.split(filename)[-1]
    filename = path.splitext(filename)[0]

    try:
        s, e = filename.split('_')[-2:]
    except ValueError:
        return False

    file_start = pd.Timestamp(dateutil.parser.parse(s.replace('.',':')))
    file_end = pd.Timestamp(dateutil.parser.parse(e.replace('.',':')))

    return start <= file_end and end > file_start


def load(tag,
         start,
         end,
         interpolation=None,
         join=None,
         base_folder='./'):
    if not isinstance(tag, list): tag = [tag]
    start = _to_datetime(start)
    end = _to_datetime(end)
    df = pd.DataFrame()

    for t in tag:
        matcher = re.compile(fnmatch.translate(t))
        dirs = [ path.join(base_folder, d)
                 for d in listdir(base_folder) if  matcher.match(d) ]
        files = [ list(map( lambda x: path.join(d, x), listdir(d) ))
                  for d in dirs ]
        files = sum( files, [] )
        files = [x for x in files if _bazefetcher_time_filter(start, end, x)]
        column = []

        for file in files:
            c = pd.read_json(file, convert_dates=['t'])
            c = c.filter(['t','v'])
            try:
                c.set_index('t', inplace=True)
                column.append(c[start:end-datetime.timedelta.resolution])
            except KeyError:
                pass

        column = pd.concat(column)
        column.rename(index=str, columns={'v':t}, inplace=True)

        if df.empty:
            df = column
        else:
            if join:
                df = df.join(column, how=join)
            else:
                df = df.join(column)

    if interpolation:
        df.interpolate(method=interpolation)

    return df
