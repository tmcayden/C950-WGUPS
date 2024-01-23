import datetime

class Truck:
    def __init__(self, id, currentAddress):
        self.id = id
        self.capacity = 16
        self.speed = 18
        self.totalMiles = 0
        self.currentAddress = currentAddress
        self.packages = []
        self.driverId = None
        self.status = "At Hub"
        self.nextAddress = None
        self.PackageInProgess = None
        self.currentDistance = 0
        self.totalDeliveryTime = datetime.timedelta(hours=0)
        self.lastDepartureTime = None
        self.estimatedArrivalTime = datetime.timedelta(hours=0)
        self.currentTravelTime = datetime.timedelta(hours=0)

    # Print Truck Information for testing
    def print(self):
        print("\n## Information for Truck ID:", self.id, "##\n\nCapacity:", self.capacity,
              "\nSpeed:", self.speed, "\ntotalMiles:", self.totalMiles, "\nTotal Delivery Time:", self.totalDeliveryTime, "\nCurrent Address:",
              self.currentAddress, "\nPackages:", end=" ")
        for package in self.packages:
            print(package.id, end=", ")
        print("\nDriverId:", self.driverId, "\nStatus:", self.status, "\nNext Address:", self.nextAddress)

    def getId(self):
        return self.id

    # Set the truck Driver
    def setDriver(self, driver):
        if driver != None:
            self.driverId = driver.getId()
            driver.setStatus("On Truck " + str(self.getId()))
        else:
            self.driverId = None

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    # Add Packages to Trucks
    def setPackage(self, package):
        if len(self.packages) < 16:
            self.packages.append(package)
        else:
            print("Unable to add package: The truck has reached its capacity!")

    # Retrieve a package by ID from the truck
    def getPackage(self, packageId):
        for package in self.packages:
            if package.getId() == packageId:
                return package
    def getPackages(self):
        return self.packages

    def setCurrentDistance(self, currentDistance):
        self.currentDistance = currentDistance

    def getCurrentDistance(self):
        return self.currentDistance

    # Change the location of the truck
    def setCurrentAddress(self, currentAddress):
        self.currentAddress = currentAddress

    def getCurrentAddress(self):
        return self.currentAddress

    def setNextAddress(self, nextAddress):
        self.nextAddress = nextAddress

    def getNextAddress(self):
        return self.nextAddress

    def setPackageInProgress(self, packageInProgess):
        self.packageInProgress = packageInProgess

    def getPackageInProgress(self):
        return self.packageInProgress

    def setCurrentTravelTime(self, time):
        self.currentTravelTime = time

    def getCurrentTravelTime(self):
        return self.currentTravelTime

    def getEstimatedArrivalTime(self):
        return self.estimatedArrivalTime

    def setEstimatedArrivalTime(self, time):
        self.estimatedArrivalTime = time

    def setDepartureTime(self, time):
        self.lastDepartureTime = time

    def getDepartureTime(self):
        return self.lastDepartureTime


    # Main algorithm to choose the closest package based on current location.
    # This function is called upon arriving at the next location.
    def chooseClosestPackage(self, distanceHash):
        # See if a next address has already been assigned
        if self.getNextAddress() != None:
            self.setCurrentAddress(self.getNextAddress())
        # Set a high min distance to compare to.
        minDistance = 100.0
        # Define next package to store the closest package so far
        nextPackage = None
        # Get the Location object of the current address of the truck
        currentLocation = distanceHash.search(self.getCurrentAddress())
        for package in self.getPackages():
            # Get the Location Object of the address that the package needs to go to.
            packageLocation = distanceHash.search(package.getAddress())
            # Compare the id's of the objects to ensure we are comparing them correctly on our distance tables.
            if packageLocation.getId() < currentLocation.getId():
               distance = currentLocation.getDistance(packageLocation.getId())
            else:
               distance = packageLocation.getDistance(currentLocation.getId())
            # Compare the current package's destination from current location
            if float(distance) < minDistance:
                # Store the current smallest distance
                minDistance = float(distance)
                # Store the current closest package
                nextPackage = package

        # Update information based on the next closest package
        self.setNextAddress(nextPackage.getAddress())
        self.setPackageInProgress(nextPackage)
        self.setCurrentDistance(minDistance)

        #print("Truck", self.getId(), "is beginning to deliver package", nextPackage.getId(), "Which is at the address:",
        #      self.nextAddress + ":", minDistance, "miles away!")
        #print("Travel time", self.getCurrentTravelTime())
        #print("Estimated Arrival Time: ", self.getEstimatedArrivalTime())

    # Called to update the time the truck left its last stop, and when it will arrive at the next stop
    def updateDepartureTimeAndEstimatedArrivalTime(self):
        # Calculate the estimated time the package will be delivered
        self.setCurrentTravelTime(self.getTravelTime())
        self.setEstimatedArrivalTime(self.lastDepartureTime + self.getCurrentTravelTime())
        # Update the time the package was chosen to be delivered
        package = self.getPackageInProgress()
        package.setBeginDeliveryTime(self.lastDepartureTime)


    # Function called after arriving to the package location.
    # This updates the truck information to display where the truck and will also add the delivery time to the package.
    def deliverPackage(self, delivered_list):
        # Update truck status
        if (self.getStatus() != "En Route for Delivery"):
            self.setStatus("En Route for Delivery")
        # Get the current package being delivered
        package = self.getPackageInProgress()
        # Update the delivery time of the package
        package.setDeliveryTime(self.getEstimatedArrivalTime())
        # Update package status to display on time or late
        package.updateStatus()
        # Update the total delivery time
        self.totalDeliveryTime += self.getCurrentTravelTime()
        # Update the departure time
        self.lastDepartureTime = self.getEstimatedArrivalTime()
        # Update the current address
        self.setCurrentAddress(package.getAddress())
        # Add the miles it took to travel to this delivery point to the total miles driven for the truck
        self.totalMiles += self.getCurrentDistance()
        #print("Truck", self.getId(), "delivered", package.getId(), "at", self.getEstimatedArrivalTime())
        # Add the package to the list of delivered packages
        delivered_list.append(package)
        # Remove the package from the truck's package list
        self.packages.remove(package)
        # Set the current pacakge in progress to none
        self.setPackageInProgress(None)

    def toHub(self, distanceHash):
        # Update truck status
        self.setStatus("Returning to Hub")
        # Update current address to be the address of the last delivered package
        self.setCurrentAddress(self.getNextAddress())
        # Update next address to be the Hub address
        self.setNextAddress("4001 S 700 E")
        # Get Location objects for hub and current location
        hub = distanceHash.search(self.getNextAddress())
        currentLocation = distanceHash.search(self.getCurrentAddress())
        # Find out how far away the hub is
        self.setCurrentDistance(float(currentLocation.getDistance(hub.getId())))
        #print("Truck", self.getId(), "is returning to Hub. Currently", self.getCurrentDistance(), "miles away!")
        # TODO: Travel to the hub. For now, we just add the distance to total distance traveled.
        # Calculate how long it will tak to get to the hub
        self.setCurrentTravelTime(self.getTravelTime())
        # Update Estimated Arrival Time
        self.setEstimatedArrivalTime(self.lastDepartureTime + self.getCurrentTravelTime())

    # Method for once the truck actually arrives at the hub.
    def arriveAtHub(self):
        # Update total miles
        self.totalMiles += self.getCurrentDistance()
        # Update travel time
        self.totalDeliveryTime += self.getCurrentTravelTime()
        # Update address
        self.setCurrentAddress("4001 S 700 E")
        # Update next address
        self.setNextAddress(None)
        # Update Status
        self.setStatus("Finished Deliveries")
        #print("Truck", self.getId(), "returned to hub at", self.getEstimatedArrivalTime())

    # getTravelTime gets the current distance to the next stop
    # and will calculate how long it will take to get there using avg truck speed.
    def getTravelTime(self):
        # Get the current distance away from the next location
        miles = self.getCurrentDistance()
        # Calculate the total number of seconds it will take to get there
        travelTime = (miles * 3600) / 18
        # Turn the time into a datetime object
        minutesPerMile = datetime.timedelta(seconds=travelTime)

        return minutesPerMile

    def deliverDelayedPackages(self, distanceHash):
        # See if a next address has already been assigned
        if self.getNextAddress() != None:
            self.setCurrentAddress(self.getNextAddress())
        # Set a high min distance to compare to.
        minDistance = 100.0
        # Define next package to store the closest package so far
        nextPackage = None
        # Get the Location object of the current address of the truck
        currentLocation = distanceHash.search(self.getCurrentAddress())
        # Find which packages have priority based on deadline
        priority = []
        for package in self.getPackages():
            if package.getDeadline() != datetime.timedelta(hours=16):
                priority.append(package)

        if len(priority) > 0:
            for package in priority:
                # Get the Location Object of the address that the package needs to go to.
                packageLocation = distanceHash.search(package.getAddress())
                # Compare the id's of the objects to ensure we are comparing them correctly on our distance tables.
                if packageLocation.getId() < currentLocation.getId():
                    distance = currentLocation.getDistance(packageLocation.getId())
                else:
                    distance = packageLocation.getDistance(currentLocation.getId())
            # Compare the current package's destination from current location
        else:
            for package in self.getPackages():
                # Get the Location Object of the address that the package needs to go to.
                packageLocation = distanceHash.search(package.getAddress())
                # Compare the id's of the objects to ensure we are comparing them correctly on our distance tables.
                if packageLocation.getId() < currentLocation.getId():
                    distance = currentLocation.getDistance(packageLocation.getId())
                else:
                    distance = packageLocation.getDistance(currentLocation.getId())
        # Compare the current package's destination from current location
        if float(distance) < minDistance:
            # Store the current smallest distance
            minDistance = float(distance)
            # Store the current closest package
            nextPackage = package

        # Update information based on the next closest package
        self.setNextAddress(nextPackage.getAddress())
        self.setPackageInProgress(nextPackage)
        self.setCurrentDistance(minDistance)