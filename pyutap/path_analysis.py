from pyutap import *
Constants = UTAP.Constants

# Checks if given path exists
def path_exists(path): # Path -> edge list
        for i in range(1, len(path) - 1, 2):
                if not (path[i - 1].dst.uid == path[i].src.uid and path[i].dst.uid == path[i + 1].src.uid):
                        return False
        return True

# Returns the set of clocks used in the given path
def find_used_clocks(path):
        res = set()
        for edge in path:
                if edge.guard.usesClock():
                        res = res.union(get_symbols(edge.guard))
                if edge.sync.usesClock():
                        res = res.union(get_symbols(edge.sync))
                if edge.src.invariant.usesClock(): # TODO: Check if symbols are not clocks
                        res = res.union(get_symbols(edge.src.invariant))

        return res
