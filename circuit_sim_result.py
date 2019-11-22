import math
from testVectorUI import testVectorGen
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
    print("inside getBasicSim\n")
    circuit = inputRead(circuit, user_tv_str)
    cycle = 0
    while cycle < total_cycles:
        basic_sim(circuit)
        reset_Gate_T_F(circuit)  # function to reset all False to true for each gate that is not a DFF
        cycle = cycle + 1
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
    print("inside getFaultCvgSeq\n")
    # incorporate fault
    cycle = 0
    while cycle < total_cycles:
        # line 566-666 down make TV a line
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






