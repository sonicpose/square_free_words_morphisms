import copy
import pickle as pkl

"""
All words are implemented as lists of nonnegative integers

"""

# Checks if a word is a square
def isSquare(l):
    return l[:len(l)//2] == l[len(l)//2:]

# Checks if a word is squareFree (SLOW)
def isSquareFree(l):
    for i in range(len(l)):
        for j in range(i+1,len(l)+1):
            if isSquare(l[i:j]):
                return False
    return True

# Checks if a word is squareFree (SLOW)
def findSquare(l):
    for i in range(len(l)):
        for j in range(i+1,len(l)+1):
            if isSquare(l[i:j]):
                return l[i:j]
    return None

# Checks if a word has no square which includes the final letter of the word (FAST, but doesn't find squares in middle of word)
def notSquareEnd(l):
    for i in range(len(l)):
        if isSquare(l[len(l)-i-1:]):
            return False
    return True

# Returns lexleast word with given prefix and size of extension
def lexLeast(prefix, size):
    L = prefix.copy()
    for i in range(size):
        for j in range(i):
            if notSquareEnd(L + [j]):
                L += [j]
                break
    return L

def cyclicLexLeast(prefix, size, mod):
    L = prefix.copy()
    for i in range(size):
        for j in range(mod):
            if notSquareEnd(L + [(L[-1] + j)%mod]):
                L += [(L[-1] + j)%mod]
                break
            if j == mod-1:
                return L
    return L

# Returns a list of all indices of occurences of item in L
def allIndices(item, L):
    return [i for i in range(len(L)) if L[i] == item]

def differences(L, n = 1):
    G = L.copy()
    for k in range(n):
        G = [G[i]-G[i-1] for i in range(1,len(G))]
    return G

def absDifferences(L, n = 1):
    G = L.copy()
    for k in range(n):
        G = [abs(G[i]-G[i-1]) for i in range(1,len(G))]
    return G

def generateNew(pref = [], size = 100):
    L = lexLeast(pref, size)
    dump(L)
    return L

def dump(data):
    with open("data.pkl", "wb") as f:
        pkl.dump(data, f)

def load():
    with open("data.pkl", "rb") as f:
        data = pkl.load(f)
    return data

def extend(n):
    L = load()
    L = lexLeast(L, n)
    dump(L)
    return L

def getRatios(L, n = 3):
    return [L.count(i)/L.count(i+1) for i in range(n)]

if __name__ == "__main__":
    pass
