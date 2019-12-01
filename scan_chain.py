#!/usr/bin/python3

from math import ceil, floor

import p2sim


# OVERVIEW
# This module acts as a scan chain library that can be imported to p2sim.py and run partial, full, and parallel
# scan chain fault simulations.
# ----------------------------------------------------------------------------------------------------------------------

# input = circuit dictionary, scan chain type, and testvector
# output = updated circuit dictionary


def scanChain(circuit, scanType, testVector, totalCycles):
    # Counter to keep track of what testvector bit you are accessing
    index = 0

    if scanType == 'partial':

        # Counter to keep track of the number of DFFs
        dffCounter = 0

        # For each gate in the circuit, find the ones that DFFs
        for gate in circuit:
            if circuit[gate][0] == 'DFF':
                dffCounter = dffCounter + 1

        dffCounter = int(ceil(dffCounter / 2))

        for gate in circuit:
            if circuit[gate][0] == 'DFF':
                # When you find a DFF, move the testvector bit in its place
                circuit[gate][3] = testVector[index]
                index = index + 1
                totalCycles = totalCycles + 1

            # Break out if ceil(half) of the DFFs are updated with testvector
            if dffCounter == index:
                break

    if scanType == 'full':

        # For each gate in the circuit, find the ones that DFFs
        for gate in circuit:
            if circuit[gate][0] == 'DFF':
                # When you find a DFF, move the testvector bit in its place
                circuit[gate][3] = testVector[index]
                index = index + 1
                totalCycles = totalCycles + 1

    if scanType == 'parallel':

        # Counter to keep track of what testvector bit you are accessing
        index = 0

        if scanType == 'partial':

            # Counter to keep track of the number of DFFs
            dffCounter = 0

            # For each gate in the circuit, find the ones that DFFs
            for gate in circuit:
                if circuit[gate][0] == 'DFF':
                    dffCounter = dffCounter + 1

            for gate in circuit:
                if circuit[gate][0] == 'DFF':
                    # When you find a DFF, move the testvector bit in its place
                    circuit[gate][3] = testVector[index]
                    index = index + 1

            totalCycles = totalCycles + int(ceil(dffCounter / 2))

    return circuit, totalCycles


# If this module is executed alone
if __name__ == "__main__":
    # let's read the name of bench file
    fileName = "s27.bench"
    testVector = [1, 0, 1]
    circuit = p2sim.netRead(fileName)
    #p2sim.printCkt(circuit)
    circuit = scanChain(circuit, 'partial', testVector, 0)
    print(circuit[1])
