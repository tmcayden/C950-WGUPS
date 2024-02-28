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
        self.truck = None

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

    # Function to print package info. Used when the user needs to lookup information about the package
    def listData(self):
        print("Package ID:", self.id, "\n###\nAddress:", self.address, ",", self.city, ",", self.state, self.zip_code,
              "\nDeadline:", self.deadline, "\nWeight:", self.weight, "\nSpecial Note:", self.notes,
              "\nAssigned to Truck:", self.truck, "\nStatus:", self.status, "\nTime Selected For Delivery:",
              self.beginDeliveryTime, "\nTime Delivered:", self.deliveryTime, end="\n\n")

    def getId(self):
        return self.id

    def setCity(self, newCity):
        self.city = newCity

    def setNote(self, newNote):
        self.notes = newNote

    def setZip(self, newZip):
        self.zip_code = newZip

    def getNote(self):
        return self.notes

    def setAddress(self, newAddress):
        self.address = newAddress

    def getAddress(self):
        return self.address

    def setBeginDeliveryTime(self, time):
        self.beginDeliveryTime = time

    def setDeliveryTime(self, time):
        self.deliveryTime = time

    def setStatus(self, status):
        self.status = status

    def getDeadline(self):
        return self.deadline

    # This function determines if the package is delivered on time. It will check if the deadline for delivery has
    # already passed. If it has, it updated that the package was late. If it was on time, it's updated accordingly.
    def updateStatus(self):
        if self.deliveryTime <= self.deadline:
            self.status = "Delivered On Time"
        else:
            self.status = "Delivered Late"

    def setTruck(self, truck):
        self.truck = truck
