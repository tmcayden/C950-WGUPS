# Thomas Hunsaker
# Student ID: 010594224
import datetime
import os

from models.Truck import Truck
from models.Driver import Driver
from PackageHash import PackageHash
from DistanceHash import DistanceHash

# Create a list to keep track of which packages have been successfully delivered
global delivered_list

# Create global hashmaps to store package and distance data
global packageHash
global distanceHash

# Create a master package list to be able to quickly see the status of all packages
global masterPackageList

# Create a global time object to manage time
global globalTime

if __name__ == '__main__':
    # initialize the masterPackageList
    masterPackageList = []
    # Set the globalTime object to be 8:00 AM
    globalTime = datetime.timedelta(hours=8)
    # Incremental variable to increase time by a second
    secondPassed = datetime.timedelta(minutes=5)
    # Create a time object for delayed packages to check for when they arrive
    delayedPackageArrival = datetime.timedelta(hours=9, minutes=5)
    # Bool to determine if truck3 has alrady been loaded
    truck3NotLoaded = True
    # Bool to determine if truck3 has left
    truck3Left = False
    # define and setup packageHash to store package information
    packageHash = PackageHash(40)
    # define and setup distanceHash to store distance information for each location
    distanceHash = DistanceHash(27)
    # Populate packageHash with formatted csv data
    packageHash.loadPackageData('csv/packageCSV.csv', masterPackageList)
    # Populate distanceHash with formatted csv data
    distanceHash.loadDistances('csv/distanceCSV.csv')
    delivered_list = []
    # Setup Trucks with starting point of WGU HUB
    truck1 = Truck(1, "4001 S 700 E")
    truck2 = Truck(2, "4001 S 700 E")
    truck3 = Truck(3, "4001 S 700 E")

    # Setup departure time for trucks 1 and 2 to be 8:00 AM
    truck1.setDepartureTime(globalTime)
    truck2.setDepartureTime(globalTime)

    # Setup 2 Drivers with each ID
    driver1 = Driver(1)
    driver2 = Driver(2)

    # Populate Truck 1 with packages that have the earliest deadlines, but no special instructions
    truck1.setPackage(packageHash.search(1))
    truck1.setPackage(packageHash.search(8))
    truck1.setPackage(packageHash.search(13))
    truck1.setPackage(packageHash.search(14))
    truck1.setPackage(packageHash.search(15))
    truck1.setPackage(packageHash.search(16))
    truck1.setPackage(packageHash.search(19))
    truck1.setPackage(packageHash.search(20))
    truck1.setPackage(packageHash.search(29))
    truck1.setPackage(packageHash.search(30))
    truck1.setPackage(packageHash.search(31))
    truck1.setPackage(packageHash.search(34))
    truck1.setPackage(packageHash.search(40))

    # Load Truck 2 with all special note packages, and others to do most of the deliveries
    truck2.setPackage(packageHash.search(2))
    truck2.setPackage(packageHash.search(3))
    truck2.setPackage(packageHash.search(4))
    truck2.setPackage(packageHash.search(5))
    truck2.setPackage(packageHash.search(7))
    truck2.setPackage(packageHash.search(10))
    truck2.setPackage(packageHash.search(11))
    truck2.setPackage(packageHash.search(12))
    truck2.setPackage(packageHash.search(17))
    truck2.setPackage(packageHash.search(18))
    truck2.setPackage(packageHash.search(21))
    truck2.setPackage(packageHash.search(22))
    truck2.setPackage(packageHash.search(33))
    truck2.setPackage(packageHash.search(36))
    truck2.setPackage(packageHash.search(37))
    truck2.setPackage(packageHash.search(38))

    # Assign the two drivers to the first two trucks
    truck1.setDriver(driver1)
    truck2.setDriver(driver2)

    #Select closest package for Truck1 and Truck2
    truck1.chooseClosestPackage(distanceHash)
    truck2.chooseClosestPackage(distanceHash)

    # Update arrival and departure times for trucks 1 and 2
    truck1.updateDepartureTimeAndEstimatedArrivalTime()
    truck2.updateDepartureTimeAndEstimatedArrivalTime()

    # Loop until all packages are delivered.
    while (truck1.getStatus() != "Finished Deliveries" or truck2.getStatus() != "Finished Deliveries"
           or truck3.getStatus() != "Finished Deliveries"):

        # Check if truck1 arrived at its package location
        if truck1.getEstimatedArrivalTime() <= globalTime and truck1.getStatus() != "Finished Deliveries":
            # Check if the truck was returning to the hub
            if truck1.getStatus() != "Returning to Hub":
                # Deliver the current package
                truck1.deliverPackage(delivered_list)
                # Check if there are still packages to be delivered
                if len(truck1.getPackages()) > 0:
                    # Choose the next closest package
                    truck1.chooseClosestPackage(distanceHash)
                    # Update time
                    truck1.updateDepartureTimeAndEstimatedArrivalTime()
                else:
                    # If no more packages, return to hub
                    truck1.toHub(distanceHash)
            else:
                truck1.arriveAtHub()
                truck1.setDriver(None)

        # Check if truck2 arrived at its location
        if truck2.getEstimatedArrivalTime() <= globalTime and truck2.getStatus() != "Finished Deliveries":
            if truck2.getStatus() != "Returning to Hub":
                truck2.deliverPackage(delivered_list)
                if len(truck2.getPackages()) > 0:
                    truck2.chooseClosestPackage(distanceHash)
                    truck2.updateDepartureTimeAndEstimatedArrivalTime()
                else:
                    truck2.toHub(distanceHash)
            else:
                truck2.arriveAtHub()
                truck2.setDriver(None)

        if globalTime >= delayedPackageArrival and truck3NotLoaded:
            # Load Truck 3 with all leftover packages, most importantly those that are delayed, or have the wrong address
            truck3.setPackage(packageHash.search(6))
            truck3.setPackage(packageHash.search(9))
            truck3.setPackage(packageHash.search(23))
            truck3.setPackage(packageHash.search(24))
            truck3.setPackage(packageHash.search(25))
            truck3.setPackage(packageHash.search(26))
            truck3.setPackage(packageHash.search(27))
            truck3.setPackage(packageHash.search(28))
            truck3.setPackage(packageHash.search(32))
            truck3.setPackage(packageHash.search(35))
            truck3.setPackage(packageHash.search(39))
            truck3.deliverDelayedPackages(distanceHash)
            truck3NotLoaded = False

        # Check to see if truck 3 has already been loaded, and Truck 1 has returned from its deliveries
        if not truck3NotLoaded and truck1.getStatus() == "Finished Deliveries":
            if not truck3Left:
                # Truck 3 can now be sent off and update the time it leaves the hub
                truck3.setDepartureTime(globalTime)
                # Use the updated time it left the hub to calculate the estimated arrival time.
                truck3.updateDepartureTimeAndEstimatedArrivalTime()
                truck3Left = True
            if truck3.getEstimatedArrivalTime() <= globalTime and truck3.getStatus() != "Finished Deliveries":
                if truck3.getStatus() != "Returning to Hub":
                    truck3.deliverPackage(delivered_list)
                    if len(truck3.getPackages()) > 0:
                        truck3.deliverDelayedPackages(distanceHash)
                        truck3.updateDepartureTimeAndEstimatedArrivalTime()
                    else:
                        truck3.toHub(distanceHash)
                else:
                    truck3.arriveAtHub()
                    truck3.setDriver(None)

        globalTime += secondPassed
