from models.Location import Location
import csv
class DistanceHash:
    def __init__(self, initial_capacity):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def _myHashFunc(self, key):
        sum = 0
        for char in key:
            sum += ord(char)
        return sum % len(self.table)

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

    def delete(self, key):
        bucket = self._myHashFunc(key)
        for i in range(0, len(self.table[bucket])):
            if self.table[bucket][i][0] == key:
                self.table[bucket].pop(i)
                return True

    # Setup distances hash with formatted csv file as input
    def loadDistances(self, fileName):
        with open(fileName) as distances:
            distances = csv.reader(distances, delimiter=',')
            for index, location in enumerate(distances):
                locationAddress = str(location[1])
                locale = Location(index, location[0], location[1], location[2], location[3:])
                self.insert(locationAddress, locale)
