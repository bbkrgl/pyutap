from pyutap import *
from ortools.linear_solver import pywraplp
Constants = UTAP.Constants


# Checks if given path exists
def path_exists(path):  # Path -> edge list
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


def is_path_realizable(path, initial_clock_vals=None):
    A = []
    B = []

    clocks = find_used_clocks(path)
    clocks_to_delay = dict()

    delay_var_count = len(path)
    var_count = delay_var_count
    delay_var_offset = 0

    if initial_clock_vals != None:
        # TODO: Check
        initial_var_count = len(clocks)
        var_count = delay_var_count + initial_var_count
        delay_var_offset = initial_var_count

        for i, c in enumerate(clocks):
            a = [[0] * var_count]
            b = [0]
            a[0][i] = -1
            A.append(a[0])
            B.append(b[0])
            try:
                clocks_to_delay[c] = [i, delay_var_offset]
                icv_c = initial_clock_vals[c]
                b[0] = icv_c
                b.append(-icv_c)
                a.append([-var for var in a[0]])
                A.append(a[1])
                B.append(b[1])
            except:
                pass

        for i, c in enumerate(clocks):
            clocks_to_delay[c] = [i, delay_var_offset]

    else:
        for c in clocks:
            clocks_to_delay[c] = [0]
  
    for transition in path:
        src = transition.src
        if src.invariant.getSize() > 0:
            for j in range(src.invariant.getSize()):
                if not src.invariant[j].usesClock():
                    continue
                # TODO: Compute constraints

        if transition.guard.getSize() > 0:
            for j in range(transition.guard.getSize()):
                if not transition.guard[j].usesClock():
                    continue
                # TODO: Compute constraints


        # TODO: Handle reset-update

        dst = transition.dst
        if dst.invariant.getSize() > 0:
            for j in range(dst.invariant.getSize()):
                if not dst.invariant[j].usesClock():
                    continue
                # TODO: Compute constraints

        # TODO: Delay etc.
        # TODO: Solve LP
