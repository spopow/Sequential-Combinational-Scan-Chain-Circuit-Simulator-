import copy
import scan_chain
import p2sim
import random
import math


# input t,n,f
# t = test vector, n = cycles ran,f = fault
# output : content of all ff's, primary outputs for good circuit and a fault


def scan_output_file(bench_file, testApplyCycles, fault, scanType):
    from p2sim import netRead, printCkt

    goodScanData = {}
    faultScanData = {}


    scanInTV, PrimaryInputs = LFSRtestGen(bench_file, testApplyCycles)

    # Text file that will hold all the results
    simulatorTxt = open("Scan Output.txt", "w+")

    # Create dictionary of circuit via benchmark file
    circuit = netRead(bench_file)

    # Run circuit simulation to generate the results of the good circuit
    goodScanData = getBasicSim(circuit, testApplyCycles, 0, scanType, bench_file, False, fault, scanInTV, PrimaryInputs)

    
    # Print the final results of the golden circuit
    #printCkt(good_circuit)

    # Write into the text file that will hold all the results
    simulatorTxt.write("******************GOOD CIRCUIT SIM********************\n")
    
    simulatorTxt.write("Flip Flop & Primary Outputs @ n = " + str(goodScanData["totalCycles"]) + "\n")
    
    # Get the number of flip flops in the circuit
    numFlipFlops = getNumFF(bench_file)

    simulatorTxt.write("D-Type Flip Flops: " + numFlipFlops + "\n")
    printFFvalues(goodScanData["circuit"], simulatorTxt)

    # Get number of primary outputs and print them to file
    numPrimOutputs = getNumPrimaryOutputs(bench_file)

    simulatorTxt.write("\nPrimary Outputs: " + str(numPrimOutputs) + "\n")

    printPOValues(goodScanData["circuit"], simulatorTxt)

    faultScanData = getBasicSim(circuit, testApplyCycles, 0, scanType, bench_file, True, fault, scanInTV, PrimaryInputs)
    # badCircuit = getFaultCvgSeq(circuit, fault, num_cycles)  # make circuit with fault and update values - JAS TD
    simulatorTxt.write("\n******************BAD CIRCUIT SIM********************\n")
    simulatorTxt.write("Fault: " + str(fault) + "\n")
    simulatorTxt.write("Flip Flop & Primary Outputs @ n = " + str(faultScanData["totalCycles"]) + "\n")
    simulatorTxt.write("*****************************************************\n")
    simulatorTxt.write("D-Type Flip Flops: " + numFlipFlops + "\n")
    # call function that prints ff/value
    printFFvalues(faultScanData["circuit"], simulatorTxt)
    simulatorTxt.write("\nPrimary Outputs: " + str(numPrimOutputs) + "\n")
    printPOValues(faultScanData["circuit"], simulatorTxt)

    simulatorTxt.write("\n******************FAULT DETECTION********************\n")
    scanFaultDetector(goodScanData, faultScanData, fault, simulatorTxt)
    
    # if (outputComparator(faultScanData["PrimaryOutputs"], goodScanData["PrimaryOutputs"])[0]):
    #     compOut = "\n" + fault + " has been detected at cycle " + str(outputComparator(badList, goodList)[1]) + " with test vector " + user_tv_str + "\n"
    #     simulatorTxt.write(compOut)
    # else:
    #     compOut = "\n" + fault + " has NOT been detected with test vector " + user_tv_str + "\n"
    #     simulatorTxt.write(compOut)

    simulatorTxt.close()


# Wrapper function to output the cycle number the fault was found

def scanFaultDetector(goodScanData, faultScanData, fault, simulatorTxt):
    dataPO = outputComparator(faultScanData["PrimaryOutputs"], goodScanData["PrimaryOutputs"])
    dataDFF = outputComparator(faultScanData["DFF"], goodScanData["DFF"])
    compOut = ''
    # number of cycles it takes to find given fault given on the index of primary outputs it took to detect
    # number of DFFs * test apply cycles + test apply cycles
    PO_cycles = len(goodScanData["DFF"][0]) * dataPO[1] + dataPO[1] 

    # number of cycles it takes to find given fault given on the index of scan out it took to detect
    # (i.e. number of DFFs * test apply cycle found + test apply cycles + number of DFFs to scan out)
    DFF_cycles = len(goodScanData["DFF"][0]) * dataDFF[1] + dataDFF[1] + len(goodScanData["DFF"][0])

    
    if dataPO[0] and PO_cycles < DFF_cycles:
        compOut = "\n" + fault + " has been detected at cycle " + str(PO_cycles) + " and at Test Apply Cycle: "+ str(dataPO[1])
        simulatorTxt.write(compOut)
    elif dataDFF[0] and DFF_cycles < PO_cycles:
        compOut = "\n" + fault + " has been detected at cycle " + str(DFF_cycles)  + " and at Test Apply Cycle: "+ str(dataDFF[1])
        simulatorTxt.write(compOut)
    else:
        compOut = "\n" + fault + " has NOT been detected \n"
        simulatorTxt.write(compOut)





def inputSizeFinder(circuit):

    f = open(circuit,'r')
    inputCtr = 0
    for line in f:

        if (line == '\n'):
            continue
        if(line[0] == '#'):
            continue
        if line[0:6] == "OUTPUT":
            continue
        if (line[0:5] == "INPUT"):
            inputCtr += 1
            continue

    return inputCtr


# Pass in circuit benchmark
def LFSRtestGen(circuit, testApplyCycles):
    lineOfPI = []
    listDFF = []
    outVect = ''
    #vector Size is the num PI and the num DFF
    
    vectPI = inputSizeFinder(circuit)
    vectDFF = _DFFnumFinder(circuit)

    #for how many test cycles, we create that many randomly generated test vectors
    
      
    for x in range(testApplyCycles):

        #listPI needs to return a list of strings
        outVect = random.randint(0, 2**(vectPI - 1))
        outVect = format(outVect, '0'+str(vectPI)+'b')
        lineOfPI.append(outVect)
        #listDFF needs to return list of lists of single bit strings
        outVect = random.randint(0, 2**(vectDFF - 1))
        outVect = format(outVect, '0'+str(vectDFF)+'b')
        listDFF.append(list(outVect))

    #returning a tuple
    return listDFF, lineOfPI

def _DFFnumFinder(circuit):

    f = open(circuit,'r')
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


#requires the circuit as an object
def getBasicSim(circuit, testApplyCycles, totalCycles, scanType, circuitBench, Fault_bool, fault, scanInTV, PrimaryInputs):
    from p2sim import basic_sim, inputRead
    from circuit_sim_result import getFaultCircuit

    scanData = {
        "circuit": {},                          #circuit dictionary
        "DFF": [],                              #list of DFF outputs
        "PrimaryOutputs":  [],                  #primary output values
        "totalCycles": totalCycles,             #number of total cycles
        "scanInTV": scanInTV,                   #scan in test vector
        "PrimaryInputs": PrimaryInputs         #Primary Input test vector   
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

        totalCycles += 1

        # function to reset all False to true for each gate that is not a DFF
        circuit = reset_Gate_T_F(circuit)  
       
        cycle = cycle + 1
        print("Running Cycle: " + str(cycle) + "\n")

    scanOutCycles = getScanOutCycles(circuit, scanType)
    totalCycles = totalCycles + scanOutCycles - 1

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
    # False: No Diffference Found
# Inputs: Good & Bad lists, wether it's sequential or scan chain study
# FIXME CHECK IF WORKS FOR OTHER SIMULATORS
def outputComparator(badList, goodList):
    
    # error check to make sure lists are the same length
    if (len(badList) != len(goodList)):
        print("The list sizes are different! Cannot compare for fault detection")
        return -1
    # goes through each index of the lists and compares
    listLength = len(badList)
    PO_Length = len(badList[0])

    for index in range(listLength):
        for vctrIndex in range(PO_Length):
            if badList[index][vctrIndex] != goodList[index][vctrIndex] and (badList[index][vctrIndex] != 'U' or goodList[index][vctrIndex] != 'U'):
                index = index + 1
                # Debugger
                # print("Lists are not the same! Fault has been detected! ", badList[index-1], 
                # " of the bad list != ", goodList[index-1], " of the good list at cycle ", index )
                return True, index

    return False, index+1

            


# circuit here is dictionary
def printFFvalues(circuit, file):
    flipFlopNum = 0
    file.write('**********************DFF VALUES**********************')
    for gate in circuit:
        if circuit[gate][0] == 'DFF':
            dFlipFlop = '\n DFF_' + str(flipFlopNum) + ": " + str(circuit[gate][3]) + " "
            flipFlopNum = flipFlopNum + 1
            file.write(dFlipFlop)
    file.write('\n******************************************************')

# FUNCTION: printPOValues
# Inputs: circuit = circuit dictionary; simulatorTxt = name of output file
# Outputs: writes to simulatorTxt the line output name and its value

def printPOValues(circuit, simulatorTxt):

    outputList = circuit["OUTPUTS"][1]
    simulatorTxt.write('*****************Primary Output Values*****************')
    for output in outputList:
        PrimaryOutputs = "\n" + output + ":" + circuit[output][3]
        simulatorTxt.write(PrimaryOutputs)


def getFaultCvgSeq(circuit, fault, total_cycles, fileIndex=None, faults=None):
    from p2sim import basic_sim, inputRead
    print("inside getFaultCvgSeq\n")
    # keep an initial (unassigned any value) copy of the circuit for an easy reset
    newCircuit = circuit
    # incorporate fault
    cycle = 0
    while cycle < total_cycles:
        # line 566-666 down make TV a line
        line = fault
        output = ""

        # Do nothing else if empty lines, ...
        if (line == "\n"):
            continue
        # ... or any comments
        if (line[0] == "#"):
            continue

        # Removing the the newlines at the end
        line = line.replace("\n", "")

        # Removing spaces
        line = line.replace(" ", "")

        circuit = inputRead(circuit, line)

        if circuit == -1:
            print("INPUT ERROR: INSUFFICIENT BITS")
            # After each input line is finished, reset the netList
            circuit = newCircuit
            print("...move on to next input\n")
            continue
        elif circuit == -2:
            print("INPUT ERROR: INVALID INPUT VALUE/S")
            # After each input line is finished, reset the netList
            circuit = newCircuit
            print("...move on to next input\n")
            continue

        circuit = basic_sim(circuit)

        for y in circuit["OUTPUTS"][1]:
            if not circuit[y][2]:
                output = "NETLIST ERROR: OUTPUT LINE \"" + y + "\" NOT ACCESSED"
                break
            output = str(circuit[y][3]) + output

        for faultLine in faults:
            # skips fault if already detected
            if faultLine[fileIndex] == True:
                continue

            # creates a copy of the circuit to be used for fault testing
            faultCircuit = copy.deepcopy(circuit)

            for key in faultCircuit:
                if key[0:5] == "wire_":
                    faultCircuit[key][2] = False
                    faultCircuit[key][3] = 'U'

            # sets up the inputs for the fault circuit
            faultCircuit = inputRead(faultCircuit, line)

            # handles stuck at faults
            if faultLine[5][1] == "SA":
                for key in faultCircuit:
                    if faultLine[5][0] == key[5:]:
                        faultCircuit[key][2] = True
                        faultCircuit[key][3] = faultLine[5][2]

            # handles in in stuck at faults by making a new "wire"
            elif faultLine[5][1] == "IN":
                faultCircuit["faultWire"] = ["FAULT", "NONE", True, faultLine[5][4]]

                # finds the input that needs to be changed to the fault line
                for key in faultCircuit:
                    if faultLine[5][0] == key[5:]:
                        inputIndex = 0
                        for gateInput in faultCircuit[key][1]:
                            if faultLine[5][2] == gateInput[5:]:
                                faultCircuit[key][1][inputIndex] = "faultWire"

                            inputIndex += 1

            # runs Circuit Simulation
            faultCircuit = basic_sim(faultCircuit)
            reset_Gate_T_F(faultCircuit)  # function to reset all False to true for each gate that is not a DFF
            # gets the output
            faultOutput = ""
            for y in faultCircuit["OUTPUTS"][1]:
                if not faultCircuit[y][2]:
                    faultOutput = "NETLIST ERROR: OUTPUT LINE \"" + y + "\" NOT ACCESSED"
                    break
                faultOutput = str(faultCircuit[y][3]) + faultOutput

            # checks to see if the fault was detected
            if output != faultOutput:
                faultLine[fileIndex] = True

        for key in circuit:
            if (key[0:5] == "wire_"):
                circuit[key][2] = False
                circuit[key][3] = 'U'
        cycle = cycle + 1
    return circuit


def reset_Gate_T_F(circuit):
    # print("stuck at resetting gates\n")
    from p2sim import printCkt
    for curr in circuit:
        #print("Curr is:" + str(circuit[curr]))
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


# If this module is executed alone
if __name__ == "__main__":
    # let's read the name of bench file
    fileName = "s27.bench"
    testVector = [1, 0, 1]
    circuit = p2sim.netRead(fileName)
    #create own tuple testvestor
    #p2sim.printCkt(circuit)
    #print(circuit)
    #circuit = getBasicSim(circuit, 5, 0, "full", fileName)