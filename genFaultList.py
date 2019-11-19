#!/usr/bin/python3

from __future__ import print_function


# OVERVIEW
# This module generates and displays the full fault ordered list of any given benchmark file to the user via the
# terminal so that the user can choose which fault they would like to simulate for.
# ----------------------------------------------------------------------------------------------------------------------

# input = circuit benchmark file
# output = full fault list

# type of bench file's row : INPUT(1)
# 1] INPUT     (signal)
# 2] OUTPUT    (signal )
# 3] LogicName (input1, input2,...)

# type of fault signal
# 1] X-SA-1/0
# 2] Y-IN-X-SA-1/0

def getFaultList(netName):
    # Opening the netlist file:
    netFile = open(netName, "r")

    # temporary variables
    faults = []  # array of the faults

    # Reading in file line by line
    for line in netFile:

        # NOT Reading any empty lines
        if (line == "\n"):
            continue

        # Removing spaces and newlines
        line = line.replace(" ", "")
        line = line.replace("\n", "")

        # NOT Reading any comments
        if (line[0] == "#"):
            continue

        # Read INPUTs and add faults to list:
        if (line[0:5] == "INPUT"):
            # Removing everything but the line variable name
            line = line.replace("INPUT", "")
            line = line.replace("(", "")
            line = line.replace(")", "")

            # Format the variable name for *VAR_NAME*-SA-0 and *VAR_NAME*-SA-1
            stuckAt0 = line + "-SA-0"
            stuckAt1 = line + "-SA-1"

            # Appending to the fault array
            faults.append(stuckAt0)
            faults.append(stuckAt1)
            continue

        # Read an OUTPUT wire
        # Note that the same wire should also appear somewhere else as a GATE output, so won't do anything with it.
        if line[0:6] == "OUTPUT":
            continue

        # Read a gate output wire, and add to the circuit dictionary
        lineSpliced = line.split("=")  # splicing the line at the equals sign to get the gate output wire
        stuckAt0 = lineSpliced[0] + "-SA-0"
        stuckAt1 = lineSpliced[0] + "-SA-1"
        # Appending faults to the fault list

        faults.append(stuckAt0)
        faults.append(stuckAt1)

        # splicing the line again at the "("  to get the gate logic
        lineSplicedAgain = lineSpliced[1].split("(")

        lineSplicedAgain[1] = lineSplicedAgain[1].replace(")", "")

        # Splicing the the line again at each comma to the get the gate terminals
        inputs = lineSplicedAgain[1].split(",")

        # Turning each term into an integer before putting it into the circuit dictionary
        for signal in inputs:
            stuckAt0 = lineSpliced[0] + "-IN-" + signal + "-SA-0"
            stuckAt1 = lineSpliced[0] + "-IN-" + signal + "-SA-1"
            faults.append(stuckAt0)
            faults.append(stuckAt1)

    totalFaults = len(faults)

    for index, fault in enumerate(faults, 1):
        print(index, '. ' + fault, sep='', end='\n')

    while True:
        print("\nEnter the integer value of the fault you would like to run fault simulation for (default is 1): ")
        userInput = input()
        if userInput == "":
            userChoice = 1
            break

        userChoice = int(userInput)

        if (userChoice <= 0) | (userChoice > totalFaults):
            print("\nChoice not valid. Please enter a valid choice.\n")
        else:
            break

    selectedFault = faults[userChoice - 1]

    return selectedFault


# If this module is executed alone
if __name__ == "__main__":
    # let's read the name of bench file
    fileName = "s27.bench"
    getFaultList(fileName)
