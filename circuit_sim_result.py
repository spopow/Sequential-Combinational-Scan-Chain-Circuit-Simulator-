import math


# printing value of sequential circuit sim
def output_file(bench_file, num_cycles):
    print("reading bench file\n")

    # Opening the bench file:
    benchFile = open(bench_file, "r")
    simulatorTxt = open("simulator.txt", "w+")
    simulatorTxt.write("******************GOOD CIRCUIT SIM********************\n")
    simulatorTxt.write("Flip Flop & Primary Outputs @ n= " + num_cycles + "\n")
    simulatorTxt.write("*****************************************************\n")
    numFlipFlops = getNumFF()
    simulatorTxt.write("D-Type Flip Flops:" + numFlipFlops + "\n")
    simulatorTxt.write("-----------------------------\n")


def getNumFF(bench_file):
    print("getting Num FF\n")
    benchFile = open(bench_file, "r")
    # get line: "# 3 D-type flipflops"
    for line in benchFile:
        if "D-type flipflops" in line:
            num_ff_here = str.split()
    return num_ff_here[1]


def getNumPrimaryOutputs(bench_file):
    print("getting Num primary inputs\n")
    benchFile = open(bench_file, "r")
    # get line: "1 outputs"
    for line in benchFile:
        if "outputs" in line:
            num_inputs_here = str.split()
    return num_inputs_here[1]



