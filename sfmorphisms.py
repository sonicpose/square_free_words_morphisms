import copy
import sfwords as sf
import itertools

# Takes a list of the form [[chunk0], [chunk1], [chunk2],...] and returns a function which maps letters to words.
def list_to_morphism(M):
    return lambda x: M[x]

# Applies a given morphism m to a list of letters
def apply_morphism(m, L):
    new = []
    for i in L:
        new += m(i)
    return new

# Returns all lists of length l containing integers from 0 to N-1
def allLists(l, N):
    return [list(x) for x in list(itertools.product(list(range(N)), repeat=l))]

# Returns all lists of length less than or equal to l containing integers from 0 to N-1
def allListsLessEqual(l,N):
    final = []
    for i in range(1, l+1):
        final += allLists(i,N)
    return final

# Returns all squarefree words of length less than or equal to L containing letters from 0 to N-1
def allSFWords(l, N):
    return [x for x in allListsLessEqual(l,N) if sf.isSquareFree(x)]

# Returns all morphisms on alphabet of size A where each letter is mapped to a chunk of no more than size M.
def allFiniteMorphismLists(A, M):
    return [list(x) for x in list(itertools.product(allSFWords(M, A), repeat=A+1))]

if __name__ == "__main__":
    pass