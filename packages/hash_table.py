# Dawei Li, 001022014

class MyHashTable(object):
    def __init__(self, size=50):
        self.buckets = [None] * size
        self.occupied = 0

    def hash(self, key):
        return hash(key) % len(self.buckets)

    def add(self, key, value):
        """Add a key value pair to the hash table"""
        key_hash = self.hash(key)
        if self.buckets[key_hash] is None:
            # If the bucket is empty, create a new list.
            self.buckets[key_hash] = []
            self.buckets[key_hash].append([key, value])
            self.occupied += 1
            if self.is_half_full():
                self.double_size()
        else:
            exist = False
            for key_value_pair in self.buckets[key_hash]:
                # When there are identical keys, update the value of the existing key.
                # Can be used to update the values of a key.
                if key_value_pair[0] == key:
                    exist = True
                    key_value_pair[1] = value
                    break
            if exist is False:
                # Append the new key value pair to the existing list.
                self.buckets[key_hash].append([key, value])
                if self.is_half_full():
                    self.double_size()

    def get(self, key):
        """Get the value from a specific key"""
        key_hash = self.hash(key)
        if self.buckets[key_hash] is not None:
            for key_value_pair in self.buckets[key_hash]:
                if key_value_pair[0] == key:
                    return key_value_pair[1]
            return None
        else:
            return None

    def all_keys(self):
        """ Return a list of all keys in the hash table."""
        keys = []
        for i in range(len(self.buckets)):
            if self.buckets[i] is not None:
                for key_value_pair in self.buckets[i]:
                    keys.append(key_value_pair[0])
        return keys

    def is_half_full(self):
        """Check if more than half of the buckets are occupied"""
        if self.occupied / len(self.buckets) >= 1/2:
            return True
        return False

    def double_size(self):
        """Double the size of the hash table"""
        # Create a new hash table with size doubled
        new_hash_table = MyHashTable(size=len(self.buckets)*2)
        # Iterate through the old hash table, copy items to the new hash table
        for index in range(len(self.buckets)):
            if self.buckets[index] is None:
                continue
            for key_value_pair in self.buckets[index]:
                new_hash_table.add(key_value_pair[0], key_value_pair[1])
        # Replace the old hash table with the new one
        self.buckets = new_hash_table.buckets
        self.occupied = new_hash_table.occupied

    def print_all(self, status):
        """Print all key-value-pairs"""
        for index in range(len(self.buckets)):
            if self.buckets[index] is None:
                continue
            for key_value_pair in self.buckets[index]:
                key = key_value_pair[0]
                if key=="delivery time" or key=="on route time" or key=="deadline":
                    hour = key_value_pair[1].hour
                    minute = key_value_pair[1].minute
                    time = str(hour) + ":" + str("%02d" %minute)
                    print(key_value_pair[0], ":", time)
                elif key_value_pair[0] == "status":
                    print("status", ":", status)
                else:
                    print(key_value_pair[0], ":", key_value_pair[1])
