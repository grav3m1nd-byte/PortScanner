#!/usr/bin/python3

import socket   # Reference https://docs.python.org/3/library/socket.html
import sys


def ip_manipulation(r_range="0.0.0.0"):
    # This function is meant to receive IP addresses or ranges in the specific notation
    # and if a dash (-) exist, designating a range, it will convert the range into a
    # list where each octet is an item of the list (addressList). The last item in the list
    # will have the last octet of the first and last IP address to scan.
    # With this last item of the list, the function evaluates it to force it to be
    # within 1 and 255, and through the iteration, the value at that point in time
    # will be assigned to that last item in the addressList.

    # From there, addressList needs to be converted into a string, joining each item
    # with a '.' and then assigning the composed string (the IP address)
    # into an item of a new empty list (rhosts). This new list becomes a list of
    # IP addresses, where each item is one IP address.

    rhosts = []     # Defining rhosts as an empty list
    if "-" in r_range:
        addressList = r_range.split(".")    # Splitting the string r_range into a list with '.' as delimiter

        # The section below focuses on the fourth item in the addressList (index 3), and will
        # make sure the range for the fourth octet stays within 1 and 255. Each for loop will
        # take care of assigning the a value to the fourth item in the addressList, to then
        # compose it into a string using the '.' delimiter, and then append each IP address
        # string into the rhosts list, where each item is one IP address.
        if (int(addressList[3].split("-")[0])) == 0 and (int(addressList[3].split("-")[1]) + 1) <= 255:
            for i in range(int(addressList[3].split("-")[0]) + 1, int(addressList[3].split("-")[1]) + 1):
                addressList[3] = str(i)
                rhosts.append(".".join(addressList))
        elif (int(addressList[3].split("-")[0])) >= 1 and (int(addressList[3].split("-")[1]) + 1) <= 255:
            for i in range(int(addressList[3].split("-")[0]), int(addressList[3].split("-")[1]) + 1):
                addressList[3] = str(i)
                rhosts.append(".".join(addressList))
        else:
            # If the IP address is not within a /24 (255 addresses to scan) per users input,
            # it will error out and exit.
            print("ERROR: Accepted IP range should be within the 255.255.255.0 subnet mask.")
            sys.exit()
    else:
        # If no range was detected by the use of a dash, then it is assumed it is an IP address.
        rhosts = [r_range]
    return rhosts


def main():
    # Receive the IP Address or range from input and pass it as an argument to the function ip_manipulation
    scanhost = ip_manipulation(input("Enter the remote address range to scan\n(Example of format is 192.168.0.1-255): "))

    # Multiple variable assignment as the same data type is expected from input. Casting is used to convert to int.
    sport, eport = int(input("Enter the start port: ")), int(input("Enter the end port: "))

    print("\nIP addresses to scan:\n")

    # For loop is used to go by one IP address at a time, from index 0 to the last item,
    # per the size (len()) of the list, then print a list of IP addresses to scan.
    for i in range(len(scanhost)):
        print("\t[*]\t", scanhost[i])

    # Similar as the above, this for loop will iterate through each item in the IP address list,
    # print one item, and then go through the range of ports as designated in the nested for loop.
    for n in range(len(scanhost)):
        print("\nScanning IP Address: ", scanhost[n])
        for port in range(sport, (eport + 1)):
            try:
                # Here, it will try to create a socket of IPv4 type (AF_INET) and TCP port (SOCK_STREAM),
                # with a timeout of 5 seconds (a delay could be added), and then connect to the IP address
                # used and the port in the current iteration. When an open port is found, print it
                # and then close the connection.
                print("\n\t[*]\tScanning port: ", port)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # socket.socket (socket_family, socket_kind)
                s.settimeout(5)
                s.connect((scanhost[n], port))
                print("\n\t[+]\tFound open port: ", port)

            except socket.error as error:
                print("ERROR: ", error)

            finally:
                s.close()


if __name__ == "__main__":
    main()

