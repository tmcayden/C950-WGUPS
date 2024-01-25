# Thomas Hunsaker
# Student ID: 010594224
import datetime

from models.Truck import Truck
from models.Driver import Driver
from PackageHash import PackageHash
from DistanceHash import DistanceHash

def printPackages():
    for package in masterPackageList:
        package.listData()

def main():
    # Create a list to keep track of which packages have been successfully delivered
    global delivered_list
    # Create global hashmaps to store package and distance data
    global packageHash
    global distanceHash
    # Create a master package list to be able to quickly see the status of all packages
    global masterPackageList
    # Create a global time object to manage time
    global globalTime
    # Variable to hold the time that the packages should be printed at
    global printPackageTime
    # Variable to hold the package ID of a specific package to be looked up
    global package_search_id
    # initialize the masterPackageList
    masterPackageList = []
    # Set the globalTime object to be 8:00 AM
    globalTime = datetime.timedelta(hours=8)
    # Incremental variable to increase time by a second
    secondPassed = datetime.timedelta(seconds=1)
    # Create a time object for delayed packages to check for when they arrive
    delayedPackageArrival = datetime.timedelta(hours=9, minutes=5)
    # Bool to determine if truck3 has alrady been loaded
    truck3Loaded = False
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
    while globalTime < printPackageTime:
        # Check to see if the time is 10:20 AM. If so, update package 9's delivery address
        if datetime.timedelta(hours=10, minutes=20) == globalTime:
            # Update package 9's address with the correct information
            package = packageHash.search(9)
            package.setAddress("410 S State St")
            package.setCity("Salt Lake City")
            package.setZip("84111")
            package.setNote("Wrong address previously listed. The new address is correct.")

        # Check if truck1 arrived at its next location
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
                # Truck arrives back to Hub and the driver can be reassigned
                truck1.arriveAtHub()
                truck1.setDriver(None)

        # Check if truck2 arrived at the next location
        if truck2.getEstimatedArrivalTime() <= globalTime and truck2.getStatus() != "Finished Deliveries":
            # Check if the truck was returning to the hub
            if truck2.getStatus() != "Returning to Hub":
                # Deliver the current package
                truck2.deliverPackage(delivered_list)
                # Check if there are still packages to be delivered
                if len(truck2.getPackages()) > 0:
                    # Choose the next closest package
                    truck2.chooseClosestPackage(distanceHash)
                    # Update time
                    truck2.updateDepartureTimeAndEstimatedArrivalTime()
                else:
                    # If no more packages, return to hub
                    truck2.toHub(distanceHash)
            else:
                # Truck arrives back to Hub and the driver can be reassigned
                truck2.arriveAtHub()
                truck2.setDriver(None)

        if globalTime >= delayedPackageArrival and not truck3Loaded:
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
            truck3Loaded = True

        # Check to see if truck 3 has already been loaded, and Truck 1 has returned from its deliveries
        if truck3Loaded and truck1.getStatus() == "Finished Deliveries":
            if not truck3Left:
                # Truck 3 can now be sent off and update the time it leaves the hub
                truck3.setDepartureTime(globalTime)
                # Use the updated time it left the hub to calculate the estimated arrival time.
                truck3.updateDepartureTimeAndEstimatedArrivalTime()
                # Bool to know if truck3 has left so the departure time isn't updating each iteration
                truck3Left = True
            # Check to see if the truck3 has arrived at its location
            if truck3.getEstimatedArrivalTime() <= globalTime and truck3.getStatus() != "Finished Deliveries":
                # See if it was returning to the hub
                if truck3.getStatus() != "Returning to Hub":
                    # Deliver the current package
                    truck3.deliverPackage(delivered_list)
                    # See if there are more packages to be delivered
                    if len(truck3.getPackages()) > 0:
                        # Choose the next package to deliver based on deadline and distance
                        truck3.deliverDelayedPackages(distanceHash)
                        # Update time
                        truck3.updateDepartureTimeAndEstimatedArrivalTime()
                    else:
                        # Return the truck to the hub if there are no more packages
                        truck3.toHub(distanceHash)
                else:
                    # Truck arrives back to Hub and the driver can be reassigned
                    truck3.arriveAtHub()
                    truck3.setDriver(None)
        # Increment the global time by a second
        globalTime += secondPassed

    # See if the user wanted to search for a package by ID
    if package_search_id > 0:
        # Retrieve the package's data by ID.
        packageHash.search(int(package_search_id)).listData()
        print('\n')
    else:
        # If no ID was set, return the entire list of packages
        printPackages()
    # Print the total miles driven for all trucks at the end of each request. This will change based on the search
    # time entered in. (If the user requests info at a specific time, the truck mileage will be accurate to that time)
    print("\nTotal miles traveled on all trucks:", round(truck1.getTotalMiles() + truck2.getTotalMiles() +
                                                         truck3.getTotalMiles(), 2), "\n")
    input("\nPress enter to return to the menu.")

# Entry point of the program
if __name__ == '__main__':
    # Variable to store user input
    choice = ""
    # Menu for the user to interact with the program
    while choice != "q":
        print("############################")
        print("#\t\t\t\t\t\t   #\n#\t", end="")
        print("WGUPS Delivery System  #")
        print("#\t\t\t\t\t\t   #")
        print("############################")
        # Options for user
        print("\nPlease select an option:")
        print("\t1) See status of all packages at the end of day")
        print("\t2) See status of a single package by ID at the end of day")
        print("\t3) See the status of all packages at a specific time")
        print("\t4) See the status of a single package at a specific time by ID")
        print("\tPress \"q\" to exit\n")
        # Store the user's selection
        choice = input("Selection: ")

        # Determine what the choice was by using match-case
        match choice:
            case "1":
                # Set the variable printPackageTime to EOD so all deliveries are ensured to be completed
                printPackageTime = datetime.timedelta(hours=int(16))
                # Set default package ID to be 0 so that no individual package information is shown
                package_search_id = 0
            case "2":
                # Retrieve the desired package ID
                package_search_id = int(input("Enter a package ID: "))
                # Set the variable printPackageTime to EOD so all deliveries are ensured to be completed
                printPackageTime = datetime.timedelta(hours=int(16))
            case "3":
                print("See the status of all packages at a specific time")
                time = input("Enter a military time in the format HH:mm\n")
                # Parse the time that the user entered
                hours, minutes = time.split(":")
                # Update the time that the program will stop its main loop
                printPackageTime = datetime.timedelta(hours=int(hours), minutes=int(minutes))
                # Set default package ID to be 0 so that no individual package information is shown
                package_search_id = 0
                print("Package Information at:", printPackageTime)
            case "4":
                package_search_id = int(input("Enter a package ID: "))
                # Validate that the package exists
                if package_search_id <= 0 or package_search_id > 40:
                    print("Error: Package ID out of range. Please select an ID between 1-40")
                    break
                # Parse the time that the user entered
                time = input("Enter a military time in the format HH:mm\n")
                hours, minutes = time.split(":")
                # Update the time that the program will stop its main loop
                printPackageTime = datetime.timedelta(hours=int(hours), minutes=int(minutes))
                print("Package Information at:", printPackageTime)
            # Case to quit the program
            case "q":
                print("Thank you for using our program. Goodbye!")
                break
            # Validate to see if a valid selection was chosen
            case _:
                input("Invalid selection, press any key to try again.")

        # Run the program unless "q" is given as an option.
        if choice == "1" or choice == "2" or choice == "3" or choice == "4":
            main()
