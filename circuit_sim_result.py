import math
import copy
from testVectorUI import testVectorGen
import json
# input t,n,f
# t = test vector, n = cycles ran,f = fault
# output : content of all ff's, primary outputs for good circuit and a fault


def output_file(bench_file, num_cycles, fault, user_tv_str):
    from p2sim import netRead, printCkt
    simulatorTxt = open("simulator.txt", "w+")
    circuit = netRead(bench_file)  # create original circuit
    good_circuit = getBasicSim(circuit, num_cycles, user_tv_str)  # to create circuit with fault and update values
    printCkt(good_circuit)
    simulatorTxt.write("******************GOOD CIRCUIT SIM********************\n")
    simulatorTxt.write("Flip Flop & Primary Outputs @ n = " + str(num_cycles) + "\n")
    simulatorTxt.write("******************************************************\n")
    numFlipFlops = getNumFF(bench_file)
    simulatorTxt.write("D-Type Flip Flops: " + numFlipFlops + "\n")
    printFFvalues(good_circuit, simulatorTxt)  # call function that prints ff/value - ALEXIS TO-DO
    numPrimOutputs = getNumPrimaryOutputs(bench_file)
    simulatorTxt.write("\nPrimary Outputs: " + str(numPrimOutputs) + "\n")
    printPOValues(good_circuit, simulatorTxt)  # call function that prints PO value - SZYMON TO-DO
    # badCircuit = getFaultCvgSeq(circuit, fault, num_cycles)  # make circuit with fault and update values - JAS TD
    simulatorTxt.write("\n******************BAD CIRCUIT SIM********************\n")
    simulatorTxt.write("Fault: " + str(fault) + "\n")
    simulatorTxt.write("Flip Flop & Primary Outputs @ n = " + str(num_cycles) + "\n")
    simulatorTxt.write("*****************************************************\n")
    simulatorTxt.write("D-Type Flip Flops: " + numFlipFlops + "\n")
    # call function that prints ff/value
    printFFvalues(circuit, simulatorTxt)
    simulatorTxt.write("\nPrimary Outputs: " + str(numPrimOutputs) + "\n")
    simulatorTxt.write("-----------------------------\n")
    # function that prints output value


def getNumFF(bench_file):
    benchFile = open(bench_file, "r")
    # get line: "# 3 D-type flipflops "
    for line in benchFile:
        if "D-type flipflops" in line:
            num_ff_here = line.split(" ")
    return num_ff_here[1]


def getNumPrimaryOutputs(bench_file):
    numOutputs = 0
    #print("getting Num primary inputs\n")
    #print("reading bench file\n")
    benchFile = open(bench_file, "r")
    # get line: "1 outputs"
    for line in benchFile:
        if "outputs" in line:
            numOutputs = numOutputs + 1
    return numOutputs


def getBasicSim(circuit, total_cycles, user_tv_str):
    print("stuck at get basic sim\n")
    from p2sim import basic_sim, inputRead
    circuit = inputRead(circuit, user_tv_str)
    cycle = 0
    while cycle < total_cycles:
        circuit = basic_sim(circuit)
        circuit = reset_Gate_T_F(circuit)  # function to reset all False to true for each gate that is not a DFF
        print("gates being reset to false")
        cycle = cycle + 1
        print("running cycle: " + str(cycle) + "\n")

    return circuit


def printFFvalues(circuit, file):
    flipFlopNum = 0
    file.write('**********************DFF VALUES**********************')
    for gate in circuit:
        if circuit[gate][0] == 'DFF':
            dFlipFlop = '\n DFF_' + str(flipFlopNum) + ": " + str(circuit[gate][3]) + " "
            flipFlopNum = flipFlopNum + 1
            file.write(dFlipFlop)
    file.write('\n******************************************************')


def printPOValues(circuit, simulatorTxt):
    outputList = circuit["OUTPUTS"][1]
    # get prim outputs from circuit
    # go through prim values
    # print values
    simulatorTxt.write('*****************Primary Output Values*****************')
    for output in outputList:
        
        poVal = "\n" + output + ": " + circuit[output][3]
        simulatorTxt.write(poVal)
    simulatorTxt.write('\n******************************************************')




def getFaultCvgSeq(circuit, fault, total_cycles):
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
            if (faultLine[fileIndex] == True):
                continue

            # creates a copy of the circuit to be used for fault testing
            faultCircuit = copy.deepcopy(circuit)

            for key in faultCircuit:
                if (key[0:5] == "wire_"):
                    faultCircuit[key][2] = False
                    faultCircuit[key][3] = 'U'

            # sets up the inputs for the fault circuit
            faultCircuit = inputRead(faultCircuit, line)

            # handles stuck at faults
            if (faultLine[5][1] == "SA"):
                for key in faultCircuit:
                    if (faultLine[5][0] == key[5:]):
                        faultCircuit[key][2] = True
                        faultCircuit[key][3] = faultLine[5][2]

            # handles in in stuck at faults by making a new "wire"
            elif (faultLine[5][1] == "IN"):
                faultCircuit["faultWire"] = ["FAULT", "NONE", True, faultLine[5][4]]

                # finds the input that needs to be changed to the fault line
                for key in faultCircuit:
                    if (faultLine[5][0] == key[5:]):
                        inputIndex = 0
                        for gateInput in faultCircuit[key][1]:
                            if (faultLine[5][2] == gateInput[5:]):
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
    #print("stuck at resetting gates\n")
    from p2sim import printCkt
    for curr in circuit:
        print("Curr is:" + str(circuit[curr]))
        currLen = len(circuit[curr])
        if currLen == 4 and circuit[curr][0] != 'DFF' and circuit[curr][0] != 'INPUT':
            circuit[curr][2] = False
            # print("Curr is now: " + str(circuit[curr]) + "\n")
    return circuit
