"""Package structure is as follows -> [id, address, city, zip, deadline, weight, status, location]
location refers to an index in the distance array"""

standard = [
    [2, "2530 S 500 E", "Salt Lake City", "UT", 84106, 0, 44, 2, 9],
    [4, "380 W 2880 S", "Salt Lake City", "UT", 84115, 0, 4, 2, 18],
    [5, "410 S State St", "Salt Lake City", "UT", 84111, 0, 5, 2, 19],
    [7, "1330 2100 S", "Salt Lake City", "UT", 84106, 0, 8, 2, 2],
    [8, "300 State St", "Salt Lake City", "UT", 84103, 0, 9, 2, 12],
    [10, "600 E 900 South", "Salt Lake City", "UT", 84105, 0, 1, 2, 25],
    [11, "2600 Taylorsville Blvd", "Salt Lake City", "UT", 84118, 0, 1, 2, 10],
    [12, "3575 W Valley Central Station bus Loop", "West Valley City", "UT", 84119, 0, 1, 2, 16],
    [17, "3148 S 1100 W", "Salt Lake City", "UT", 84119, 0, 2, 2, 14],
    [19, "177 W Price Ave", "Salt Lake City", "UT", 84115, 0, 37, 2, 4],
    [21, "3595 Main St", "Salt Lake City", "UT", 84115, 0, 3, 2, 17],
    [22, "6351 South 900 East", "Murray", "UT", 84121, 0, 2, 2, 26],
    [24, "5025 State St", "Murray", "UT", 84107, 0, 7, 2, 22],
    [26, "5383 South 900 East #104", "Salt Lake City", "UT", 84117, 0, 25, 2, 24],
    [27, "1060 Dalton Ave S", "Salt Lake City", "UT", 84104, 0, 2, 2, 1],
    [33, "2530 S 500 E", "Salt Lake City", "UT", 84106, 0, 1, 2, 9],
    [35, "1060 Dalton Ave S", "Salt Lake City", "UT", 84104, 0, 88, 2, 1],
    [39, "2010 W 500 S", "Salt Lake City", "UT", 84104, 0, 9, 2, 6]
]

truckSpecific = [
    [3, "233 Canyon Rd", "Salt Lake City", "UT", 84103, 0, 2, 2, 8],
    [18, "1488 4800 S", "Salt Lake City", "UT", 84123, 0, 6, 2, 3],
    [36, "2300 Parkway Blvd", "West Valley City", "UT", 84119, 0, 88, 2, 7],
    [38, "410 S State St", "Salt Lake City", "UT", 84111, 0, 9, 2, 19]
]

priority = [
    [1, "195 W Oakland Ave", "Salt Lake City", "UT", 84115, 1030, 21, 2, 5],
    [23, "5100 South 2700 West", "Salt Lake City", "UT", 84118, 9, 5, 2, 23],
    [29, "1330 2100 S", "Salt Lake City", "UT", 84106, 1030, 2, 2, 2],
    [30, "300 State St", "Salt Lake City", "UT", 84103, 1030, 1, 2, 12],
    [31, "3365 S 900 W", "Salt Lake City", "UT", 84119, 1030, 1, 2, 15],
    [34, "4580 S 2300 E", "Holladay", "UT", 84117, 1030, 2, 2, 21],
    [37, "410 S State St", "Salt Lake City", "UT", 84111, 1030, 2, 2, 19],
    [40, "380 W 2880 S", "Salt Lake City", "UT", 84115, 1030, 45, 2, 18]
]

delayed = [
    [6, "3060 Lester St", "West Valley City", "UT", 84119, 1030, 88, 1, 13],
    [25, "5383 South 900 East # 104", "Salt Lake City", "UT", 84117, 1030, 7, 1, 24],
    [28, "2835 Main St", "Salt Lake City", "UT", 84115, 0, 7, 1, 11],
    [32, "3365 S 900 W", "Salt Lake City", "UT", 84119, 0, 1, 1, 15],
]

incorrectAddresses = [[9, "410 S State St", "Salt Lake City", "UT", 84111, 0, 2, 1, 19]] #basically delayed until 1030

grouped = [
    [13, "2010 W 500 S", "Salt Lake City", "UT", 84104, 1030, 2, 2, 6],
    [14, "4300 S 1300 E", "Millcreek", "UT", 84117, 1030, 88, 2, 20],
    [15, "4580 S 2300 E", "Holladay", "UT", 84117, 900, 4, 2, 21],
    [16, "4580 S 2300 E", "Holladay", "UT", 84117, 1030, 88, 2, 21],
    [20, "3595 Main St", "Salt Lake City", "UT", 84115, 1030, 37, 2, 17]
]



