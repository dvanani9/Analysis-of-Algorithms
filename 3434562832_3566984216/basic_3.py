import psutil
import sys
import time

# Get Cost Function
def getCost(i, j):
    if X_Sequence[i-1]=='A': ith=0
    elif X_Sequence[i-1]=='C': ith=1
    elif X_Sequence[i-1]=='G': ith=2
    elif X_Sequence[i-1]=='T': ith=3

    if Y_Sequence[j-1]=='A': jth=0
    elif Y_Sequence[j-1]=='C': jth=1
    elif Y_Sequence[j-1]=='G': jth=2
    elif Y_Sequence[j-1]=='T': jth=3
    cost=costMatrix[ith][jth]
    return cost
    
# To get Alignment
def getAlignment(i, j):
    if X_Sequence[i-1]=='A': ith=0
    elif X_Sequence[i-1]=='C': ith=1
    elif X_Sequence[i-1]=='G': ith=2
    elif X_Sequence[i-1]=='T': ith=3

    if Y_Sequence[j-1]=='A': jth=0
    elif Y_Sequence[j-1]=='C': jth=1
    elif Y_Sequence[j-1]=='G': jth=2
    elif Y_Sequence[j-1]=='T': jth=3
    
    return [charMapping[ith] if i>0 else '_', charMapping[jth] if j>0 else '_']

# Find Minimum Cost and Alignment
def minCostAndAlignment():
    # Fill DP Table
    for i in range(len(X_Sequence)+1):
        opt[i][0] = deltaVal*i
    for j in range(len(Y_Sequence)+1):
        opt[0][j] = deltaVal*j
    for i in range(1, len(X_Sequence)+1):
        for j in range(1, len(Y_Sequence)+1):
            opt[i][j] = min(opt[i-1][j-1] + getCost(i, j),
                                deltaVal + opt[i][j-1],
                                deltaVal + opt[i-1][j])

    # Write Optimal Cost
    f_write.write(str(opt[len(X_Sequence)][len(Y_Sequence)]))

    # TopDown Pass
    X_Align_List= []
    Y_Align_List= []
    i,j = len(X_Sequence), len(Y_Sequence)
    while i and j:
        if opt[i][j] == getCost(i, j) + opt[i-1][j-1] :
            alignStore=getAlignment(i, j)
            X_Align_List.insert(len(X_Align_List),alignStore[0])
            Y_Align_List.insert(len(Y_Align_List),alignStore[1])
            i = i-1
            j = j-1
        elif opt[i][j-1] + deltaVal == opt[i][j]:
            alignStore=getAlignment(0, j)
            X_Align_List.insert(len(X_Align_List),alignStore[0])
            Y_Align_List.insert(len(Y_Align_List),alignStore[1])
            j = j -1
        else:
            alignStore=getAlignment(i, 0)
            X_Align_List.insert(len(X_Align_List),alignStore[0])
            Y_Align_List.insert(len(Y_Align_List),alignStore[1])
            i = i-1
    while i:
        alignStore=getAlignment(i, 0)
        X_Align_List.insert(len(X_Align_List),alignStore[0])
        Y_Align_List.insert(len(Y_Align_List),alignStore[1])
        i = i-1
    while j:
        alignStore=getAlignment(0, j)
        X_Align_List.insert(len(X_Align_List),alignStore[0])
        Y_Align_List.insert(len(Y_Align_List),alignStore[1])
        j = j -1
    
    # Will return final alignment of X and Y in list form
    return [X_Align_List[::-1],Y_Align_List[::-1]]
    
def sequenceAlignmentPrint(list_X_Y_pairs):
    X_Sequence_List, Y_Sequence_List  = [],[]

    for i in list_X_Y_pairs[1]:
        Y_Sequence_List.append(i)

    for i in list_X_Y_pairs[0]:
        X_Sequence_List.append(i)

    final_X=''.join(X_Sequence_List)
    final_Y=''.join(Y_Sequence_List)
    f_write.write("\n"+final_X)
    f_write.write("\n"+final_Y)

# Memory Consumption Function
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

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
            # Because '\n' character will not come at end of file read so it would not go in the 'if' above
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


# *****************Driver Code Starts************************

start_time = time.time()
f_write=open(sys.argv[2],'w')
# Generate the Strings
stringList=stringGenerator()

deltaVal = 30
charMapping = {
    0:'A',
    1:'C',
    2:'G',
    3:'T'
    }
# Mismatch Scores
costMatrix = [[0,110,48,94],
           [110,0,118,48],
           [48,118,0,110],
           [94,48,110,0]]
string1=stringList[0]
string2=stringList[1]

# Converting String to List
X_Sequence = list(string1)
Y_Sequence = list(string2)

# Fill DP matrix with zeros
opt= [[0 for i in range(len(Y_Sequence)+1)] for j in range(len(X_Sequence)+1)]

# Basic Sequence Alignment Algorithm
sequenceAlignmentPrint(minCostAndAlignment())

end_time = time.time()
time_taken = (end_time - start_time)*1000
memory_took=process_memory()
f_write.write("\n"+str(time_taken))
f_write.write("\n"+str(memory_took))


# *****************Driver Code Ends************************