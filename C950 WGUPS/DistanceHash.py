from models.Location import Location
import csv
class DistanceHash:
    # Initialize hash with an array of length initial_capacity and populate each index with an empty array
    def __init__(self, initial_capacity):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Hash function for quick insert and search functions
    def _myHashFunc(self, key):
        sum = 0
        # Since we are using the address as the key,
        # sum the ASCII values of each character in the address
        for char in key:
            sum += ord(char)
        return sum % len(self.table)

    # Called to add data to the table by hashing the key inserted
    def insert(self, key, data):
        # Find which bucket the data will go in
        bucket = self._myHashFunc(key)
        # retrieve the list located in that bucket
        bucket_list = self.table[bucket]
        # Iterate through items already in the list
        for pair in bucket_list:
            # Check if key is already in the data structure
            if pair[0] == key:
                # Key was found, update the old data to the new data
                pair[1] = data
                return True
        # If the key doesn't already exist, add the new key value to the bucket
        key_value = [key, data]
        bucket_list.append(key_value)
        return True

    # Retrieve data from the table by key
    def search(self, key):
        # Find out which bucket the key corresponds to
        bucket = self._myHashFunc(key)
        # Search the list found in the bucket to see if the key exists
        for pair in self.table[bucket]:
            # Check if the key matches
            if pair[0] == key:
                # Return the data if found
                return pair[1]
        return None

    # Not used in the program -- used to find data in the data structure and remove it.
    def delete(self, key):
        bucket = self._myHashFunc(key)
        for i in range(0, len(self.table[bucket])):
            if self.table[bucket][i][0] == key:
                self.table[bucket].pop(i)
                return True

    # Setup distances hash with formatted csv file as input
    def loadDistances(self, fileName):
        # open the file to retrieve data
        with open(fileName) as distances:
            # Create a list storing individual package information
            distances = csv.reader(distances, delimiter=',')
            # Keep track of index to use as the id of the location.
            # This will allow us to follow exactly along the distance table provided as index values will be the same
            for index, location in enumerate(distances):
                # Extract the address so that we can input it as they key in the hash table
                locationAddress = str(location[1])
                # create a location object
                locale = Location(index, location[0], location[1], location[2], location[3:])
                # Add the location object to the hash table.
                self.insert(locationAddress, locale)
