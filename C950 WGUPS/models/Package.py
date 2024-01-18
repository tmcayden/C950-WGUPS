class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes, status, deliveryTime):
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.deliveryTime = deliveryTime

    def listData(self):
        return(self.id, self.address, self.city, self.state, self.zip_code, self.deadline, self.weight, self.notes, self.status, self.deliveryTime)

    def getId(self):
        return self.id

    def getAddress(self):
        return self.address


    #def getLocationDistances(self, distanceHash):
