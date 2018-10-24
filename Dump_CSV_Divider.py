import pandas as pd
import numpy as np
import os


def delete_blanks(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    # remove spaces
    lines = [line.replace(' ', '') for line in lines]

    # finally, write lines in the file
    with open(file_name, 'w') as f:
        f.writelines(lines)


def keep_cols(in_file_name, out_file_name, keep_col):
    f = pd.read_csv(in_file_name)
    new_f = f[keep_col]
    new_f.to_csv(out_file_name, index=False)


def split_dump(dump, networks_file_name, clients_file_name):
    file = open(dump, "r")
    networks_file = open("files/%s_raw.csv" % networks_file_name, "w+")
    clients_file = open("files/%s_raw.csv" % clients_file_name, "w+")
    x = 0
    for line in file:
        if x == 1:
            networks_file.write(line)
        elif x == 2:
            clients_file.write(line)

        if line == "\n":
            x += 1


def process_dump(dump_name):
    csv_file = dump_name
    networks_name = "networks"
    clients_name = "clients"
    clients_keep_cols = ["Station MAC", " BSSID"]
    networks_keep_cols = ["BSSID", " channel", " ESSID"]

    split_dump(csv_file, networks_name, clients_name)

    keep_cols("files/%s_raw.csv" % networks_name, "files/networks.csv", networks_keep_cols)
    keep_cols("files/%s_raw.csv" % clients_name, "files/clients.csv", clients_keep_cols)

    clients = pd.read_csv("files/clients.csv", skipinitialspace=True)
    networks = pd.read_csv("files/networks.csv", skipinitialspace=True).rename(columns={"channel": "Channel"})
    result = clients.merge(networks, on="BSSID", how="left")

    result["Device_Name"] = np.nan
    result.to_csv("files/dump.csv", index=False)

    networks = pd.read_csv("files/networks.csv", skipinitialspace=True)
    networks.to_csv("files/networks.csv")

    os.remove("files/%s_raw.csv" % networks_name)
    os.remove("files/%s_raw.csv" % clients_name)
    os.remove("files/%s.csv" % clients_name)
    # os.remove("files/%s.csv" % networks_name)

    return "files/dump.csv"


process_dump("test-01._csv")
