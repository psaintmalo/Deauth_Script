import csv
import json
from Dump_CSV_Divider import *
import pandas as pd

# fieldnames = ["StationMAC", "BSSID", "channel", "ESSID"]


def csv2json(dump_file, json_file):
    with open(dump_file, "r") as f:
        reader = csv.reader(f)
        next(reader)
        d = dict((rows[0], rows[1:]) for rows in reader)

    with open(json_file, 'a') as f:
        json.dump(d, f, indent=4)


def read_csv(csv_file):
    df = pd.read_csv(csv_file)
    pd.options.display.max_columns = len(df.columns)
    pd.set_option('display.expand_frame_repr', False)
    print(df)


def rename(_id, new_name, dump):
    csv_ = open(dump, "r")
    csv_read = csv.reader(csv_)
    lines = list(csv_read)
    lines[_id+1][4] = new_name
    new_csv_ = open(dump, "w+")
    writer = csv.writer(new_csv_)
    writer.writerows(lines)


def delete_files():
    os.remove("files/dump.csv")
    os.remove("files/networks.csv")
