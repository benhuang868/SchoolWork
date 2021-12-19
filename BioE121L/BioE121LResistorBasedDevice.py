#List of lists to establish design parameters
width20 = [[50, 70],[20, 50], [40, 70]]
width25 = [[60, 75],[25, 50], [50, 75]]
width30 = [[70, 80],[30, 50], [60, 80]]
width35 = [[80, 85],[35, 50], [70, 85]]
width40 = [[90, 90],[40, 50], [80, 90]]
width45 = [[100, 95],[45, 50], [90, 95]]
width50 = [[110, 100],[50, 50], [100, 100]]
dimensions = [width20, width25, width30, width35, width40, width45, width50]

#Calculates resistance using parameters
def rectangularresistance(w, L, h, mu):
    return (12 * mu * L) / (w * (h ** 3))

#Calculates needed length based on input resistance and parameters
def resistorlength(eqres, w, h, mu):
    return (eqres * w * (h ** 3)) / (12 * mu)

#Calculates equivalent resistance of each filter set
def eqresistance(library, height, mu, pillars, n, resistancesum=0):
    def filtereqresistance(r_1, r_2, r_3, pillars):
        def recursiveresist(initialresist, m):
            if m == 0:
                return initialresist
            else:
                return ((r_2 ** -1) + ((r_1 + recursiveresist(initialresist, m-1) + r_3) ** -1)) ** -1
        return recursiveresist(r_2, pillars)
    m = 0
    while m <= n:
        r1data = library[m][0]
        r2data = library[m][1]
        r3data = library[m][2]
        r1 = rectangularresistance(r1data[0], r1data[1], height, mu)
        r2 = rectangularresistance(r2data[0], r2data[1], height, mu)
        r3 = rectangularresistance(r3data[0], r3data[1], height, mu)
        resistresult = filtereqresistance(r1, r2, r3, pillars)
        curve = rectangularresistance(library[m][2][0], 3.14 * (library[m][2][0] * 2 + 50), height, mu)
        resistancesum += (resistresult + curve)
        m += 1
    lastresist = rectangularresistance(library[0][2][0], 3.14 * (library[0][2][0] * 2 + 50), height, mu)
    print("Resistance of", library[n][1][0], "micron filter set:", resistancesum - lastresist)
    return resistancesum - lastresist

#Calculates required restance needed for each filter set outlet
def seteqresistance(set, scaling=0):
    finallist = []
    for i in range(len(set)):
        if i == 0:
            finallist.append(set[0] * (1 + scaling))
        else:
            finallist.append((set[i] + ((2 * (finallist[i - 1] ** -1))) ** -1) * (1 + scaling))
    return finallist

#Operates functions and calculates lengths required for each filter set
resistateachset = []
for i in range(len(dimensions)):
    resistateachset.append(eqresistance(dimensions, 30, 1, 71, i))

scaling = 1
resistateachstage = seteqresistance(resistateachset, scaling)
    
totallength = []
for i in range(len(resistateachstage)):
    length = resistorlength(resistateachstage[i], dimensions[i][1][0] + 5, 30, 1)
    totallength.append(length)
    print("Outlet resistor length at", dimensions[i][1][0], "micron filter set should be approximately", length, "microns with", scaling * 100, "% scaling.")
