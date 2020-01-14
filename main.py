# Dawei Li, 001022014

import re
import math
from datetime import datetime
from datetime import timedelta
import random
import packages.data as data
from packages.read_xlsx import XlsxReader
from packages.truck import Truck
from packages.hash_table import MyHashTable
from packages.truck import Truck


def deliver(id_remain_shuffled):
    """Allocate and deliver packages."""
    # Create truck objects.
    # truck3 will not start to deliver until either truck1 or truck2, whichever
    # the earlier, returns. 
    truck1 = Truck()
    truck2 = Truck()
    truck3 = Truck()

    # Load some specific packages to trucks.
    # Load all packages with early deadlines on truck 1.
    id_early_deadline = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
    for id in id_early_deadline:
        truck1.load_truck(id, data.package_data.get(id))
    # Load delayed packages on truck 2.
    id_delayed = [6, 25, 28, 32]
    for id in id_delayed:
        truck2.load_truck(id, data.package_data.get(id))
    # Some packages can only be on truck 2.
    id_truck2 = [3, 18, 36, 38]
    for id in id_truck2:
        truck2.load_truck(id, data.package_data.get(id))
    # Package 9 has a wrong address. The correct address will not be provided 
    # until 10:20 am. Therefore, put it on the second delivery round.
    truck3.load_truck(9, data.package_data.get(9))

    # For the remaining packages, semi-randomly assign them to 
    # truck2 (8 slots available) and truck3 (15 slots available).
    for i in range(8):
        id = id_remain_shuffled[i]
        truck2.load_truck(id, data.package_data.get(id))
    for i in range(8, 19):
        id = id_remain_shuffled[i]
        truck3.load_truck(id, data.package_data.get(id))

    # Truck 1 and 2 deliver the packages.
    # Truck 1 departs at 8:00am
    start_time_1 = datetime(2019, 11, 22, 8)
    # Truck 2 departs at 9:05am
    start_time_2 = datetime(2019, 11, 22, 9, 5)
    start_location = "4001 South 700 East"
    truck1_success = truck1.deliver(start_time=start_time_1, start_location=start_location)
    truck2_success = truck2.deliver(start_time=start_time_2, start_location=start_location)
 
    # Truck 3 departs when either truck 1 or 2 returns, whichever the earlier.
    start_time_3 = truck1.curr_time if truck1.curr_time < truck2.curr_time else truck2.curr_time
    truck3_success = truck3.deliver(start_time=start_time_3, start_location=start_location)

    if truck1_success and truck2_success and truck3_success:
        return data.total_distance
    else:
        return math.inf

def main():
    random.seed(0)

    # Initialize package and distance data.
    data.init()

    # Randomly assign the remaining packages to three trucks.
    # Repeat the random allocation a few times to pick the best route.
    id_remain = [2, 4, 5, 7, 8, 10, 11, 12, 17, 19, 21, 22, 23, 24, 26, 27, 33, 35, 39]
    min_total_distance = math.inf
    for _ in range(100):
        id_remain_shuffled = id_remain[:]
        random.shuffle(id_remain_shuffled)
        data.total_distance = 0
        this_total_distance = deliver(id_remain_shuffled)
        if this_total_distance < min_total_distance:
            min_total_distance = this_total_distance
            best_id_allocation = id_remain_shuffled[:]
 
    # Run the delivery using best_id_allocation
    data.total_distance = 0
    final_distance = deliver(best_id_allocation)
    print("All packages are delivered. Final distance is", round(final_distance, 2), "miles")


def lookup_time():
    """Used in the lookup menu to let the users choose a time to lookup package status."""
    hour = int(input("Please enter the time (hour) to look up the status: "))
    while hour<0 or hour>24:
        print("Input error! Hour must be between 0 and 24 inclusive")
        hour = int(input("Please enter the time (hour) to look up the status: "))
    minute = int(input("Please enter the time (minute) to look up the status: "))
    while minute<0 or minute>60:
        print("Input error! Minute must be between 0 and 60 inclusive")
        minute = int(input("Please enter the time (minute) to look up the status: "))
    lookup_time = datetime(2019, 11, 22, hour=hour, minute=minute)
    return lookup_time


def lookup_by_id(package_id, lookup_time):
    """Lookup package details by package ID."""
    ht = data.package_data.get(package_id)
    delivery_time = ht.get("delivery time")
    on_route_time = ht.get("on route time")
    status = determine_status(lookup_time, on_route_time, delivery_time)
    print("\nPackage ID", int(package_id), "information: ")
    ht.print_all(status)


def lookup_by_attribute(attribute_data, attribute, lookup_time):
    """Lookup package IDs by an attribute."""
    id_list = []
    for i in range(len(data.package_data.buckets)):
        if data.package_data.buckets[i] is not None:
            for package_key_value in data.package_data.buckets[i]:
                values_hashtable = package_key_value[1]
                if attribute=="status":
                    delivery_time = values_hashtable.get("delivery time")
                    on_route_time = values_hashtable.get("on route time")
                    true_status = determine_status(lookup_time, on_route_time, delivery_time)
                    if true_status == attribute_data:
                        id_list.append(package_key_value[0])
                elif values_hashtable.get(attribute)==attribute_data:
                    id_list.append(package_key_value[0])
    if len(id_list)==0:
        print("No matching package was found.")
    else:
        for package_id in id_list:
            lookup_by_id(package_id, lookup_time)
            print()


def determine_status(lookup_time, on_route_time, delivery_time):
    """Given a lookup time and a package's on route time and delivery time, 
    determine the current status of a package
    """
    status = "idle"
    if lookup_time>=on_route_time and lookup_time<delivery_time:
        # set to on route
        status = "on route"
    elif lookup_time>=delivery_time:
        # set to delivered
        status = "delivered"
    return status


def show_menu():
    """Menu for look up."""
    choice, lookup_time = show_prompt()

    while choice != "0":
        if choice == "1":
            package_id = int(input("Please enter package ID number: "))
            while package_id<1 or package_id>40:
                print("Input error! Package ID number must be between 1 and 40 inclusive")
                package_id = int(input("Please enter package ID number: "))
            lookup_by_id(package_id, lookup_time)
        elif choice == "2":
            address = input("Please enter delivery address: ")
            lookup_by_attribute(attribute_data=address, attribute="address", lookup_time=lookup_time)
        elif choice == "3":
            hour = int(input("Please enter delivery deadline (Hour): "))
            while hour<0 or hour>24:
                print("Input error! Hour must be between 0 and 24 inclusive")
                hour = int(input("Please enter delivery deadline (Hour): "))
            minute = int(input("Please enter delivery deadline (Minute): "))
            while minute<0 or minute>60:
                print("Input error! Minute must be between 0 and 60 inclusive")
                minute = int(input("Please enter delivery deadline (Minute): "))
            deadline = datetime(2019, 11, 22, hour=hour, minute=minute)
            lookup_by_attribute(attribute_data=deadline, attribute="deadline", lookup_time=lookup_time)
        elif choice == "4":
            city = input("Please enter delivery city: ")
            lookup_by_attribute(attribute_data=city, attribute="city", lookup_time=lookup_time)
        elif choice == "5":
            zip = int(input("Please enter zip code: "))
            lookup_by_attribute(attribute_data=zip, attribute="zip", lookup_time=lookup_time)
        elif choice == "6":
            weight = int(input("Please enter package weight (kilo): "))
            while weight <= 0:
                print("Input error! Weight must be greater than 0.")
                weight = int(input("Please enter package weight (kilo): "))
            lookup_by_attribute(attribute_data=weight, attribute="weight", lookup_time=lookup_time)
        elif choice == "7":
            delivery_status = input("Please enter delivery status (Options: idle, on route, delivered): ")
            while delivery_status!="idle" and delivery_status!="on route" and delivery_status!="delivered":
                print("Input error! status must be idle, on route, or delivered")
                delivery_status = input("Please enter delivery status (Options: idle, on route, delivered: ")
            lookup_by_attribute(attribute_data=delivery_status, attribute="status", lookup_time=lookup_time)
        elif choice == "8":
            for package_id in range(1, 41):
                    ht = data.package_data.get(package_id)
                    delivery_time = ht.get("delivery time")
                    on_route_time = ht.get("on route time")
                    status = determine_status(lookup_time, on_route_time, delivery_time)
                    print("Package ID", int(package_id), "is", status)
        else:
            print("Only numbers 1-8, 0 are allowed. Please choose again.")
        choice, lookup_time = show_prompt()
    print("Exiting the program...")
    return


def show_prompt():
    """Show prompts for user inputs."""
    hour = int(input("\nPlease enter the time (hour) to look up the status: "))
    while hour<0 or hour>24:
        print("Input error! Hour must be between 0 and 24 inclusive")
        hour = int(input("Please enter the time (hour) to look up the status: "))
    minute = int(input("Please enter the time (minute) to look up the status: "))
    while minute<0 or minute>60:
        print("Input error! Minute must be between 0 and 60 inclusive")
        minute = int(input("Please enter the time (minute) to look up the status: "))
    lookup_time = datetime(2019, 11, 22, hour=hour, minute=minute)

    print()
    print("========Look-up function========")
    print("1. Look-up by package ID number")
    print("2. Look-up by delivery address")
    print("3. Look-up by delivery deadline")
    print("4. Look-up by delivery city")
    print("5. Look-up by delivery zip code")
    print("6. Look-up by package weight")
    print("7. Look-up by delivery status (Options: idle, on route, delivered)")
    print("8. Show the status of ALL packages.")
    print("0. exit")

    choice = input("Please enter your choice: ")

    return choice, lookup_time


if __name__ == '__main__':
    main()
    show_menu()
