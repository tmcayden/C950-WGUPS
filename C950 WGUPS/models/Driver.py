class Driver:
    def __init__(self, id):
        self.id = id
        self.status = "At Hub"

    # Retrieve driver Id
    def getId(self):
        return self.id

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status