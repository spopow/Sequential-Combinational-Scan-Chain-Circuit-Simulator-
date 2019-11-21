import math

# input t,n,f
# t = test vector, n = cycles ran,f = fault
# output : content of all ff's, primary outputs for good circuit and a fault

def output_file(bench_file, num_cycles,fault):
    simulatorTxt = open("simulator.txt", "w+")
    simulatorTxt.write("******************GOOD CIRCUIT SIM********************\n")
    #do circ sim
    good_circuit = getBasicSim(circuit , num_cycles)
    simulatorTxt.write("Flip Flop & Primary Outputs @ n= " + str(num_cycles) + "\n")
    simulatorTxt.write("*****************************************************\n")
    numFlipFlops = getNumFF(bench_file)
    simulatorTxt.write("D-Type Flip Flops:" + numFlipFlops + "\n")
    simulatorTxt.write("-----------------------------\n")
    # function that prints ff/value
    # print circuit
    numPrimOutputs = getNumPrimaryOutputs(bench_file);
    simulatorTxt.write("Primary Outputs:" + str(numPrimOutputs) + "\n")
    simulatorTxt.write("-----------------------------\n")
    # function that prints output value

    simulatorTxt.write("******************BAD CIRCUIT SIM********************\n")
    #do fault sim
    badCircuit = getFaultCvgSeq(circuit, fault, num_cycles)
    simulatorTxt.write("Fault: " + str(fault) + "\n")
    simulatorTxt.write("Flip Flop & Primary Outputs @ n= " + str(num_cycles) + "\n")
    simulatorTxt.write("*****************************************************\n")
    simulatorTxt.write("D-Type Flip Flops:" + numFlipFlops + "\n")
    simulatorTxt.write("-----------------------------\n")
    # function that prints ff/value
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


def getBasicSim(circuit,cycles):
    print("inside getBasicSim\n")
    return circuit


def getFaultCvgSeq(circuit,fault, cycles):
    print("inside getFaultCvgSeq\n")
    return circuit

