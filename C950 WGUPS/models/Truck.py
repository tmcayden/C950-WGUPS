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
        self.totalDeliveryTime = 0
        self.lastDepartureTime = 0
        self.estimatedArrivalTime = 0

    # Print Truck Information for testing
    def print(self):
        print("\n## Information for Truck ID:", self.id, "##\n\nCapacity:", self.capacity,
              "\nSpeed:", self.speed, "\ntotalMiles:", self.totalMiles, "\nCurrent Address:",
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

    # Main algorithm to choose the closest package based on current location.
    def chooseClosestPackage(self, distanceHash):
        # This function is called upon arriving at the next location.
        if self.getNextAddress() != None:
            self.setCurrentAddress(self.getNextAddress())
        # Set a high min distance to compare to.
        minDistance = 100.0
        # Define next package to store the closest package so far
        nextPackage = None
        for package in self.getPackages():
            # Get the Location Object of the address that the package needs to go to.
            packageLocation = distanceHash.search(package.getAddress())
            # Get the Location object of the current address of the truck
            currentLocation = distanceHash.search(self.getCurrentAddress())
            # Compare the id's of the objects to ensure we are comparing them correctly on our distance tables.
            if packageLocation.getId() < currentLocation.getId():
               distance = currentLocation.getDistance(packageLocation.getId())
            else:
               distance = packageLocation.getDistance(currentLocation.getId())
            #print("Comparing Address: ", packageLocation.getName(), "to", currentLocation.getName())
            #print("Comparing " + str(distance) + " to " + str(minDistance))
            # Check if the package we are currently looking at is closer than the previously found "closest" package
            if float(distance) < minDistance:
                # Store the current smallest distance
               minDistance = float(distance)
                # Store the current closest package
               nextPackage = package

        # Update information based on the next closest package
        self.setNextAddress(nextPackage.getAddress())
        self.setPackageInProgress(nextPackage)
        self.setCurrentDistance(minDistance)
        print("Truck", self.getId(), "is beginning to deliver package", nextPackage.getId(), "Which is at the address:", self.nextAddress + ":", minDistance, "miles away!")
        return nextPackage

    def deliverPackage(self, delivered_list):
        # Update truck status
        if (self.getStatus() != "En Route for Delivery"):
            self.setStatus("En Route for Delivery")
        # Get the current package being delivered
        package = self.getPackageInProgress()
        # Update the current address
        self.setCurrentAddress(package.getAddress())
        # Add the miles it took to travel to this delivery point to the total miles driven for the truck
        self.totalMiles += self.getCurrentDistance()
        print("Truck", self.getId(), "is delivering package", package.getId())
        # Add the package to the list of delivered packages
        delivered_list.append(package)
        print("package", package.getId(), "successfully added to delivered list")
        # Remove the package from the truck's package list
        self.packages.remove(package)
        # Set the current pacakge in progress to none
        print("package", package.getId(), "successfully removed from truck")
        self.setPackageInProgress(None)

        # TODO: UPDATE next address to none


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
        print("Truck", self.getId(), "is returning to Hub. Currently", self.getCurrentDistance(), "miles away!")
        # TODO: Travel to the hub. For now, we just add the distance to total distance traveled.
        self.totalMiles += self.getCurrentDistance()
        self.setCurrentAddress(hub.getAddress())
        self.setNextAddress(None)
        self.setStatus("At Hub")

