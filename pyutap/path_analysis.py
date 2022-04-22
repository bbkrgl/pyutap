from pyutap import *

# Checks if given path exists
def path_exists(path): # Path -> edge list
        for i in range(1, len(path) - 1, 2):
                if not (path[i - 1].dst.uid == path[i].src.uid and path[i].dst.uid == path[i + 1].src.uid):
                        return False
        return True

# Returns the set of symbols in an expression
def get_symbols(expression):
        res = set()
        if (expression.getSize() == 0):
                if (expression.getKind() == Constants.IDENTIFIER):
                        res.add(expression.toString())
                        return res
                return res

        for i in range(expression.getSize()):
                res = res.union(get_symbols(expression[i]))

        return res

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