# Dawei Li, 001022014

import re
from .hash_table import MyHashTable
from datetime import datetime
from .read_xlsx import XlsxReader


# Create two global variables to hold package and distance data
# to be used across modules.
package_data = None
distance_data = None
total_distance = 0


def init():
    read_package_data()
    read_distance_data()


def read_package_data():
    """Read package data into a hash table"""
    # Create an empty hash table to store package data
    # Key: package ID
    # Value: a hash table holding package details
    global package_data
    package_reader = XlsxReader(file_loc="./data/WGUPS Package File.xlsx")
    rawdata = package_reader.read_data_sheet(0)
    package_data = MyHashTable()
    for row in range(8, rawdata.nrows):
        # Package id is the key
        id = rawdata.cell_value(row, 0)
        # Use a hash table to store package details
        hash_table = MyHashTable()
        # Package 9 has a wrong address.
        if row == 16:
            hash_table.add("address", "410 S State St")
        else:
            hash_table.add("address", rawdata.cell_value(row, 1))
        hash_table.add("city", rawdata.cell_value(row, 2))
        hash_table.add("state", rawdata.cell_value(row, 3))
        hash_table.add("zip", rawdata.cell_value(row, 4))
        hash_table.add("deadline", deadline(rawdata.cell_value(row, 5)))
        hash_table.add("weight", rawdata.cell_value(row, 6))
        hash_table.add("notes", rawdata.cell_value(row, 7))
        # Add and initialize two additional attributes
        hash_table.add("status", "idle")
        hash_table.add("delivery time", None)
        # Add package id (key) and details (value) to the hash table
        package_data.add(id, hash_table)


def deadline(time):
    """Convert the deadline data in the EOD column in the package excel file to datetime format"""
    # If time is "EOD", convert it to 17:00
    if time == "EOD":
        return datetime(2019, 11, 22, 17)
    time = int(time * 24 * 3600)
    hour = time // 3600
    minute = (time % 3600) // 60
    return datetime(2019, 11, 22, hour, minute)


def read_distance_data():
    """Read distance data into a hash table"""
    # Create an empty hash table to store distance data
    # Key: a tuple of two locations
    # Value: distance between the two locations in the key
    global distance_data
    distance_reader = XlsxReader(file_loc="./data/WGUPS Distance Table.xlsx")
    rawdata = distance_reader.read_data_sheet(0)
    distance_data = MyHashTable()
    # First extract only street number and street name
    # from the full address. This combination matches the 
    # address data in the packages data
    addresses = []
    col = 0
    for row in range(8, rawdata.nrows):
        value = rawdata.cell_value(row, col)
        value = re.split(r'\s*\n\s*', value)[1]
        value = re.split(r'\,', value)[0]
        # Correct a mismatch between the distance file and the package file
        if value == "3575 W Valley Central Sta bus Loop":
            value = "3575 W Valley Central Station bus Loop"
        addresses.append(value)
    # Extract distance data into the hash table
    for row in range(8, rawdata.nrows):
        for i in range(2, row-7):
            address_tuple = (addresses[row-8], addresses[i-2])
            distance = rawdata.cell_value(row, i)
            distance_data.add(address_tuple, distance)
        for j in range(row+1, rawdata.nrows):
            address_tuple = (addresses[j-8], addresses[row-8])
            distance = rawdata.cell_value(j, row-6)
            distance_data.add(address_tuple, distance)
        # Two packages may be delivered to the same address.
        # So set the distance of a location to itself as 0.
        address_tuple = (addresses[row-8], addresses[row-8])
        distance_data.add(address_tuple, 0)


def all_status():
    """Return a hash table of (id, status) for all packages."""
    global package_data
    all_status = MyHashTable()
    packages_id = package_data.all_keys()
    for id in packages_id:
        status = package_data.get(id).get("status")
        delivery_time = package_data.get(id).get("delivery time")
        all_status.add(id, (status, delivery_time))
        print(id, " ", (status, delivery_time))
    return all_status
