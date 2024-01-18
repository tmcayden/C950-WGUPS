# Thomas Hunsaker
# Student ID: 010594224

from models.Truck import Truck
from models.Driver import Driver
from PackageHash import PackageHash
from DistanceHash import DistanceHash

# Create a list to keep track of which packages have been successfully delivered
global delivered_list

# Create global hashmaps to store package and distance data
global packageHash
global distanceHash

def getLocationByPackage(package):
    location_distances = distanceHash.search(package.getAddress())
    return location_distances


if __name__ == '__main__':
    # define and setup packageHash to store package information
    packageHash = PackageHash(40)
    # define and setup distanceHash to store distance information for each location
    distanceHash = DistanceHash(27)
    # Populate packageHash with formatted csv data
    packageHash.loadPackageData('csv/packageCSV.csv')
    # Populate distanceHash with formatted csv data
    distanceHash.loadDistances('csv/distanceCSV.csv')
    delivered_list = []
    # Setup Trucks with starting point of WGU HUB
    truck1 = Truck(1, "4001 S 700 E")
    truck2 = Truck(2, "4001 S 700 E")
    truck3 = Truck(3, "4001 S 700 E")

    special_note_packages = []
    deadline_packages = []

    # Setup 2 Drivers with each ID
    driver1 = Driver(1)
    driver2 = Driver(2)

    # Populate Truck 1 with packages that have the earliest deadlines, but no special instructions
    truck1.setPackage(packageHash.search(1))
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
    truck1.setPackage(packageHash.search(37))
    truck1.setPackage(packageHash.search(40))

    # Load Truck 2 with all special note packages, and others to do most of the deliveries
    truck2.setPackage(packageHash.search(2))
    truck2.setPackage(packageHash.search(3))
    truck2.setPackage(packageHash.search(4))
    truck2.setPackage(packageHash.search(5))
    truck2.setPackage(packageHash.search(7))
    truck2.setPackage(packageHash.search(8))
    truck2.setPackage(packageHash.search(10))
    truck2.setPackage(packageHash.search(11))
    truck2.setPackage(packageHash.search(12))
    truck2.setPackage(packageHash.search(17))
    truck2.setPackage(packageHash.search(18))
    truck2.setPackage(packageHash.search(21))
    truck2.setPackage(packageHash.search(22))
    truck2.setPackage(packageHash.search(36))
    truck2.setPackage(packageHash.search(38))
    truck2.setPackage(packageHash.search(39))

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
    truck3.setPackage(packageHash.search(33))
    truck3.setPackage(packageHash.search(35))

    truck1.setDriver(driver1)
    truck2.setDriver(driver2)
    print("\n")

    for i in range(len(truck1.getPackages())):
        truck1.chooseClosestPackage(distanceHash)
        print("\n")
        truck1.deliverPackage(delivered_list)
        print("\n")
        truck1.print()
        print("\n")
    truck1.toHub(distanceHash)
    truck1.setDriver(None)

    for i in range(len(truck2.getPackages())):
        truck2.chooseClosestPackage(distanceHash)
        print("\n")
        truck2.deliverPackage(delivered_list)
        print("\n")
        truck2.print()
        print("\n")
    truck2.toHub(distanceHash)
    truck2.setDriver(None)

    truck3.setDriver(driver1)

    for i in range(len(truck3.getPackages())):
        truck3.chooseClosestPackage(distanceHash)
        print("\n")
        truck3.deliverPackage(delivered_list)
        print("\n")
        truck3.print()
        print("\n")

    for package in delivered_list:
        print(package.getId())

    truck3.toHub(distanceHash)
    truck1.print()
    truck2.print()
    truck3.print()
