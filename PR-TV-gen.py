
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

#This finds the number of inputs given a circuit
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

def TestVector_A(inputSize, startSeed):
    outVect = ''        #output vector at each line
    outputName = "TV_A.txt"

    outputFile = open(outputName,"w")
    #we have to deduce the number of seeds based on the inputs size and 8bit seed size
    numSeeds = math.ceil(inputSize / 8)
    for x in range(255):
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

    outputFile = open(outputName,"w")
   
    for x in range(255):
        outVect = random.randint(0, 2**(inputSize -1))
        outVect = format(outVect, '0'+str(inputSize)+'b')
        outputFile.write(outVect + '\n')

# Pass in circuit benchmark
def LFSRtestGen(circuit, numCycles):
    listPI = []
    listDFF = []
    outVect = ''
    #vector Size is the num PI and the num DFF
    
    vectPI = inputSizeFinder(circuit)
    vectDFF = _DFFnumFinder(circuit)

    #for how many test cycles, we create that many randomly generated test vectors
    for x in range(numCycles):
        outVect = random.randint(0, 2**(vectPI - 1))
        outVect = format(outVect, '0'+str(vectPI)+'b')
        listPI.append(outVect)
    for x in range(numCycles):
        outVect = random.randint(0, 2**(vectDFF - 1))
        outVect = format(outVect, '0'+str(vectDFF)+'b')
        listDFF.append(outVect)

    #returning a tuple
    return listPI, listDFF

def _DFFnumFinder(circuit):

    f = open(circuit,'r')
    DFFctr = 0
    for line in f:
        if line.find("DFF") > 0:
            DFFctr += 1
            continue

    return DFFctr
#input bench file
def main():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    inputSize = 0
    seedVal = 0
#User interface for reading in file
    while True:
        cktFile = "circuit.bench"
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
        print("\n Use 0 as start seed? Otherwise enter desired starting seed integer, 0-255: ")
        userInput = input()
        if userInput =="":
            print(" \n Your Start seed is: ", seedVal)
            break
        else: 
            seedVal = int(userInput)
            if(seedVal >= 0 & seedVal <= 255):
                print("\n Your Start Seed is:", hex(int(userInput)))
                break
            else:
                print("\n Integer Value not Valid. Enter a valid integer, 1-255")

    #Prereqs for other functions

    inputSize = inputSizeFinder(cktFile)

    # TestVector_A(inputSize, seedVal)
    # TestVector_B(inputSize, seedVal)
    # TestVector_E(inputSize, seedVal)
    # TestVector_D(inputSize, seedVal)
    # TestVector_C(inputSize, seedVal)
    # MarsenneTwisterPRTG(inputSize)
    print(LFSRtestGen(cktFile, 5)[0])
    print(LFSRtestGen(cktFile, 5)[1])



if __name__ == "__main__":

    main()



    #find what input size of bench file

#create 255 Test Vectors to a file called TV_A


 

