import math
import copy
from testVectorUI import testVectorGen
import json
# input t,n,f
# t = test vector, n = cycles ran,f = fault
# output : content of all ff's, primary outputs for good circuit and a fault


def output_file(bench_file, num_cycles, fault, user_tv_str):
    from p3sim import netRead, printCkt
    from scan_chain_sim_result import outputComparator
    goodList = []
    badList = []

    simulatorTxt = open("simulator.txt", "w+")
    circuit = netRead(bench_file)  # create original circuit
    clean_circuit = netRead(bench_file)
    Fault_bool = False

    # create circuit and update values
    good_circuit = getBasicSim(circuit, num_cycles, user_tv_str, Fault_bool, fault)[0]
    goodList = getBasicSim(circuit, num_cycles, user_tv_str, Fault_bool, fault)[1]
    #printCkt(good_circuit)     DEBUG COMMENT
    simulatorTxt.write("******************GOOD CIRCUIT SIM********************\n")
    simulatorTxt.write("Flip Flop & Primary Outputs @ n = " + str(num_cycles) + "\n")
    #simulatorTxt.write("-------------------------------------------------------\n")
    numFlipFlops = getNumFF(bench_file)
    #simulatorTxt.write("D-Type Flip Flops: " + str(numFlipFlops) + "\n")
    printFFvalues(good_circuit, simulatorTxt)  # call function that prints ff/value
    numPrimOutputs = getNumPrimaryOutputs(bench_file)
    #simulatorTxt.write("\nPrimary Outputs: " + str(numPrimOutputs) + "\n")
    printPOValues(good_circuit, simulatorTxt)  # call function that prints PO value - SZYMON TO-DO
    Fault_bool = True
    badCircuit = getBasicSim(clean_circuit, num_cycles, user_tv_str, Fault_bool, fault)[0]  # make circuit with fault and update values
    badList = getBasicSim(clean_circuit, num_cycles, user_tv_str, Fault_bool, fault)[1]
    #print(outputComparator(badList, goodlist))
   
    simulatorTxt.write("\n******************BAD CIRCUIT SIM********************\n")
    simulatorTxt.write("Fault: " + str(fault) + "\n")
    simulatorTxt.write("Flip Flop & Primary Outputs @ n = " + str(num_cycles) + "\n")
    simulatorTxt.write("\n******************FAULT DETECTION********************\n")
    if (outputComparator(badList, goodList)[0]):
        compOut = "\n" + fault + " has been detected at cycle " + str(outputComparator(badList, goodList)[1]) + " with test vector " + user_tv_str + "\n"
        simulatorTxt.write(compOut)
    else:
        compOut = "\n" + fault + " has NOT been detected with test vector " + user_tv_str + "\n"
        simulatorTxt.write(compOut)
    #simulatorTxt.write("---------------------------------------------------------\n")
    #simulatorTxt.write("D-Type Flip Flops: " + str(numFlipFlops) + "\n")
    # call function that prints ff/value
    printFFvalues(badCircuit, simulatorTxt)
    #simulatorTxt.write("\nPrimary Outputs: " + str(numPrimOutputs) + "\n")
    # function that prints output value
    printPOValues(badCircuit, simulatorTxt)

def getNumFF(bench_file):
    benchFile = open(bench_file, "r")
    # get num ffs
    num_ff = 0
    for line in benchFile:
        if "DFF" in line:
            num_ff = num_ff + 1
    return num_ff


def getNumPrimaryOutputs(bench_file):
    numOutputs = 0
    benchFile = open(bench_file, "r")
    # get line: "1 outputs"
    for line in benchFile:
        if "outputs" in line:
            numOutputs = numOutputs + 1
    return numOutputs


def getBasicSim(circuit, total_cycles, user_tv_str, Fault_bool, fault):
    #print("stuck at get basic sim\n")
    from p3sim import basic_sim, inputRead
    from scan_chain_sim_result import storePrimaryOutputs
    circuit = inputRead(circuit, user_tv_str)
    cycle = 0
    badList = []
    goodList = []
    
    while cycle < total_cycles:
        if Fault_bool:
            #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")   DEBUG COMMENT
            circuit = getFaultCircuit(circuit, fault)  # sets fault line = true
        circuit = basic_sim(circuit, Fault_bool, fault)
        if Fault_bool:
            badList.append(storePrimaryOutputs(circuit, badList))
        else:
            goodList.append(storePrimaryOutputs(circuit, goodList))
        circuit = reset_Gate_T_F(circuit)  # resets all except dff's/PIs
        #print("gates being reset to false")
        cycle = cycle + 1
        print("Running Cycle: " + str(cycle) + "\n")

    print("Done with basic sim with Fault = " + str(Fault_bool) + "\n")
    if Fault_bool:
        return circuit, badList
    else:
        return circuit, goodList


def getFaultCircuit(circuit, fault):
    from p3sim import printCkt
    fault = fault_processing(fault)
    faultCircuit = copy.deepcopy(circuit)

    faultLine = fault
    # handles stuck at faults
    #print("faultline/fault: ")
    #print(faultLine)         DEBUG COMMENT
    #print("\n")
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
    #printCkt(faultCircuit)      DEBUG COMMENT
    return faultCircuit


def printFFvalues(circuit, file):
    flipFlopNum = 0
    file.write('---------------------DFF VALUES-------------------------')
    for gate in circuit:
        if circuit[gate][0] == 'DFF':
            dFlipFlop = '\n DFF_' + str(flipFlopNum) + ": " + str(circuit[gate][3]) + " "
            flipFlopNum = flipFlopNum + 1
            file.write(dFlipFlop)
    #file.write('\n------------------------------------------------------')


def printPOValues(circuit, simulatorTxt):
    outputList = circuit["OUTPUTS"][1]
    # get prim outputs from circuit
    # go through prim values
    # print values
    simulatorTxt.write('\n-----------------Primary Output Values-----------------')
    for output in outputList:
        poVal = "\n" + output + ": " + circuit[output][3]
        simulatorTxt.write(poVal)
   # simulatorTxt.write('\n---------------------------------------------------\n')


def reset_Gate_T_F(circuit):
    #print("stuck at resetting gates\n")
    from p3sim import printCkt
    for curr in circuit:
        #print("Curr is:" + str(circuit[curr]))              DEBUG COMMENT
        currLen = len(circuit[curr])
        if currLen == 4 and circuit[curr][0] != 'DFF' and circuit[curr][0] != 'INPUT':
            circuit[curr][2] = False
            # print("Curr is now: " + str(circuit[curr]) + "\n")
    return circuit


def fault_processing(fault):
    #print("doing fault processing")
    line = fault
    line = line.replace("\n", "")
    data = []
    for _ in range(5):
        data.append(False)
    data.append(line.split("-"))
    #print("data: ")                DEBUG COMMENT
    #print(data)                    DEBUG COMMENT
    #print("\n")                    DEBUG COMMENT
    line = line.split("-")
    #print("line w/no dashes: ")     DEBUG COMMENT
    #print(line)                     DEBUG COMMENT
    #print("\n")                     DEBUG COMMENT

    return data

