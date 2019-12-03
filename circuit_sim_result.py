import math
import copy
import csv

from testVectorUI import testVectorGen
import json
# input t,n,f
# t = test vector, n = cycles ran,f = fault
# output : content of all ff's, primary outputs for good circuit and a fault


def output_file(bench_file, num_cycles, fault, user_tv_str):
    from p2sim import netRead, printCkt
    from scan_chain_sim_result import outputComparator

    simulatorTxt = open("simulator.txt", "w+")
    circuit = netRead(bench_file)  # create original circuit
    clean_circuit = netRead(bench_file)
    Fault_bool = False

    # create circuit and update values
    good_circuit, goodList = getBasicSim(circuit, num_cycles, user_tv_str, Fault_bool, fault)
    simulatorTxt.write("******************GOOD CIRCUIT SIM********************\n")
    simulatorTxt.write("Flip Flop & Primary Outputs @ n = " + str(num_cycles) + "\n")
    simulatorTxt.write("User TV: " + user_tv_str + "\n")

    numFlipFlops = getNumFF(bench_file)

    printFFvalues(good_circuit, simulatorTxt)  # call function that prints ff/value
    numPrimOutputs = getNumPrimaryOutputs(bench_file)

    printPOValues(good_circuit, simulatorTxt)  # call function that prints PO value

    # make circuit with fault and update values
    Fault_bool = True
    badCircuit, badList = getBasicSim(clean_circuit, num_cycles, user_tv_str, Fault_bool, fault)
   
    simulatorTxt.write("\n******************BAD CIRCUIT SIM********************\n")
    simulatorTxt.write("Fault: " + str(fault) + "\n")
    simulatorTxt.write("Flip Flop & Primary Outputs @ n = " + str(num_cycles) + "\n")
    simulatorTxt.write("\n******************FAULT DETECTION********************\n")
    if outputComparator(badList, goodList)[0]:
        compOut = "\n" + fault + " has been detected at cycle " + str(outputComparator(badList, goodList)[1]) + " with test vector " + user_tv_str + "\n"
        simulatorTxt.write(compOut)
    else:
        compOut = "\n" + fault + " has NOT been detected with test vector " + user_tv_str + "\n"
        simulatorTxt.write(compOut)
    # call function that prints ff/value
    printFFvalues(badCircuit, simulatorTxt)
    # function that prints output value
    printPOValues(badCircuit, simulatorTxt)
    print("\nCreated simulator.txt with results of simulation\n")


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
    # print("stuck at get basic sim\n")
    from p2sim import basic_sim, inputRead
    from scan_chain_sim_result import storePrimaryOutputs
    circuit = inputRead(circuit, user_tv_str)
    cycle = 0
    badList = []
    goodList = []
    
    while cycle < total_cycles:
        if Fault_bool:
            # sets fault line = true
            circuit = getFaultCircuit(circuit, fault)
        circuit = basic_sim(circuit, Fault_bool, fault)
        if Fault_bool:
            badList.append(storePrimaryOutputs(circuit, badList))
        else:
            goodList.append(storePrimaryOutputs(circuit, goodList))

        # reset all except dff's/PIs
        circuit = reset_Gate_T_F(circuit)
        cycle = cycle + 1
        print("Running Cycle: " + str(cycle) + "\n")
    print("Done with basic sim with Fault = " + str(Fault_bool) + "\n")
    if Fault_bool:
        return circuit, badList
    else:
        return circuit, goodList


def getFaultCircuit(circuit, fault):
    from p2sim import printCkt
    fault = fault_processing(fault)
    faultCircuit = copy.deepcopy(circuit)

    faultLine = fault
    # handles stuck at faults
    # print("faultline/fault: ")
    # print(faultLine)         DEBUG COMMENT
    # print("\n")
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
    return faultCircuit


def printFFvalues(circuit, file):
    flipFlopNum = 0
    file.write('---------------------DFF VALUES-------------------------')
    for gate in circuit:
        if circuit[gate][0] == 'DFF':
            dFlipFlop = '\n DFF_' + str(flipFlopNum) + ": " + str(circuit[gate][3]) + " "
            flipFlopNum = flipFlopNum + 1
            file.write(dFlipFlop)


def printPOValues(circuit, simulatorTxt):
    outputList = circuit["OUTPUTS"][1]
    # get prim outputs from circuit
    # go through prim values
    # print values
    simulatorTxt.write('\n-----------------Primary Output Values-----------------')
    for output in outputList:
        poVal = "\n" + output + ": " + circuit[output][3]
        simulatorTxt.write(poVal)


def reset_Gate_T_F(circuit):
    for curr in circuit:
        currLen = len(circuit[curr])
        if currLen == 4 and circuit[curr][0] != 'DFF' and circuit[curr][0] != 'INPUT':
            circuit[curr][2] = False
    return circuit


def fault_processing(fault):
    line = fault
    line = line.replace("\n", "")
    data = []
    for _ in range(5):
        data.append(False)
    data.append(line.split("-"))

    return data


def seq_data_analysis(bench_file, cycles):
    from p2sim import netRead
    from scan_chain_sim_result import LFSRtestGen, scanFaultDetector
    from genFaultList import getFaultListStudy

    first_line_csv = ['Initialization ->', 'FF=U', 'FF=1', 'FF=0']
    with open('seq_simulator_analysis.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(first_line_csv)

    # generating fault list for circuit
    fault_list = getFaultListStudy(bench_file)
    total_num_faults = len(fault_list)
    print("\ncircuit has: " + total_num_faults + " test vectors\n")

    # generating a Mersenne tv and return list with a tv for every fault we r testing
    _, input_TVs = LFSRtestGen(bench_file, total_num_faults)
    num_tvs = len(input_TVs)
    print("\njust generated: " + num_tvs + " test vectors\n")

    # creating csv file to plot data
    num_fault = 0

    circuit = netRead(bench_file)
    # doing initialization for corresponding circuits DFF
    circuit_u = netRead(bench_file)
    # circuit_one = ff_init_one(original_circuit)
    # circuit_zero = ff_init_zero(original_circuit)

    while num_fault < total_num_faults:
        column = 0
        while column < 3:
            print("column #:" + str(column) + "\n")

            Fault_bool = True
            # call getBasicSim for each circuit w/fault
            circuit_u_f = getBasicSim(circuit_u, cycles, input_TVs[num_fault], Fault_bool, fault_list[num_fault])
            # circuit_one_f = getBasicSim(circuit_one, cycles, input_TVs[num_fault], Fault_bool, fault_list[num_fault])
            # circuit_zero_f = getBasicSim(circuit_zero, cycles, input_TVs[num_fault], Fault_bool, fault_list[num_fault])

            Fault_bool = False
            # call getBasicSim for each circuit wout/fault
            circuit_u_nf = getBasicSim(circuit_u, cycles, input_TVs[num_fault], Fault_bool, fault_list[num_fault])
            # circuit_one_nf = getBasicSim(circuit_one, cycles, input_TVs[num_fault], Fault_bool, fault_list[num_fault])
            # circuit_zero_nf = getBasicSim(circuit_zero, cycles, input_TVs[num_fault], Fault_bool, fault_list[num_fault])


            # call function that gets cycle where fault was found
            scanFaultDetector(circuit)

        num_fault += 1




def ff_init_one(circuit):

    return circuit

def ff_init_zero(circuit):

    return circuit
