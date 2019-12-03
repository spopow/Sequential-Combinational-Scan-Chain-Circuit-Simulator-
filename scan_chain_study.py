import csv
import scan_chain
import random
import math


def scan_chain_study():
    from genFaultList import getFaultListStudy

    faultsFoundPartial = 0
    faultsFoundFull = 0
    faultsFoundParallel = 0

    cycleFaultFoundPartial = []
    cycleFaultFoundFull = []
    cycleFaultFoundParallel = []

    scanTypeList = ['partial', 'full', 'parallel']

    testApplyCycles = 20

    print("Scan Chain Study\n")
    print("----------------------------------------------------\n")

    # Ask user to input circuit benchmark
    circuit_bench = input("Input a circuit benchmark: ")

    # Take file name and generate fault list for bench file
    fullFaultList = getFaultListStudy(circuit_bench)

    while True:
        print(
            "\nPlease input an integer value for the number of cycles you want to simulate (default = 20): ")
        cycleInput = input()
        if cycleInput == "":
            print("\nWill simulate for" + str(testApplyCycles) + "test apply cycles = \n")
            break
        elif not cycleInput.isdigit():
            print("\nYour input value is not an integer or it's less than 0")
        elif int(cycleInput) <= 0:
            print("\nYour input value should be greater than 0")
        else:
            print("\nYour input is: ", cycleInput)
            testApplyCycles = int(cycleInput)
            break

    for fault in fullFaultList:

        # Run fault coverage for partial, full, and parallel
        flipFlopTVs, inputTVs = LFSRtestGen(circuit_bench, testApplyCycles)

        for scanType in scanTypeList:
            if scanType == 'partial':
                faultsFoundPartial, cycleFaultFoundPartial = scan_output_file(circuit_bench, testApplyCycles, fault,
                                                                              scanType, inputTVs, flipFlopTVs,
                                                                              faultsFoundPartial,
                                                                              cycleFaultFoundPartial)

            if scanType == 'full':
                faultsFoundFull, cycleFaultFoundFull = scan_output_file(circuit_bench, testApplyCycles, fault, scanType,
                                                                        inputTVs, flipFlopTVs, faultsFoundFull,
                                                                        cycleFaultFoundFull)

            if scanType == 'parallel':
                faultsFoundParallel, cycleFaultFoundParallel = scan_output_file(circuit_bench, testApplyCycles, fault,
                                                                                scanType, inputTVs, flipFlopTVs,
                                                                                faultsFoundParallel,
                                                                                cycleFaultFoundParallel)

    percentFoundPartial = getPercentageFaultsFound(faultsFoundPartial, len(fullFaultList))
    percentFoundFull = getPercentageFaultsFound(faultsFoundFull, len(fullFaultList))
    percentFoundParallel = getPercentageFaultsFound(faultsFoundParallel, len(fullFaultList))

    avgCyclePartial = getAverageCycles(cycleFaultFoundPartial)
    avgCycleFull = getAverageCycles(cycleFaultFoundFull)
    avgCycleParallel = getAverageCycles(cycleFaultFoundParallel)

    avgCyclePartial = round(avgCyclePartial, 2)
    avgCycleFull = round(avgCycleFull, 2)
    avgCycleParallel = round(avgCycleParallel, 2)

    printCSV(circuit_bench, percentFoundPartial, percentFoundFull, percentFoundParallel, avgCyclePartial, avgCycleFull,
             avgCycleParallel)


def scan_output_file(bench_file, testApplyCycles, fault, scanType, inputTVs, flipFlopTVs, faultsFound, cycleFaultFound):
    from p3sim import netRead

    # Create dictionary of circuit via benchmark file
    circuit = netRead(bench_file)

    # Run circuit simulation to generate the results of the good circuit
    goodScanData = getBasicSim(circuit, testApplyCycles, 0, scanType, False, fault, flipFlopTVs, inputTVs)

    # Run circuit simulation to generate the results of the faulty circuit
    faultScanData = getBasicSim(circuit, testApplyCycles, 0, scanType, True, fault, flipFlopTVs, inputTVs)

    # Detect the cycles at which faults are detected
    faultAnalysis = scanFaultDetector(goodScanData, faultScanData, faultsFound, cycleFaultFound, scanType)

    return faultAnalysis


def scanFaultDetector(goodScanData, faultScanData, faultsFound, cycleFaultFound, scanType):
    dataPO = outputComparator(faultScanData["PrimaryOutputs"], goodScanData["PrimaryOutputs"])
    dataDFF = outputComparator(faultScanData["DFF"], goodScanData["DFF"])

    compOut = ''
    scanOutCycles = getScanOutCycles(goodScanData["circuit"], scanType)

    # number of cycles it takes to find given fault given on the index of primary outputs it took to detect
    # PO_cycles = goodScanData["totalCycles"] + dataPO[1]  (number test applies)
    PO_cycles = scanOutCycles * dataPO[1] + dataPO[1]

    # number of cycles it takes to find given fault given on the index of scan out it took to detect
    # DFF_cycles = goodScanData["totalCycles"] + dataDFF[1] + scanOutCycles
    DFF_cycles = scanOutCycles * dataDFF[1] + dataDFF[1] + scanOutCycles


    if dataPO[0] and PO_cycles < DFF_cycles:
        faultsFound = faultsFound + 1
        cycleFaultFound.append(PO_cycles)

    elif dataDFF[0] and DFF_cycles < PO_cycles:
        faultsFound = faultsFound + 1
        cycleFaultFound.append(DFF_cycles)

    else:
        print("Fault not detected...")

    return faultsFound, cycleFaultFound


def inputSizeFinder(circuit):
    f = open(circuit, 'r')
    inputCtr = 0
    for line in f:

        if line == '\n':
            continue
        if line[0] == '#':
            continue
        if line[0:6] == "OUTPUT":
            continue
        if line[0:5] == "INPUT":
            inputCtr += 1
            continue

    return inputCtr


# Pass in circuit benchmark
def LFSRtestGen(circuit, testApplyCycles):
    lineOfPI = []
    listDFF = []
    outVect = ''
    # vector Size is the num PI and the num DFF

    vectPI = inputSizeFinder(circuit)
    vectDFF = _DFFnumFinder(circuit)

    # for how many test cycles, we create that many randomly generated test vectors

    for x in range(testApplyCycles):
        # listPI needs to return a list of strings
        outVect = random.randint(0, 2 ** (vectPI - 1))
        outVect = format(outVect, '0' + str(vectPI) + 'b')
        lineOfPI.append(outVect)
        # listDFF needs to return list of lists of single bit strings
        outVect = random.randint(0, 2 ** (vectDFF - 1))
        outVect = format(outVect, '0' + str(vectDFF) + 'b')
        listDFF.append(list(outVect))

    # returning a tuple
    return listDFF, lineOfPI


def _DFFnumFinder(circuit):
    f = open(circuit, 'r')
    DFFctr = 0
    for line in f:
        if line.find("DFF") > 0:
            DFFctr += 1
            continue

    return DFFctr


def getNumFF(bench_file):
    benchFile = open(bench_file, "r")
    # get line: "# 3 D-type flipflops "
    for line in benchFile:
        if "D-type flipflops" in line:
            num_ff_here = line.split(" ")
    return num_ff_here[1]


def getNumPrimaryOutputs(bench_file):
    numOutputs = 0
    # print("getting Num primary inputs\n")
    # print("reading bench file\n")
    benchFile = open(bench_file, "r")
    # get line: "1 outputs"
    for line in benchFile:
        if "OUTPUT" in line:
            numOutputs = numOutputs + 1
    return numOutputs


# requires the circuit as an object
def getBasicSim(circuit, testApplyCycles, totalCycles, scanType, Fault_bool, fault, scanInTV, PrimaryInputs):
    from p3sim import basic_sim, inputRead
    from circuit_sim_result import getFaultCircuit

    scanData = {
        "circuit": {},  # circuit dictionary
        "DFF": [],  # list of DFF outputs
        "PrimaryOutputs": [],  # primary output values
        "totalCycles": totalCycles,  # number of total cycles
        "scanInTV": scanInTV,  # scan in test vector
        "PrimaryInputs": PrimaryInputs  # Primary Input test vector
    }

    cycle = 0

    while cycle < testApplyCycles:

        # Update Scan with desired test vector in DFF (i.e SCAN IN)
        circuit, totalCycles = scan_chain.scanChain(circuit, scanType, scanData["scanInTV"][cycle], totalCycles)

        # Update Input Values 
        circuit = inputRead(circuit, scanData["PrimaryInputs"][cycle])

        # Set the Fault line to True 
        if Fault_bool:
            circuit = getFaultCircuit(circuit, fault)

        # Simulates circuit provided faults or 8not (i.e. TEST APPLY)
        circuit = basic_sim(circuit, Fault_bool, fault)

        # collect list of scan out data to dictionary
        scanData["DFF"].append(storeScanOut(circuit, scanData["DFF"]))

        # collect list of test apply data to dictionary
        scanData["PrimaryOutputs"].append(storePrimaryOutputs(circuit, scanData["PrimaryOutputs"]))

        # Add test apply cycle
        # totalCycles += 1

        # function to reset all False to true for each gate that is not a DFF
        circuit = reset_Gate_T_F(circuit)

        cycle = cycle + 1
        # print("Running Cycle: " + str(cycle) + "\n")

    # scanOutCycles = getScanOutCycles(circuit, scanType)
    # totalCycles = totalCycles + scanOutCycles - 1

    # update circuit in the dictionary
    scanData["circuit"] = circuit
    scanData["totalCycles"] = totalCycles

    return scanData


# FUNCTION: storeScanOut
# Outputs: appends scan out values into a list, that would be used later for comparison
# Inputs: circuit dictionary
def storeScanOut(circuit, someList):
    scanOutputs = []
    for gate in circuit:
        if circuit[gate][0] == "DFF":
            scanOutputs.append(circuit[gate][3])
    return scanOutputs


# FUNCTION: storePrimaryOutputs
# Outputs: appends PO into a list, that would be used later for comparison
# Inputs: circuit dictionary
def storePrimaryOutputs(circuit, someList):
    outputs = []
    outputList = circuit["OUTPUTS"][1]
    for output in outputList:
        outputs.append(circuit[output][3])
    return outputs


# FUNCTION: outputComparator
# Boolean Function Outputs:
# True: Difference found between circuits so fault found
# False: No difference found
# Inputs: Good & Bad lists, whether it's sequential or scan chain study
def outputComparator(badList, goodList):
    # error check to make sure lists are the same length
    if len(badList) != len(goodList):
        print("The list sizes are different! Cannot compare for fault detection")
        return -1
    # goes through each index of the lists and compares
    listLength = len(badList)
    PO_Length = len(badList[0])

    for index in range(listLength):
        for vctrIndex in range(PO_Length):
            if badList[index][vctrIndex] != goodList[index][vctrIndex] and (
                    badList[index][vctrIndex] != 'U' or goodList[index][vctrIndex] != 'U'):
                index = index + 1
                # Debugger
                # print("Lists are not the same! Fault has been detected! ", badList[index-1], 
                # " of the bad list != ", goodList[index-1], " of the good list at cycle ", index )
                return True, index

    return False, index + 1


# FUNCTION: printPOValues
# Inputs: circuit = circuit dictionary; simulatorTxt = name of output file
# Outputs: writes to simulatorTxt the line output name and its value

def reset_Gate_T_F(circuit):
    # print("stuck at resetting gates\n")
    from p3sim import printCkt
    for curr in circuit:
        # print("Curr is:" + str(circuit[curr]))
        currLen = len(circuit[curr])
        if currLen == 4 and circuit[curr][0] != 'DFF' and circuit[curr][0] != 'INPUT':
            circuit[curr][2] = False
            # print("Curr is now: " + str(circuit[curr]) + "\n")
    return circuit


def getScanOutCycles(circuit, scanType):
    # Number of scan out cycles
    scanOut = 0

    if scanType == 'partial' or 'parallel':

        # Counter to keep track of the number of DFFs
        dffCounter = 0

        # For each gate in the circuit, find the ones that DFFs
        for gate in circuit:
            if circuit[gate][0] == 'DFF':
                dffCounter = dffCounter + 1

        scanOut = math.ceil(dffCounter / 2)

    if scanType == 'full':

        # For each gate in the circuit, find the ones that DFFs
        for gate in circuit:
            if circuit[gate][0] == 'DFF':
                scanOut = scanOut + 1

    return scanOut


def getAverageCycles(cycleFaultFound):
    return sum(cycleFaultFound) / len(cycleFaultFound)


def getPercentageFaultsFound(faultsFound, totalFaults):
    return round((faultsFound / totalFaults) * 100, 2)


def printCSV(benchName, percentFoundPartial, percentFoundFull, percentFoundParallel, avgCyclePartial, avgCycleFull,
             avgCycleParallel):
    firstLine = ['', '% of Faults Found', 'Average Cycles']
    partialLine = ['Partial', str(percentFoundPartial), str(avgCyclePartial)]
    fullLine = ['Full', str(percentFoundFull), str(avgCycleFull)]
    parallelLine = ['Parallel', str(percentFoundParallel), str(avgCycleParallel)]

    with open("scan_chain_study_420_1.csv", 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(firstLine)
        writer.writerow(partialLine)
        writer.writerow(fullLine)
        writer.writerow(parallelLine)


# If this module is executed alone
if __name__ == "__main__":
    # let's read the name of bench file
    scan_chain_study()
