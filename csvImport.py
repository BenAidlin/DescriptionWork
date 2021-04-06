import pandas as pd

""""
procedures to extract csv from event2mind and ATOMIC using pandas,
notice event column in both projects is not unique, so to use 
the dictionary without losing info i've used the i-trick.
"""


def import_csv_from_all_files(list_of_paths, atomic_delimiter):
    """"
    atomic_delimiter(int) csv files in ATOMIC format
    the rest in event2mind format
    """
    to_ret = []
    i = 0
    for path in list_of_paths:
        if i < atomic_delimiter:
            to_ret.append(read_csv_atomic(path))
        else:
            to_ret.append(read_csv_event2mind(path))
        i += 1
    return to_ret


def read_csv_atomic(path):
    dic = {}
    df = pd.read_csv(path)
    i = 0
    for index, row in df.iterrows():
        if row['event'] not in dic.keys():
            dic[row['event']] = tuple(row[i] for i in (row.keys().delete(0)))
            i = 0
        else:
            dic[row['event']+str(i)] = tuple(row[i] for i in (row.keys().delete(0)))
            i += 1
        # event	: oEffect	oReact	oWant	xAttr	xEffect	xIntent	xNeed	xReact	xWant	prefix	split if


def read_csv_event2mind(path):
    dic = {}
    df = pd.read_csv(path)
    i = 0
    for index, row in df.iterrows():
        if row['Event'] not in dic.keys():
            dic[row['Event']] = tuple(row[i] for i in (row.keys().delete(1)))
            i = 0
        else:
            dic[row['Event']+str(i)] = tuple(row[i] for i in (row.keys().delete(1)))
            i += 1
        # 	Event : Source	Xintent 	Xemotion	Otheremotion	Xsent	Osent
