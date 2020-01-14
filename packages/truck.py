# Dawei Li, 001022014

from datetime import timedelta
from datetime import datetime
import packages.data as data
from .hash_table import MyHashTable


class Truck(object):
    def __init__(self, max_load=16):
        self.loads = MyHashTable(max_load)
        self.package_count = 0
        # Trucks travel at an average speed of 18 miles per hour.
        self.speed = 18
        self.curr_time = None
    
    def load_truck(self, package_id, package_values):
        """Load the truck with packages"""
        # Load a package into the truck
        self.loads.add(package_id, package_values)
        self.package_count += 1

    def deliver(self, start_time, start_location):
        """Deliver packages using a greedy algorithm."""
        # Set the status of each packate to "on route"
        # Add an attribute "on route time"
        self.set_on_route(start_time)

        travel_distance = 0
        curr_location = start_location
        self.curr_time = start_time
        # Get all undelivered package IDs.
        undelivered = self.get_undelivered_packages_id()
        while len(undelivered) > 0:
            # Initialize the package whose location is 
            # the closest to the current location.
            min_id = undelivered[0]
            min_location = self.get_location(min_id)
            min_distance = data.distance_data.get((curr_location, min_location))
            if min_distance is None:
                min_distance = data.distance_data.get((min_location, curr_location))
            # Iterate through the undelivered packages to find the package 
            # whose location is the closest to the current location.
            for i in range(1, len(undelivered)):
                id = undelivered[i]
                location = self.get_location(id)
                distance = data.distance_data.get((curr_location, location))
                if distance is None:
                    distance = data.distance_data.get((location, curr_location))
                if distance < min_distance:
                    min_id = id
                    min_location = location
                    min_distance = distance
            
            # Increment travel distance.
            travel_distance += min_distance
            # Set the current location to the location of the chosen package.
            curr_location = min_location
            # Change the status of the chosen package to "delivered", 
            # and add its delivery time.
            self.set_delivered(min_id, self.curr_time, min_distance)

            # If a package is delivered beyond its deadline, stop the delivery
            # and return False.
            delivery_time = data.package_data.get(min_id).get("delivery time")
            deadline = data.package_data.get(min_id).get("deadline")
            if delivery_time > deadline:
                # print("Package ", min_id, " was not delivered on time.")
                return False

            # Update the list of undelivered packages
            undelivered = self.get_undelivered_packages_id()
        # After the last package is delivered, drive the truck back to the start_location.
        distance = data.distance_data.get((curr_location, start_location))
        curr_location = start_location
        travel_distance += distance
        data.total_distance += travel_distance
        return True
            
    def is_empty(self):
        return self.package_count == 0
    
    def get_undelivered_packages_id(self):
        """Return a list of the ids of undelivered packages."""
        packages_id = []
        packages = self.loads.buckets
        for i in range(len(packages)):
            if packages[i] is not None:
                for key_value_pair in packages[i]:
                    if key_value_pair[1].get("status") != "delivered":
                        packages_id.append(key_value_pair[0])
        return packages_id
    
    def get_location(self, id):
        """ Given a package id, return its delivery location."""
        return self.loads.get(id).get("address")
    
    def set_on_route(self, start_time):
        """Change all packages' status to 'on route'."""
        packages = self.loads.buckets
        for i in range(len(packages)):
            if packages[i] is not None:
                for key_value_pair in packages[i]:
                    id = key_value_pair[0]
                    data.package_data.get(id).add("status", "on route")
                    data.package_data.get(id).add("on route time", start_time)

    def set_delivered(self, id, curr_time, distance):
        """Change a package's status to delivered, and set its delivery time"""
        data.package_data.get(id).add("status", "delivered")
        travel_time = timedelta(hours=distance/self.speed)
        self.curr_time += travel_time
        data.package_data.get(id).add("delivery time", self.curr_time)
