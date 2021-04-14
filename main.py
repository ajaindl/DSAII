import sys
import enum
import distances
import packages

#global truck dictionary
truckList = {}

"""Hash map for storing packages"""
class PackageHashMap:
    def __init__(self):
        """Given the scale of WGUPS shipping, 1000 is a reasonable backing array size"""
        self.size = 1000
        self.mapArray = [None] * self.size

    """gets a hash by hashing the key mod size of hash map array to bring value in range of array indexes"""
    def getHash(self, key):
       return hash(key) % self.size

    """add values to the hashmap:
        Hash the key, then checking if if that hash exists in the map array
        Create a key value tuple with key being a package property and value being the package object.
        Check if hashed key exists in hashmap
            If it does not, wrap tuple in list and add to array at hash key index
        If it does, iterate through tuples in list at array index until a tuple key matches the key to insert
            Append tuple to list at hash key index
        Time: O(1)
    """
    def addPackage(self, key, value):
        keyHash = self.getHash(key)
        valueTuple = [key, value]

        if self.mapArray[keyHash] is None:
            self.mapArray[keyHash] = list([valueTuple])
        else:
            for tuple in self.mapArray[keyHash]:
                if tuple[0] == key:
                    tuple[1] == value
            self.mapArray[keyHash].append(valueTuple)

    """gets values from hashmap by grabbing tuple list at hashed key array index and then matching input key to 
    tuple key. Time: O(1)"""
    def getPackage(self, key):
        keyHash = self.getHash(key)
        if self.mapArray[keyHash] is None:
            return None
        else:
            for tuple in self.mapArray[keyHash]:
                if tuple[0] == key:
                    return tuple[1]

    def getAllPackages(self, key):
        keyHash = self.getHash(key)
        if self.mapArray[keyHash] is None:
            return None
        else:
            return self.mapArray[keyHash]

#global package hash table
packageHashTable = PackageHashMap()


class Truck:
    def __init__(self, truckId):
        self.id = truckId
        self.active = False
        self.location = 0
        self.capacity = 16
        self.milesDriven = 0
        self.route = []
        self.routeDistances = []
        self.routeTimes = []
        self.packages = []
        self.timeDriven = 0
        self.timeSinceLastDelivery = 0
        self.timeToHub = 0
        truckList[truckId] = self

    """add a package to the truck and reduce capacity by 1"""
    def addPackage(self, package):
        self.packages.append(package)
        self.capacity -=1


    """deliver the package. reset current drive time, and update the route and route times list. Time: O(n)"""
    def deliverPackage(self, location):
        for package in self.packages:
            if(package.location == location):
                self.packages.remove(package)
                self.location = location
                packageToUpdate = packageHashTable.getPackage(package.id)
                packageToUpdate.status = PackageStatus.Delivered
                packageHashTable.addPackage(packageToUpdate.id, packageToUpdate)
                self.timeDriven += self.timeSinceLastDelivery
                self.timeSinceLastDelivery = 0
                self.route.pop(0)
                self.milesDriven += self.routeDistances.pop(0)
                self.timeDriven += self.routeTimes.pop(0)

    """gets the route using nearest neighbor algorithm. Is constrained to that method's runtime. 
        get all locations
        get current location
        while a location has not been added to the route:
            get the nearest neighbor by getting all distances to current node and returning the smallest
            add nearest neighbor location to the route
            set current location to the location of the nearest neighbor
            remove previous location
        Time: O(n^2) """
    def getRoute(self):
        locationsLeft = [package.location for package in self.packages]
        currentLocation = self.location
        route = []
        while len(locationsLeft) > 0:
            nearestLocation = getNearestNeighbor(currentLocation,locationsLeft)
            route.append(nearestLocation)
            locationsLeft.remove(nearestLocation)
            currentLocation = nearestLocation
        self.route = route
        self.routeDistances = self.getRouteDistances(self.location, self.route)
        self.routeTimes = self.getRouteTimes()
        self.timeToHub = getDistanceBetween(0, route[-1])
        self.active = True
        self.setPackageStates()

    """sets all packages on truck to In_Route status. Time: O(n)"""
    def setPackageStates(self):
        for package in self.packages:
            packageHashTable.getPackage(package.id).status = PackageStatus.In_Route


    """get the distance of each node to node route and add them to an array. Time: O(n)"""
    def getRouteDistances(self, location, routes):
        distances = []
        if len(routes) < 1:
            return distances
        distances.append(getDistanceBetween(self.location, routes[0]))
        for i, loc1 in enumerate(routes[:-1]):
            distances.append(getDistanceBetween(loc1, routes[i + 1]))
        return distances

    """returns a list of route times that matches up the the list of route distances. Calculated under the assumption
    that each truck averages 18 mph. Map function iterates over every item in the list and excecutes a method on it,
     so - Time: O(n)"""
    def getRouteTimes(self):
        return list(map(lambda distance: distance * (60/18), self.routeDistances))

    """checks if truck is ready for a delivery by comparing running time in minutes to next package delivery time. 
    Runtime is tied to the deliverPackage() method, so - Time: O(n)"""
    def checkForDelivery(self):
        if len(self.packages) > 0 and len(self.routeTimes)>0:
            self.timeSinceLastDelivery +=1
            if self.timeSinceLastDelivery >= self.routeTimes[0]:
                self.deliverPackage(self.route[0])
        else:
            self.active = False

"""enum for package status"""
class PackageStatus(enum.Enum):
    Delayed = 1
    In_Hub = 2
    In_Route = 3
    Delivered = 4

"""enum for package status"""
class SearchType(enum.Enum):
    weight = 1
    id = 2
    other = 3

class Package:
    def __init__(self, id, address, city, state, zip, deliveryTime, weight, status, location):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryTime = deliveryTime
        self.weight = weight
        self.status = PackageStatus(status).name
        self.location = location

        self.addPackageToHashTable(id, address, city, zip, deliveryTime, weight, status, location)

    """ creates the a hash table using a global dictionary to map property hashes as keys to package(s) as values. Each package id
     will map to it's corresponding package object. Other package properties will be mapped as property string value as
      key -> packages containing that property string as the value"""
    def addPackageToHashTable(self, id, address, city, zip, deliveryTime, weight, status, location):
        #id will be unique, so no need to check if exists
        packageHashTable.addPackage(id, self)
        packageHashTable.addPackage(address, self)
        packageHashTable.addPackage(city, self)
        packageHashTable.addPackage(str(zip), self)
        packageHashTable.addPackage(str(deliveryTime), self)
        packageHashTable.addPackage("weight" + str(weight), self) ##
        packageHashTable.addPackage(PackageStatus(status).name, self)

    def print(self):
        print(f"Package #: {self.id}, Address: {self.address}, City: {self.city}, Zip: {self.zip}, Weight: {self.weight}, Status: {self.status}")



"""Creates a clock that increments in minutes, and returns a string of HH:mm"""
class Clock:
    def __init__(self):
        self.start = 800
        self.hoursAdded = 0
        self.minutesAdded = 0
    def increment(self, increment):
        self.minutesAdded += increment
        if self.minutesAdded >= 60:
            self.hoursAdded += round(self.minutesAdded/60) * 100
            self.minutesAdded = self.minutesAdded % 60
        self.current = self.start + self.hoursAdded + self.minutesAdded

    def __str__(self):
        current = self.current.__str__()
        if(current.__len__() %2 == 1):
            return f"{current[:1]}:{current[1:]}"
        else:
            return f"{current[:2]}:{current[2:]}"


# helper methods

""" generate packages from package arrays, populates global package table. Time: O(n)"""
def importPackages():
    for package in packages.priority + packages.standard + packages.grouped + packages.truckSpecific + packages.incorrectAddresses + packages.delayed :
            Package(package[0], package[1], package[2], package[3], package[4], package[5], package[6], package[7], package[8])

#generate truck dictionary
def initializeTrucks():
    for i in range(1,4):
        Truck(i)


"""gets the nearest neighbor to current location. Time: O(n)"""
def getNearestNeighbor(location, neighbors):
    # set closest to distance between current location and last neighbor, then iterate over remaining neighbors
    nearestNode = neighbors[len(neighbors)-1]
    nearestNodeDist = getDistanceBetween(location, nearestNode)
    for index, node in enumerate(neighbors[:-1]):
        distance = getDistanceBetween(location, node)
        if(distance < nearestNodeDist):
            nearestNode = node
            nearestNodeDist = distance
    return nearestNode

"""gets the distance between two locations. Time: O(1)"""
def getDistanceBetween(locationA, locationB):
    return distances.distances[min(locationA, locationB)][max(locationA, locationB) - min(locationA, locationB)]

"""gets distance of a route. Time: O(n)"""
def calculateRouteDistance(route):
    distances = [getDistanceBetween(loc, route[i+1]) for i, loc in enumerate(route[:-1])]
    return sum(distances)
"""
Load the trucks with packages. Truck 1 will contain priority and grouped packages. Truck 2 will contain truck specific. 
Truck 3 will contain incorrect address. Standard delivery packages will be split between all three trucks, 
prioritizing truck 1, then 2, then 3 
Time: O(n)
"""
def loadTrucks():
    priority = [1,23,29,30,31,34,37,40]
    truckSpecific = [3,18,36,38]
    delayed = [6,25,28,32]
    incorrectAddress = [9]
    grouped = [13,14,15,16,20]
    standard = [2,4,5,7,8,10,11,12,17,19,21,22,24,26,27,33,35,39]
    # add priority packages to truck 1
    for id in priority:
        truckList[1].addPackage(packageHashTable.getPackage(id))
    for id in grouped:
        truckList[1].addPackage(packageHashTable.getPackage(id))
    for id in truckSpecific:
        truckList[2].addPackage(packageHashTable.getPackage(id))
    for id in delayed:
        truckList[3].addPackage(packageHashTable.getPackage(id))
    for id in incorrectAddress:
        truckList[3].addPackage(packageHashTable.getPackage(id))

    #fill trucks with standard packages, filling non delayed trucks first
    for id in standard:
        if truckList[1].capacity>0:
            truckList[1].addPackage(packageHashTable.getPackage(id))
        elif truckList[2].capacity>0:
            truckList[2].addPackage(packageHashTable.getPackage(id))
        else:
            truckList[3].addPackage(packageHashTable.getPackage(id))

"""lookup function. Searches package hash table by search term and returns list. Time: O(1)"""
def lookupPackage(term, type):
    packages = []
    if type == SearchType.weight:
        packages =  packageHashTable.getAllPackages("weight" + str(term)) # add weight string for hashing
    elif type == SearchType.id:
        packages =  packageHashTable.getAllPackages(int(term))
    else:
        packages = packageHashTable.getAllPackages(str(term))

    if packages is None or len(packages) == 0:
        print("No package(s) found")
    else:
        for package in packages:
            package[1].print()


"""Prints status info for all packages. Time: O(1)"""
def printAllPackageStatus():
    for id in range(1,41):
        package = packageHashTable.getPackage(id)
        package.print()

"""checks to see if a truck has no packages and can return to hub. Time: O(1)"""
def getAvailableTruck():
    if not truckList[1].active and not truckList[2].active:
        if truckList[1].timeToHub < truckList[2].timeToHub:
            return 1
        else:
            return 2
    elif not truckList[1].active:
        return 1
    elif not truckList[2].active:
        return 2
    else:
        return -1

def main():
    initializeTrucks()
    importPackages()
    loadTrucks()
    clock = Clock()

    #trucks 1 and 2 begin routes
    truckList[1].getRoute()
    truckList[2].getRoute()
    minutes = 420  #8 hour day
    while(minutes > 0):
        clock.increment(1)
        minutes -= 1

        #delayed packages will be delivered when the package 9 delivery address is corrected
        if(clock.hoursAdded>=200 and clock.minutesAdded>= 5):
            availableTruck = getAvailableTruck()
            if( availableTruck != -1 and not truckList[3].active):
                try:
                    truckList[3].getRoute()
                    #add time to first route as time for returning truck to get to hub
                    truckList[3].routeTimes[0] += truckList[availableTruck].timeToHub
                    print(f"Truck 3 leaving hub at {clock.__str__()}")
                except:
                    pass

        if(clock.__str__() == "9:05"):
            print("State of all packages at 9:05")
            printAllPackageStatus()
        if(clock.__str__() == "10:20"):
            print("State of all packages at at 10:20")
            printAllPackageStatus()
        if(clock.__str__() == "12:05"):
            print("State of all packages Delivered at 12:05")
            printAllPackageStatus()

        truckList[1].checkForDelivery()
        truckList[2].checkForDelivery()
        truckList[3].checkForDelivery()

    print(f"End of day packages status: ")
    printAllPackageStatus()
    print(f"Current time: {clock.__str__()}")
    print(f"Total Miles Drive: {truckList[1].milesDriven + truckList[1].milesDriven + truckList[1].milesDriven}")
    print(f"Total Minutes Driven: {truckList[1].timeDriven + truckList[1].timeDriven + truckList[1].timeDriven}")

    while True:
        searchTerm = input("To search for a package, first input what type of term you want to search by - available terms are id, weight, or other:")
        if searchTerm == "id":
            term = input()
            lookupPackage(term, SearchType.id)
        elif searchTerm == "weight":
            term = input()
            lookupPackage(term, SearchType.weight)
        elif searchTerm == "other":
            term = input()
            lookupPackage(term, SearchType.other)
        else:
            print("Please input a valid search type")




if __name__ == "__main__":
    main()
