import os
import math
import random

def convert(s): 
  
    # initialization of string to "" 
    str1 = "" 
  
    # using join function join the list s by  
    # separating words by str1 
    return(str1.join(s))

def LFSR_234(startSeed):

    testVector = ''
    nextVector = [None] * 8 #temporary test vector that LFRS's TestVector

    # initialize test vector to a string of 8 bits
    testVector = format(startSeed, '08b')

    # Initialize 8 bit test vector and flip its bits
    testVector = testVector[::-1]

    #Hardcode LFSR
    nextVector[0] = testVector[7]
    nextVector[1] = testVector[0]
    nextVector[2] = str(int(testVector[7]) ^ int(testVector[1]))
    nextVector[3] = str(int(testVector[7]) ^ int(testVector[2]))
    nextVector[4] = str(int(testVector[7]) ^ int(testVector[3]))
    nextVector[5] = testVector[4]
    nextVector[6] = testVector[5]
    nextVector[7] = testVector[6]

    #Convert testVector and Reverse the array
    testVector = convert(nextVector)
    testVector = testVector[::-1]
    
    #We need to make sure we output an integer
    testVector = int(testVector, 2)

    return testVector

def TestVector_A(inputSize, startSeed):
    outVect = ''        #output vector at each line
    outputName = "TV_A.txt"

    outputFile = open(outputName,"w")
    outputFile.write("#seed: " + str(startSeed) + "\n")
    #we have to deduce the number of seeds based on the inputs size and 8bit seed size
    #numSeeds = math.ceil(inputSize / 8)
    for _ in range(255):
        outVect = format(0, '0'+str(inputSize) + 'b') + format(startSeed, '08b')
        startSeed += 1
        outVect = outVect[::-1]
        #Cuts string to size of the input
        outVect = outVect[0:inputSize]
        outVect = outVect[::-1]

        outputFile.write(outVect + '\n')
        outVect = ''


#multiple 8-bit counters
def TestVector_B(inputSize, startSeed):
    vectorList = []     #list of Vectors 0-255
    newSeed = 0         #next seed vector in sequence
    outVect = ''        #output vector at each line
    outputName = "TV_B.txt"

    outputFile = open(outputName,"w")
    outputFile.write("#seed: " + str(startSeed) + "\n")
    #we have to deduce the number of seeds based on the inputs size and 8bit seed size
    numSeeds = math.ceil(inputSize / 8)

    #append the start seed to the list
    vectorList.append(startSeed)
    for x in range(255):
        #The first seed passed to the LFSR is startseed
        newSeed = vectorList[x]
        startSeed +=1
        #We then append the next seed into the next line of the vector list
        vectorList.append(startSeed)

        for x in range(numSeeds):
            outVect = outVect + format(newSeed, '08b')[::-1]

        #Cuts string to size of the input
        outVect = outVect[0:inputSize]

        #Reverses string so output vector is from s[n], s[n-1], s[s-2] ... s[0]
        outVect = outVect[::-1]

        #Writes and resets for the next output
        outputFile.write(outVect + '\n')
        outVect = ''

def TestVector_C(inputSize, startSeed):
    vectorList = []     #list of Vectors 0-255
    newSeed = 0         #next seed vector in sequence
    outVect = ''        #output vector at each line
    outputName = "TV_C.txt"

    outputFile = open(outputName,"w")
    outputFile.write("#seed: " + str(startSeed) + "\n")
    #we have to deduce the number of seeds based on the inputs size and 8bit seed size
    numSeeds = math.ceil(inputSize / 8)

    #append the start seed to the list
    vectorList.append(startSeed)
    for x in range(255):
        #The first seed passed to the LFSR is startseed
        newSeed = vectorList[x]
        startSeed +=1
        #We then append the next seed into the next line of the vector list
        vectorList.append(startSeed)

        for x in range(numSeeds):
            outVect = outVect + format(newSeed, '08b')[::-1]
            newSeed += 1

        #Cuts string to size of the input
        outVect = outVect[0:inputSize]

        #Reverses string so output vector is from s[n], s[n-1], s[s-2] ... s[0]
        outVect = outVect[::-1]

        #Writes and resets for the next output
        outputFile.write(outVect + '\n')
        outVect = ''


def TestVector_D(inputSize, startSeed):
    vectorList = []     #list of Vectors 0-255
    newSeed = 0         #next seed vector in sequence
    outVect = ''        #output vector at each line
    outputName = "TV_D.txt"

    outputFile = open(outputName,"w")
    outputFile.write("#seed: " + str(startSeed) + "\n")
    #we have to deduce the number of seeds based on the inputs size and 8bit seed size
    numSeeds = math.ceil(inputSize / 8)

    #append the start seed to the list
    vectorList.append(startSeed)
    for x in range(255):
        #The first seed passed to the LFSR is startseed
        newSeed = vectorList[x]

        #We then append the next seed into the next line of the vector list
        vectorList.append(LFSR_234(newSeed))

        for x in range(numSeeds):
            outVect = outVect + format(newSeed, '08b')[::-1]

        #Cuts string to size of the input
        outVect = outVect[0:inputSize]

        #Reverses string so output vector is from s[n], s[n-1], s[s-2] ... s[0]
        outVect = outVect[::-1]

        #Writes and resets for the next output
        outputFile.write(outVect + '\n')
        outVect = ''


# Test Vector E --> Multiple 8 bit LFSRS
def TestVector_E(inputSize, startSeed):

    vectorList = []     #list of Vectors 0-255
    newSeed = 0         #next seed vector in sequence
    outVect = ''        #output vector at each line
    outputName = "TV_E.txt"

    outputFile = open(outputName,"w")
    outputFile.write("#seed: " + str(startSeed) + "\n")
    #we have to deduce the number of seeds based on the inputs size and 8bit seed size
    numSeeds = math.ceil(inputSize / 8)

    #append the start seed to the list
    vectorList.append(startSeed)
    for x in range(255):
        #The first seed passed to the LFSR is startseed
        newSeed = vectorList[x]

        #We then append the next seed into the next line of the vector list
        vectorList.append(LFSR_234(newSeed))

        for x in range(numSeeds):
            outVect = outVect + format(newSeed, '08b')[::-1]
            newSeed = LFSR_234(newSeed)

        #Cuts string to size of the input
        outVect = outVect[0:inputSize]

        #Reverses string so output vector is from s[n], s[n-1], s[s-2] ... s[0]
        outVect = outVect[::-1]

        #Writes and resets for the next output
        outputFile.write(outVect + '\n')
        outVect = ''


def MersenneTwisterPRTG(inputSize):
    outVect = ''
    outputName = "MersenneTwisterPRTG.txt"

    outputFile = open(outputName, "w")
   
    for x in range(255):
        outVect = random.randint(0, (2**(inputSize) - 1))
        outVect = format(outVect, '0'+str(inputSize)+'b')
        outputFile.write(outVect + '\n')

    

