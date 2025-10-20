from math import gcd
from functools import reduce
import os
from collections import defaultdict
from itertools import permutations
from contextlib import ExitStack
from enum import Enum

class Transformation(Enum): 
    #the class that defines the transformations that we apply to our series
    P = "P"
    I = "I"
    R = "R"
    RI = "RI"
    def apply(self, series:list[int], t:int, n:int)->list[int]:
        if   self == Transformation.P:  return [(x+t) % n for x in series]
        elif self == Transformation.I:  return [(-x+t) % n for x in series]
        elif self == Transformation.R:  return [(x+t) % n for x in reversed(series)]
        elif self == Transformation.RI: return [(-x+t) % n for x in reversed(series)]

def proliferatingPermutation(transformation:Transformation, series:list[int], t:int, n:int)->list[int]:
    #calculates the permutations obtained from series by appliyng transformation and transposition t.
    #The permutation is stored as a list[int] so that permutations[i] yields the note in the transformed
    #series that is in the same place that i was in the original series
    transformed = transformation.apply(series, t, n)
    index = {value: i for (i, value) in enumerate(series)}
    return [transformed[index[value]] for value in range(n)]

def lcm_list(series:list[int])->int:
    return reduce(lambda a,b: a*b//gcd(a,b), series)

def cycleStructure(permutation:list[int],n:int)->(int,list[int]):
    #calculates the lengths of the cycles of the permutation. Returns the order of the permutation and
    #a list with the lengths of the cycles
    visited = [False]*n
    cycles = []
    for i in range(n):
        if not visited[i]:
            current=permutation[i]
            length=1
            while current!=i:
                visited[current]=True
                current=permutation[current]
                length+=1
            cycles.append(length)
    return lcm_list(cycles), sorted(cycles)

def print_justified(series: list[int]) -> None:
    width = max(len(str(x)) for x in series)
    print("["+", ".join(f"{x:{width}d}" for x in series)+"]")

def proliferations(transformation:Transformation, series:list[int], t:int)->None:
    #first major program: takes a transformation with a transposition t and a series. Prints the original
    #and all its proliferations. Also prints the order and the structure of the permutation obtained
    print("Proliferations of", series, "using", transformation.name,"and a transposition of", t, "tone-fractions:")
    print_justified(series)
    n=len(series)
    permutation = proliferatingPermutation(transformation, series, t, n)
    current = [permutation[x] for x in series]
    while current != series:
        print_justified(current)
        current = [permutation[x] for x in current]
    (order,cycles)=cycleStructure(permutation,n) 
    print("Order:", order)
    print("Structure:", cycles)

def proliferations_data(transformation:Transformation, t:int, n:int, path:str)->None:
    #second major program: takes a transformation, a transposition t, a number of notes n and a path.
    #The program creates in this path a folder for the transformation, another folder inside for the
    #number of notes and 3 more subfolders inside it, called "CompleteList", "Data_Orders" and 
    #"Data_Structures". Finally, a txt file inside each of them distinguishing the transposition t.
    #The file in "CompleteList" shows every possible series starting with 0 and the number of proliferations 
    #that it produces. The file in "Data_Orders" shows how many series generate permutations of each possible
    #order, and the file in "Data_Structures" shows how many saries generate permutations of each possible 
    #structure. 
    base_path = os.path.join(path, transformation.name, f"Proliferations_{n}_notes")
    dirs = {
        "Data_Structures": os.path.join(base_path, "Data_Structures"),
        #"CompleteList": os.path.join(base_path, "CompleteList"),   #<------------ comment if you don't want the CompleteList
        "Data_Orders": os.path.join(base_path, "Data_Orders")
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)
    file_paths = {key: os.path.join(dirs[key], f"transposition{t}.txt") for key in dirs}
    occurrence_orders = defaultdict(int)
    occurrence_structures = defaultdict(int)
    with ExitStack() as stack:
        files = {key: stack.enter_context(open(file_paths[key], "w")) for key in file_paths}
        for seriesWithout0 in permutations(range(1, n)):
            completeSeries = (0,) + (seriesWithout0)
            permutation = proliferatingPermutation(transformation, completeSeries, t, n)
            order, structure = cycleStructure(permutation, n)
            #files["CompleteList"].write(f"{completeSeries} --> {order}\n")  #<------------ comment if you don't want the CompleteList
            occurrence_orders[order] += n #we sum n and not 1 since we are only considering series that start with 0, so each will appear n times more
            occurrence_structures[(order, tuple(structure))] += n
        for k, v in sorted(occurrence_orders.items()):
            files["Data_Orders"].write(f"{k}: {v}\n")
        for k, v in sorted(occurrence_structures.items()):
            files["Data_Structures"].write(f"{k}: {v}\n")