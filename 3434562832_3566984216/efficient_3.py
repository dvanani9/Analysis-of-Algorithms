import psutil
import time
import sys
from resource import *

# Basic Algorithm for Sequence Alignment
def basicAlgorithm(stringX, stringY):    
    # Fill the DP table
    for i in range(len(stringX)+1):
        opt[i][0] = deltaVal*i
    for j in range(len(stringY)+1):
        opt[0][j] = deltaVal*j
    for i in range(1, len(stringX)+1):
        for j in range(1, len(stringY)+1):
            mismatchCost = cost[char_to_int[stringX[i-1]]][char_to_int[stringY[j-1]]]
            opt[i][j] = min(mismatchCost + opt[i-1][j-1],
                            deltaVal + opt[i][j-1] , deltaVal + opt[i-1][j])

    # Alignment Calculation using Top-Down Pass
    i, j = len(stringX), len(stringY)
    alignX = []
    alignY = []
    while i > 0 and j > 0:
        mismatchCost = cost[char_to_int[stringX[i-1]]][char_to_int[stringY[j-1]]]
        if opt[i][j] == mismatchCost + opt[i-1][j-1]:
            alignX.insert(len(alignX),stringX[i-1])
            alignY.insert(len(alignY),stringY[j-1])
            i = i - 1
            j = j - 1
        elif opt[i][j] == deltaVal + opt[i-1][j]:
            alignX.insert(len(alignX),stringX[i-1])
            alignY.insert(len(alignY),'_')
            i = i - 1
        elif opt[i][j] == deltaVal + opt[i][j-1]:
            alignX.insert(len(alignX),'_')
            alignY.insert(len(alignY),stringY[j-1])
            j = j - 1
    while i > 0:
        alignX.insert(len(alignX),stringX[i-1])
        alignY.insert(len(alignY),'_')
        i = i - 1
    while j > 0:
        alignX.insert(len(alignX),'_')
        alignY.insert(len(alignY),stringY[j-1])
        j = j - 1
    # [Reversed Alignment 1, Reversed Alignment 2, Cost]
    return [''.join(alignX)[::-1], ''.join(alignY)[::-1], opt[len(stringX)][len(stringY)]]

# Calculate cost from Left.
def fromLeft(stringX, stringY):
    opt = []
    opt=[[0 for i in range(len(stringY)+1)] for j in range(len(stringX)+1)]
    for i in range(len(stringX)+1):
        opt[i][0] = deltaVal*i
    for j in range(len(stringY)+1):
        opt[0][j] = deltaVal*j
    for i in range(1, len(stringX)+1):
        for j in range(1, len(stringY)+1):
            mismatchCost = cost[char_to_int[stringX[i-1]]][char_to_int[stringY[j-1]]]
            opt[i][j] = min(mismatchCost + opt[i-1][j-1],
                            deltaVal + opt[i-1][j], deltaVal + opt[i][j-1])
        # free the occupied memory
        pos=i-1
        opt[pos] = []
    res=opt[len(stringX)]
    return res    

# Calculate cost from right.
def fromRight(stringX, stringY):
    opt = []
    opt=[[0 for i in range(len(stringY)+1)] for j in range(len(stringX)+1)]
    for i in range(len(stringX)+1):
        opt[i][0] = deltaVal*i
    for j in range(len(stringY)+1):
        opt[0][j] = deltaVal*j
    for i in range(1, len(stringX)+1):
        for j in range(1, len(stringY)+1):
            mismatchCost = cost[char_to_int[stringX[len(stringX)-i]]][char_to_int[stringY[len(stringY)-j]]]
            opt[i][j] = min(mismatchCost + opt[i-1][j-1],
                            deltaVal + opt[i-1][j], deltaVal + opt[i][j-1])
        # free the occupied memory
        pos=i-1
        opt[pos] = []
    res=opt[len(stringX)]
    return res  

# Memory efficient Implementation Uning Divide and Conquer and Dynamic Programming
def memoryEfficientImpl(stringX, stringY):
    if len(stringX)<2 or len(stringY)<2:
        # we call normal space inefficient algorithm
        return basicAlgorithm(stringX, stringY)
    else:
        # Using divide and conquer strategy
        division=[]
        leftOfX = fromLeft(stringX[:int(len(stringX)/2)], stringY)
        rightOfX = fromRight(stringX[int(len(stringX)/2):], stringY)
        for j in range(len(stringY)+1):
            division.append(leftOfX[j] + rightOfX[len(stringY)-j])
        minDivideValue=min(division)
        divisionPoint = division.index(minDivideValue)
        # empty memory to avoid data storage during recursion
        leftOfX=[]
        rightOfX=[]
        division=[]
        # Call Function itself recursively
        leftCall = memoryEfficientImpl(stringX[:int(len(stringX)/2)], stringY[:int(divisionPoint)])
        rightCall = memoryEfficientImpl(stringX[int(len(stringX)/2):], stringY[int(divisionPoint):])
        # Result format: [1st alignment of X, 2nd alignment if Y, cost]
        resultList=[]
        for i in range(3):
            resultList.append(leftCall[i] + rightCall[i])
        return resultList
        
char_to_int = {'A':0, 'C':1, 'G':2, 'T':3}
# Scores Values
cost = [[0,110,48,94],
           [110,0,118,48],
           [48,118,0,110],
           [94,48,110,0]]
deltaVal=30

# Generate Strings from given input
def stringGenerator():
    f = open(sys.argv[1])
    x=f.read()
    mylist=[]
    stringIndices=[]
    tempstr=''
    # To generate the list which includes the strings and the indices for inserting
    for i in range(len(x)):
        if x[i]=='\n':
            mylist.append(tempstr)
            tempstr=''
        else:
            tempstr+=x[i]
            # Because '\n' character will not come at end of file read so it would not go in the if above
            if i==len(x)-1:
                mylist.append(tempstr)

    # To find the indices of the input strings
    j=0
    for i in mylist:
        if i.isalpha():
            stringIndices.append(mylist.index(i,j))
            j+=2

    string1=mylist[stringIndices[0]]
    string2=mylist[stringIndices[1]]
    
    # To generate the string1
    for i in range(int(stringIndices[0]+1),int(stringIndices[1])):
        string1=string1[:int(mylist[i])+1]+string1+string1[int(mylist[i])+1:]

    # To generate the string2
    for i in range(int(stringIndices[1]+1),len(mylist)):
        string2=string2[:int(mylist[i])+1]+string2+string2[int(mylist[i])+1:]
    
    return [string1,string2]

# Memory Consumption Function
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed


# *****************Driver Code Starts************************

start_time = time.time()

# Open output file, in preparation for storing output alignments
f_write=open(sys.argv[2],'w')

# Generate the Strings
stringList=stringGenerator()

stringX=stringList[0]
stringY=stringList[1]

opt = []
# Fill the DP/OPT matrix with zeros
opt=[[0 for i in range(len(stringY)+1)] for j in range(len(stringX)+1)]

costAlignmentList = memoryEfficientImpl(stringX, stringY)

end_time = time.time()
timetaken=(end_time - start_time)*1000

# Write outputs to text file
f_write.write(str(costAlignmentList[2]) + "\n")
f_write.write(costAlignmentList[0] + "\n")
f_write.write(costAlignmentList[1] + "\n")
f_write.write(str(timetaken) + "\n")
f_write.write(str(process_memory()) + "\n")


# *****************Driver Code Ends************************