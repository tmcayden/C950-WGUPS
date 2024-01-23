import datetime

class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes, status, deliveryTime):
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.weight = weight
        self.notes = notes
        self.status = status
        self.beginDeliveryTime = None
        self.deliveryTime = deliveryTime

        # Set the deadline as a datetime object
        if deadline == "EOD":
            # Set deadline to 4pm for packages with no deadline
            self.deadline = datetime.timedelta(hours=16)
        else:
            # Remove " AM" from each time
            deadline = deadline[:-3]
            # Grab Hours
            hours = deadline[:-3]
            # Grab Minutes
            minutes = deadline[3:5]
            # Create datetime object with hours and minutes
            self.deadline = datetime.timedelta(hours=int(hours), minutes=int(minutes))


    def listData(self):
        print("Package ID:", self.id, "\nAddress:", self.address, ",", self.city, ",", self.state, self.zip_code,
              "\nDeadline:", self.deadline, "\nWeight:", self.weight, "\nSpecial Note:", self.notes, "\nStatus:",
              self.status, "\nTime Selected For Delivery:", self.beginDeliveryTime, "\nTime Delivered:",
              self.deliveryTime, end="\n\n")

    def getId(self):
        return self.id

    def getAddress(self):
        return self.address

    def setBeginDeliveryTime(self, time):
        self.beginDeliveryTime = time

    def setDeliveryTime(self, time):
        self.deliveryTime = time

    def updateStatus(self):
        if self.deliveryTime <= self.deadline:
            self.status = "Delivered On Time"
        else:
            self.status = "Delivered Late"

    def getDeadline(self):
        return self.deadline
