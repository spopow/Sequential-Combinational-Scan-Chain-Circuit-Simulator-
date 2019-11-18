
import os
import math

########################################################################
# These functions allow for prompting the user to input test vector t, 
# in integer form, supporting negative values
# temporary UI is used for testing purposes
########################################################################


# FUNCTION: inputSizeFinder - Finds the number of inputs given a circuit
# INPUT: Circuit, supporting sequential circuits
# OUTPUT: integer value of number of inputs

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

# FUNCTION: twoComptoBinary - Converts an integer to two's complement of a specified num of digits
# INPUT: integer value - intVal, number of bits - numbits
# OUTPUT: integer value of number of inputs
def twoComptoBinary(intVal, numBits):
    s = bin(intVal & int("1"*numBits, 2))[2:]
    return ("{0:0>%s}" % numBits).format(s)

# FUNCTION: testVectorGen - Wrapper function to create a binary string test vector in two's complement
def testVectorGen(circuit, intVal):
    numBits = inputSizeFinder(circuit)
    if (intVal >= 2 ** numBits):
        print("\nCannot represent ", intVal, " with ", numBits, " using circuit,", circuit )
        return
    else:
        return twoComptoBinary(intVal, numBits)

            
#input bench file
def main():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    inputSize = 0
    intVal = 0

#User interface for reading in file
    while True:
        cktFile = "circ.bench"
        print("\n Read circuit benchmark file: use " + cktFile + "?" + " Enter to accept or type filename: ")
        userInput = input()

        if userInput == "":
            break
        else:
            #If the user clicked enter, the program proceeds to user c432.bench
            cktFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(cktFile):
                print("File does not exist. \n")
            else:
                break

    while True:
        print("\n Use 0 as your test vector? ")
        userInput = input()
        if userInput =="":
            print(" \n Your integer for your test vector is: ", intVal)
            break
        else: 
            intVal = int(userInput)
            print(" \n Your integer for your test vector is: ", intVal)
            break


    print(testVectorGen(cktFile, intVal))



if __name__ == "__main__":

    main()



 