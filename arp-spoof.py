#!/usr/bin/env python3

import os
import platform

system = platform.uname()
operatingSystem = system[0]


def arp_info():  # First function
    arpData = os.popen("arp -a").read()
    return arpData.split("\n")


def arp_filters(arp_list=[]):  # Second function
    arp_dict = dict()

    # for line in range(len(arp_list)):
    for line in range(len(arp_list) - 1):
        try:
            if "Windows" in operatingSystem:
                ip_address = arp_list[line].split()[0]
                mac_address = arp_list[line].split()[1]
                if len(mac_address) == 17 and mac_address.count("-") == 5:
                    arp_dict.update({ip_address: mac_address})
            else:
                ip_address = arp_list[line].split()[1].strip('()')
                mac_address = arp_list[line].split()[3]
                hostname = str(arp_list).split()[0].strip("['")

                if len(mac_address) == 17 and mac_address.count(":") == 5:
                    arp_dict.update({ip_address: [mac_address, hostname]})

        except IndexError as error:
            print("ERROR: {}".format(error))

    return arp_dict


def check_dup(arpdict=dict()):
    macAddress = list(arpdict.values())

    if "Windows" in operatingSystem:

        for ip, mac in arpdict.items():
            if mac == "FF-FF-FF-FF-FF-FF":
                print("\nNetwork Broadcast Address: {}-> {}".format(ip, mac))
            elif macAddress.count(mac) >= 2:
                print("\nDuplicate MAC Address found:\n\tIP: {} --> MAC: {}".format(ip, mac))
    else:
        counter = 1
        for ip, hostinfo in arpdict.items():
            mac = hostinfo[0]
            host = hostinfo[1]

            if mac == "FF:FF:FF:FF:FF:FF" or mac == "ff:ff:ff:ff:ff:ff":
                print("\nNetwork Broadcast Address: {} --> MAC: {}".format(ip, mac))

            elif sum(index0.count(mac) for index0 in macAddress) >= 2:
                print("\tDuplicate #{}:\n\t\tIP: {} --> MAC: {}\tHost: {}".format(counter, ip, mac, host))
                counter += 1


def get_arp_table(arpdict=dict()):
    macAddress = list(arpdict.values())

    if "Windows" in operatingSystem:

        for ip, mac in arpdict.items():
            print("\tIP: {} --> MAC: {}".format(ip, mac))
    else:
        for ip, hostinfo in arpdict.items():
            mac = hostinfo[0]
            host = hostinfo[1]
            print("IP: {} --> MAC: {}\tHost: {}".format(ip, mac, host))


def main():
    print("Running Script on System:")
    for i in range(len(system) - 1):
        print("\t{}".format(system[i]))

    arp_data = arp_info()
    ip_mac_dict = arp_filters(arp_data)

    print("\nARP Table Data:")
    get_arp_table(ip_mac_dict)

    check_dup(ip_mac_dict)


if __name__ == "__main__":
    main()
