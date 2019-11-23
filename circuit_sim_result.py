import math
import copy
from testVectorUI import testVectorGen
import json
# input t,n,f
# t = test vector, n = cycles ran,f = fault
# output : content of all ff's, primary outputs for good circuit and a fault


def output_file(bench_file, num_cycles, fault, user_tv_str):
    from p2sim import netRead
    simulatorTxt = open("simulator.txt", "w+")
    circuit = netRead(bench_file)  # create original circuit
    good_circuit = getBasicSim(circuit, num_cycles, user_tv_str)  # to create circuit with fault and update values - JAS - TO-DO
    simulatorTxt.write("******************GOOD CIRCUIT SIM********************\n")
    simulatorTxt.write("Flip Flop & Primary Outputs @ n= " + str(num_cycles) + "\n")
    simulatorTxt.write("*****************************************************\n")
    numFlipFlops = getNumFF(bench_file)
    simulatorTxt.write("D-Type Flip Flops:" + numFlipFlops + "\n")
    simulatorTxt.write("-----------------------------\n")
    printFFvalues(good_circuit, numFlipFlops)  # call function that prints ff/value - ALEXIS TO-DO
    numPrimOutputs = getNumPrimaryOutputs(bench_file)
    simulatorTxt.write("Primary Outputs:" + str(numPrimOutputs) + "\n")
    simulatorTxt.write("-----------------------------\n")
    printPOValues(good_circuit, numPrimOutputs)  # call function that prints primary output value - SZYMON TO-DO
    # badCircuit = getFaultCvgSeq(circuit, fault, num_cycles)  # to create circuit with fault and update values - JAS TD
    simulatorTxt.write("******************BAD CIRCUIT SIM********************\n")
    simulatorTxt.write("Fault: " + str(fault) + "\n")
    simulatorTxt.write("Flip Flop & Primary Outputs @ n= " + str(num_cycles) + "\n")
    simulatorTxt.write("*****************************************************\n")
    simulatorTxt.write("D-Type Flip Flops:" + numFlipFlops + "\n")
    simulatorTxt.write("-----------------------------\n")
    # call function that prints ff/value
    printFFvalues(circuit)
    simulatorTxt.write("Primary Outputs:" + str(numPrimOutputs) + "\n")
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
    print("getting Num primary inputs\n")
    print("reading bench file\n")
    benchFile = open(bench_file, "r")
    # get line: "1 outputs"
    for line in benchFile:
        if "outputs" in line:
            num_inputs_here = str.split(" ")
    return num_inputs_here[1]


def getBasicSim(circuit, total_cycles, user_tv_str):
    from p2sim import basic_sim, inputRead
    circuit = inputRead(circuit, user_tv_str)
    cycle = 0
    while cycle < total_cycles:
        print('Its stuck before basic sim')
        circuit = basic_sim(circuit) 
        circuit = reset_Gate_T_F(circuit)  # function to reset all False to true for each gate that is not a DFF
        print("gates being reset to false")
        cycle = cycle + 1
        
    file1 = open("myfile.txt","w")#write mode 
    file1.write(json.dumps(circuit, indent=4, sort_keys=True)) 
    file1.close() 
    return circuit


def printFFvalues(circuit, numFlipFlops):
    print("inside printFF values function\n")
    simulatorTxt = open("simulator.txt", "a")
    i = 0
    while i < numFlipFlops:
        simulatorTxt.write(" ")
        i = i+1


def printPOValues(circuit, numPrimOutputs):
    print("inside printPO values function\n")
    simulatorTxt = open("simulator.txt", "a")
    i = 0
    while i < numPrimOutputs:
        simulatorTxt.write(" ")
        i = i+1


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
            if (output != faultOutput):
                faultLine[fileIndex] = True

        for key in circuit:
            if (key[0:5] == "wire_"):
                circuit[key][2] = False
                circuit[key][3] = 'U'
        cycle = cycle + 1
    return circuit


def reset_Gate_T_F(circuit):
    queue = list(circuit["GATES"][1])
    i = 1
    while True:
        i -= 1
        # If there's no more things in queue, done
        if len(queue) == 0:
            break

        # Remove the first gate element of the queue and assign it to a variable for us to use
        curr = queue[0]
        queue.remove(curr)

        # initialize a flag, used to check if every terminal has been accessed
        term_has_value = True

        # Check if the terminals have been accessed
        for term in circuit[curr][1]:
            if not circuit[term][2]:
                term_has_value = False
                break

        if term_has_value:

            # checks to make sure the gate output has not already been set
            if circuit[curr][2] is False:
                circuit[curr][2] = True

    return circuit






