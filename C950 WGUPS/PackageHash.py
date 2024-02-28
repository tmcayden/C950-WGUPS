from models.Package import Package
import csv
class PackageHash:
    # Initialize hash with an array of length initial_capacity and populate each index with an empty array
    def __init__(self, initial_capacity):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Hash function for quick insert and search functions
    def _myHashFunc(self, key):
        bucket = ((key * 7) + 27)
        return bucket % len(self.table)

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

    # Setup package hash with formatted csv file as input
    def loadPackageData(self, fileName, masterPackageList):
        # open the file to retrieve data
        with open(fileName) as packages:
            # Create a list storing individual package information
            packageData = csv.reader(packages, delimiter=',')
            # Parse the list information to separate variables
            for package in packageData:
                pId = int(package[0])
                pAddress = str(package[1])
                pCity = str(package[2])
                pState = str(package[3])
                pZipCode = str(package[4])
                pDeadline = str(package[5])
                pWeight = str(package[6])
                pNotes = str(package[7])
                # Add a default status and delivery time to be printed when the package is brought to the hub
                pStatus = "Waiting to be loaded..."
                deliveryTime = "Not Delivered"
                # Create a package object
                package = Package(pId, pAddress, pCity, pState, pZipCode, pDeadline, pWeight, pNotes, pStatus,
                                  deliveryTime)
                # Insert the package to the data structure using the package ID as they key and the package object as
                # the data to be inserted
                self.insert(pId, package)
                # Add the package to the global variable masterPackageList.
                # This is so we can access it anytime.
                masterPackageList.append(package)
