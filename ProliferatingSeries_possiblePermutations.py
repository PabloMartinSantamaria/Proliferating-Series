from math import gcd
from functools import reduce
from itertools import permutations
from collections import defaultdict

def lcm_list(series:list[int])->int: #calculates the least common multiple of a list
    return reduce(lambda a,b: a*b//gcd(a,b), series)
    
def doubleList(l:list[int])->list[int]:
    return [i for i in l for _ in range(2)]
    
def partitions(n:int, max=None)->list[list[int]]:
    if max is None:       max = n
    if n == 0:            return [[]]
    if n < 0 or max == 0: return []
    withMax = partitions(n - max, max)
    withoutMax = partitions(n, max - 1)
    return [p + [max] for p in withMax] + withoutMax

def canonicalList(L:list[list[int]])->list[(int,list[int])]:
    #takes a list of structures of type list[int]. Normalizes it eliminating repeated structures,
    #sorting and adding the order of the permutations
    return sorted(list(set([(lcm_list(l),tuple(l)) for l in L])))

def possiblePermutationsRI(n:int,t:int)->list[(int,list[int])]:
    permutationsList=[]
    if n==1: return [(1,[1])]
    elif n%2==0:
        if t%2==0: 
            for i in range(2,n+1,2): #loop choosing the cycle containing the 2 self-inverses
                permutationsList.extend([sorted([i]+doubleList(l)) for l in partitions((n-i)//2)])
        else: #if t%2==1
            permutationsList.extend([doubleList(l) for l in partitions(n//2)])
    else: #if n%2==1
        for i in range(3,n+1,2): #loop choosing the cycle in the center
            permutationsList.extend([sorted([i]+doubleList(l)) for l in partitions(int((n-i)/2))])
        if t%n!=0: #in this case the cycle in the center can also be 1
            permutationsList.extend([[1]+doubleList(l) for l in partitions(int((n-1)/2))])
    return canonicalList(permutationsList)

def possiblePermutationsR_coprime_t(n:int)->list[(int,list[int])]:
    def parityOfNumberOfEvens(l): 
        return len([i for i in l if i%2==0])%2 
    if n%4==1 or n%4==2:  #auxiliar variable that has to match parityOfNumberOfEvens(n)
        signature = 0
    else: #if n%4==0 or n%4==3
        signature = 1
    finalList=[l for l in partitions(n) if len(l)<=(n/2)+1 and parityOfNumberOfEvens(l)==signature]
    return canonicalList(finalList)

#From here we have auxiliar functions for possiblePermutations_R. This function generalizes the previous possiblePermutationsR_coprime_t, but 
#it is quite slow in some cases for n>=13.
#It consists of a recursive process that gradually adds notes to the permutations. We will have to save more information
#than just the lengths of the cycles, in permutation structures of the form S=[C1,C2,C3...], where Ci represent the cycles. 
#Those cycles are of the form Ci=[length,cycle], where length is an int and cycle is a list representing which GT-cycles 
#contain the notes in the cycle, and in what order

def equalCycles(cycle1:list[int], cycle2:list[int])->bool: 
    if len(cycle1) != len(cycle2): return False
    separator = "|"
    s1 = separator.join(map(str, cycle1))
    s2 = separator.join(map(str, cycle2))
    return s1 in (s2 + separator + s2)
    
def GTPermutations(GT:list[int])->list[tuple[int]]: #this function calculates the permutations of a GT. Since the GT is ordered 
        #with the greatest element in the left, it is of the form [a_0,...a_0, a_1, ..., a_1, ..., a_k, ..., a_k], with
        #a_0>a_1>...>a_k. We want to calculate permutations of len(GT) that only permute numbers i,j such that GT[i]==GT[j]
    separators = [i for i in range(1,len(GT)) if GT[i]!=GT[i-1]]+[len(GT)]
    permutationsList=list(permutations(range(separators[0])))
    for i in range(1,len(separators)):
        newBlock=list(permutations(range(separators[i-1],separators[i])))
        permutationsList = [x+y for x in permutationsList for y in newBlock]
    return permutationsList 
    
def equalStructures(S1:list[list[(int,list[int])]],S2:list[list[(int,list[int])]],n:int,GT:list[int])->bool: 
    #for a first layer of comprobation of two structures being the same, we permute the GT, since 
    #GT-cycles of the same length are indistinguishable with respect to the structure
    for perm in GTPermutations(GT):
        comprobation=[False for _ in range(len(S1))] #the boolean in position i of this list checks if cycles in position i match
        flag=False #flag turns true in the moment that we detect two cycles which do not match
        if n%2==1: #if n is odd, we have to check separately the first cycle of a structure, since it contains the most recently 
            #added note in it, and it must be in the last position of the cycle. That is, these cycles needen't satisfy equalCycles
            #they have to be exactly the same
            (len1,cyc1)=S1[0]
            (len2,cyc2)=S2[0]
            if len1!=len2: 
                return False #if lengths do not match, we directly return False
            else:
                cyc2 = [perm[i] for i in cyc2] #we apply the permutation to cyc2
                if cyc2==cyc1: #and we check if they are exactly the same, not if they are equalCycles
                    comprobation[0]=True 
                else: 
                    flag=True
        for i in range(n%2,len(S1)): #loop for all the cycles that remain to check(all if n%2==0 or all except the first if n%2==1)
            if flag: break
            (len1,cyc1)=S1[i]
            (len2,cyc2)=S2[i]
            if len1!=len2: 
                return False
            else:
                cyc2 = [perm[i] for i in cyc2]
                if equalCycles(cyc2,cyc1): 
                    comprobation[i]=True #for the rest we do use our last function equalCycles
                else: 
                    flag=True
        if all(comprobation): 
            return True
    return False #if we exit the permutations cycle and all(comprobation) was false always, then there aren't GTpermutations
                 #that make the structures equal

def structurePermutation(S:list[list[(int,list[int])]],n:int)->list[tuple[(list[(int,list[int])])]]: 
    #similar to GTPermutations but with a whole structure. We permute the cycles which have the same length (S will be 
    #given sorted with the greatest cycle in the right, except when n%2==1, where the first cycle will always be a 
    #distinguished one, which we don't want to permute)
    if n%2==1: 
        separators=[1]+[i for i in range(2,len(S)) if S[i-1][0]!=S[i][0]]+[len(S)]
    else:      
        separators=    [i for i in range(1,len(S)) if S[i-1][0]!=S[i][0]]+[len(S)]
    permutationsList=list(permutations(S[:separators[0]]))
    for i in range(1,len(separators)):
        newBlock=list(permutations(S[separators[i-1]:separators[i]]))
        permutationsList = [x+y for x in permutationsList for y in newBlock]
    return permutationsList
    
def strongEqualStructures(S1:list[list[(int,list[int])]],S2:list[list[(int,list[int])]],n:int,GT:list[int])->bool: 
    #for a second layer of checking equal structures, we also have to permute the cycles Ci in the structures 
    permutationsList=structurePermutation(S2,n)
    return any([equalStructures(S1,list(permutedS2),n,GT) for permutedS2 in permutationsList]) 
        
def cycleStructure(S:list[list[(int,list[int])]])->tuple[int]: #extracts the lengths of the cycles of a structure
    return tuple([length for (length,cycle) in S])
    
def eliminateRepeated(structuresList:list[list[list[(int,list[int])]]],n:int,GT:list[int])->list[list[list[(int,list[int])]]]: 
    #the function that combines the previous auxiliary functions to eliminate the repeated structures of a list
    withoutRepeated = [] #initialize the list without repeated structures
    dic=defaultdict(list) #this dictionary saves all the different structures which have the same lengths of cycles 
                          #in order to use strongEqualStructures just when they have the same lengths of cycles
    for S in structuresList:
        if n%2==1: sortedS=[S[0]]+sorted(S[1:]) #sort the structure S mantaining the first if n%2==1
        else:      sortedS=sorted(S)
        projection=cycleStructure(sortedS)
        if dic[projection]==[]:
            dic[projection]=[sortedS]
            withoutRepeated.append(sortedS)
        else:
            flag=False
            for visited in dic[projection]:
                if strongEqualStructures(visited,sortedS,n,GT): 
                    flag = True
                    break
            if not flag: 
                dic[projection].append(sortedS)
                withoutRepeated.append(sortedS)
    return withoutRepeated
        
def auxR(n:int,GT:list[int])->list[list[list[(int,list[int])]]]: #our main function will call this one to make the recursive process
    if n==1: #base case: for n=1 our only structure consists of one cycle in the only cycle of the GT
        permutationsList = [[[1,[0]]]]
    elif n%2==1:
        permutationsList=[] #initialize the list of all possible permutations with n notes and the generalized transposition GT
        for i in range(len(GT)): #loop to apply the inductive step to every cycle of the GT
            if (i==len(GT)-1 or GT[i]!=GT[i+1]) and GT[i]==1: #induction step if we are eliminating a cycle of length 1 from the GT
                auxGT = GT[:]
                del auxGT[i]
                for S in auxR(n-1,auxGT): #loop for every possible structure with n-1 notes and the new GT
                    permutationsList+=[[[1,[len(GT)-1]]]+S] #our permutation consists in adding a cycle of length 1 to each of
                                                            #the previous structures
            elif i==len(GT)-1 or GT[i]!=GT[i+1]: #induction step if we are subtracting 1 to any other cycle of the GT
                auxGT = GT[:]
                auxGT[i]-=1
                for S in auxR(n-1,auxGT): #loop for every possible structure with n-1 notes and the new GT
                    for j in range(len(S)):
                        (length,cycle)=S[j] #we take every cycle of the structure S
                        for k in range(length):
                            if cycle[k]==i: #we instert the new note in every place of the cycle, increasing its length by 1, if
                                            #the note in position k is in the same cycle of the GT as the note added
                                SNew=S[:]
                                SNew.pop(j)
                                newCycle=cycle[k:]+cycle[:k]+[i] 
                                #(it's important that we represent the new cycle with the added note in last place)
                                SNew.insert(0,[length+1,newCycle]) 
                                #we insert the new cycle in the first place to the new structure
                                permutationsList+=[SNew]    
    else: #if n%2==0
        permutationsList=[]
        i = len(GT)-1 #for this case, it suffices that we apply the inductive step for the last cycle of the GT
        m = GT[i]
        if m == 1: #induction step if we are eliminating a cycle of length 1 from the GT
            newGT=GT[:]
            del newGT[i]
            for S in auxR(n-1,newGT): #loop for every possible structure with n-1 notes and the new GT
                SNew=S[:]
                SNew[0][0]+=1   #SNew[0] is of the form (length, cycle); we add the note to the first cycle of our structure
                SNew[0][1]+=[i] #(this is why it's important for the added note be in the last place when n%2==1, and its cycle
                                 #be the first of the structure)
                permutationsList+=[SNew]
        else:  #induction step if we are subtracting 1 to any other cycle of the GT
            newGT=GT[:]
            newGT[i]-=1
            for S in auxR(n-1,newGT): #loop for every possible structure with n-1 notes and the new GT
                (length, cycle)=S.pop(0) #we take the first cycle of the structure. now we have two different 
                                         #operations to apply 
                for j in range(0,len(S)): 
                    (length2,cycle2)=S[j] #the first, we take the other cycles of the structure S
                    for k in range(len(cycle2)):
                        if cycle2[k]==i: #if that cycle contains a note in the same GT-cycle as the note we are adding, then
                                         #we can combine cycle and cycle2 to the final list
                            SNew=S[:]
                            del SNew[j]
                            SNew.append([length+length2+1,[i]+cycle+cycle2[k:]+cycle2[:k]])
                            permutationsList+=[SNew]
                for j in range(len(cycle)): #the second, we loop the first cycle
                    if cycle[j]==i: #for every note of the cycle, if it belogs to the same GT-cycle ad the note we are adding, we can
                                        #divide this cycle into two other cycles and add them to the final list
                        SNew=S[:]
                        SNew.append([1+j,[i]+cycle[0:j]])
                        SNew.append([length-j,cycle[j:len(cycle)]])
                        permutationsList.append(SNew)
    #our final list is already calculated            
    finalList=eliminateRepeated(permutationsList,n,GT) 
    return finalList

def possiblePermutationsR(n,t):
    GT=[n//gcd(n,t) for _ in range(gcd(n,t))] #transform the regular transposition t into a GT
    listOfStructures=auxR(n,GT)
    finalList=[tuple(sorted([length for length,cycle in structure])) for structure in listOfStructures]
    return canonicalList(finalList)