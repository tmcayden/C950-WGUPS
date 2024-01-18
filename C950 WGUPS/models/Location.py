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

    def getSize(self):
        return len(self.distances)

    def getName(self):
        return self.name

    def getMinDistance(self):
        min = 100
        for distance in self.distances:
            if distance < min:
                min = distance

    def getId(self):
        return self.id

    def getAddress(self):
        return self.address