# This is a location object that will mostly be used to access each locations distance row
# from the distances sheet provided.
class Location:
    def __init__(self, id, name, address, zip_code, distances):
        self.id = id
        self.name = name
        self.address = address
        self.zip_code = zip_code
        self.distances = distances

    def getDistance(self, other_hub_id):
        return self.distances[other_hub_id]

    def listData(self):
        return (self.id, self.name, self.address, self.zip_code, self.distances)

    # Returns the ID (the index of the distance row) for the distance object
    # This is used to compare the distance of one location to another
    def getId(self):
        return self.id

    def getAddress(self):
        return self.address