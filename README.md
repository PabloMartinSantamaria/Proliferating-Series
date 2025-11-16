# Jean Barraqué proliferating series studied in terms of permutations: auxiliar code

This repository is subordinate to a paper published in [...], available in the link below:

# Abstract of the paper:

Barraqué's proliferating series give an interesting turn on the concept of classic serialism 
by creating a new invariant when it comes to constructing the series: rather than the intervals 
between consecutive notes, what remains unaltered during the construction of the proliferations 
of the given base series is the permutation of the notes which happens between two consecutive 
series, that is to say, the transformation of the order of the notes in the series. This presents 
new possibilities for composers interested in the serial method, given the fact that the variety 
of intervalsobtained by this method is far greater than that of classic serialism.
In this manuscript, we will study some unexplored possibilities that the proliferating series
offer from a mathematical view, which will allow composers to gain much more familiarity with 
them and potentially result in the creation of pieces that take serialism to the next level.


# Utility of this repository:

The code available here is a tool to create and manipulate proliferating series. We can find two main code files: 
ProliferatingSeries_seriesManipulation and ProliferatingSeries_possiblePermutations, both of which have a .py version 
with the raw code and a .ipynb with the code and some examples already executed in notebook format. 

The first file, ProliferatingSeries_seriesManipulation, is the one that can be more useful for the average reader, including a composer who wants 
to use proliferating series in a piece. This code allows us to input a series of our choice, a transformation (P,I,R,RI) and a transposition, and calculate all the 
proliferations that this combination generates, that is, all the new series that we can use. The series are represented as lists of integer numbers, relating the
numbers with the notes (or the elements that we are serializing) in ascending order with respect to the tone-fractions. An usual correspondence would be
C --> 0, Db --> 1, D --> 2, Eb --> 3...
And after obtaining all the proliferations in number terms, we only have to apply the inverse correspondence to get our series.
In this same file, there is also a program that is given a number of notes, a 
transformation and a transposition, and calculates the proliferations of every possible 
series of that number of notes, organizing all the information in a collection of files.

The second file, ProliferatingSeries_possiblePermutations, brings a more theoretical information. 
This program uses the results obtained in the article to calculate
every possible permutation obtainable by the various methods of proliferating series, yielding as the 
output a list of all the possible cycle structures, paired
with their order. In particular, it has a program for RI, other for R with a coprime transposition
and a final one for the general case of R. The former two programs are quite efficient for reasonable numbers 
of notes, but, since the final case of retrogradation
with an arbitrary transposition does not have a compact result that caracterizes the possible series, 
the program utilizes directly the recursive process, which
is very unefficient. The cases P and I are not included for their simplicity. 

Finally, there is a folder called Proliferations_data. This folder is the result of executing the program mentioned in 
the first file for every transformation, every number of notes up to 12 and every possible transposition for each 
number of notes, organizing the information of every proliferating series. In this folder we can find subfolders called 
P,I,R,RI, for each transformation. Each subfolder has more subfolders for every number of notes up to 12, and each of those 
has two subfolders, one for the information about cycle structures of permutations and another one for the information about 
number of proliferations obtained (the second one is actually redundant, since we can obtain the order of a permutation 
given the lengths of its cycles). Finally, in each of those two folders, we can find .txt files for each transposition 
of that number of notes, each containing all the possible cycle structures/number of proliferations, and how many series 
produce each of those. For example, in Proliferations_data/RI/Proliferations_03_notes/Data_Structures/transposition0.txt we 
will find that, in the context of RI with 4 notes and 0 transpositions, there are 8 series that proliferate into a permutation
of structure [1,1,2] (which has order 2, meaning just 2 proliferations), and 16 series that proliferate 
into a permutation of structure [4] (which has order 4).







