import pandas as pd
from os import path, walk, listdir
import dateutil

def _bazefetcher_time_filter(start, end, filename):
    filename = path.split(filename)[-1]
    filename = path.splitext(filename)[0]

    try:
        s, e = filename.split('_')[-2:]
    except ValueError:
        return False

    file_start = pd.Timestamp(dateutil.parser.parse(s.replace('.',':')))
    file_end = pd.Timestamp(dateutil.parser.parse(e.replace('.',':')))

    return start <= file_start and file_end < end

def load(config, base_folder='./'):
    start = config['start']
    end = config['end']
    df = pd.DataFrame()
    for i, t in enumerate(config['tag']):
        dirs = [ path.join(base_folder, d)
                 for d in listdir(base_folder) if  t.match(d) ]
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
                column.append(c[start:end])
            except KeyError:
                pass
        column = pd.concat(column)
        df = df.join(column, how=config['join'])

    try:
        df.interpolate(method=config['interpolation'])
    except KeyError:
        pass

    return df
