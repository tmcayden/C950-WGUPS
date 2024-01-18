from models.Location import Location
from models.Package import Package
import csv
class PackageHash:
    def __init__(self, initial_capacity):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def _myHashFunc(self, key):
        bucket = ((key * 7) + 27)
        return bucket % len(self.table)

    def insert(self, key, data):
        bucket = self._myHashFunc(key)
        bucket_list = self.table[bucket]

        for pair in bucket_list:
            if pair[0] == key:
                pair[1] = data
                return True
        key_value = [key, data]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        bucket = self._myHashFunc(key)
        for pair in self.table[bucket]:
            if pair[0] == key:
                return pair[1]
        return None

    def getLocationName(self, key):
        bucket = self._myHashFunc(key)
        for pair in self.table[bucket]:
            if pair[0] == key:
                return pair[1]

    def delete(self, key):
        bucket = self._myHashFunc(key)
        for i in range(0, len(self.table[bucket])):
            if self.table[bucket][i][0] == key:
                self.table[bucket].pop(i)
                return True

    # Setup package hash with formatted csv file as input
    def loadPackageData(self, fileName):
        with open(fileName) as packages:
            packageData = csv.reader(packages, delimiter=',')
            for package in packageData:
                pId = int(package[0])
                pAddress = str(package[1])
                pCity = str(package[2])
                pState = str(package[3])
                pZipCode = str(package[4])
                pDeadline = str(package[5])
                pWeight = str(package[6])
                pNotes = str(package[7])
                pStatus = "AT HUB"
                deliveryTime = "Not Delivered"

                package = Package(pId, pAddress, pCity, pState, pZipCode, pDeadline, pWeight, pNotes, pStatus,
                                  deliveryTime)
                self.insert(pId, package)
