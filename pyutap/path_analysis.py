from ortools.linear_solver import pywraplp
from pyutap import *
Constants = UTAP.Constants


# Checks if given path exists
def path_exists(path):  # Path -> edge list
    for i in range(1, len(path) - 1, 2):
        if not (path[i - 1].dst.uid == path[i].src.uid and path[i].dst.uid == path[i + 1].src.uid):
            return False
        return True


# Returns a path from state labels
def construct_path_from_labels(states, template):
    path = []
    for i in range(0, len(states) - 1):
        src = states[i]
        dst = states[i + 1]

        edge_found = False
        for edge in template.edges:
            if edge.src.uid.getName() == src and edge.dst.uid.getName() == dst:
                edge_found = True
                path.append(edge)
                break

        if not edge_found:
            return []
    return path


# Returns the set of clocks used in the given path
def find_used_clocks(path):
    res = set()
    for edge in path:
        if edge.guard.usesClock():
            res = res.union(get_symbols(edge.guard))
        if edge.sync.usesClock():
            res = res.union(get_symbols(edge.sync))
        if edge.assign.usesClock():
            res = res.union(get_symbols(edge.assign))
        if edge.src.invariant.usesClock(): # TODO: Check if symbols are not clocks
            res = res.union(get_symbols(edge.src.invariant))

    return res


def calculate_subrow(exp, i, cumul_var, var_count, v):
    sub_A = []
    sub_B = []
    if exp.getKind() == Constants.LE:
        a = [0 for _ in range(var_count)]
        a[cumul_var:i+1] = [1 for _ in range(i - cumul_var + 1)]
        sub_A.append(a)
        sub_B.append(v)
    elif exp.getKind() == Constants.GE:
        a = [0 for _ in range(var_count)]
        a[cumul_var:i+1] = [-1 for _ in range(i - cumul_var + 1)]
        sub_A.append(a)
        sub_B.append(-v)
    elif exp.getKind() == Constants.EQ:
        a = [0 for _ in range(var_count)]
        a[cumul_var:i+1] = [1 for _ in range(i - cumul_var + 1)]
        sub_A.append(a)
        sub_B.append(v)

        a = [0 for _ in range(var_count)]
        a[cumul_var:i+1] = [-1 for _ in range(i - cumul_var + 1)]
        sub_A.append(a)
        sub_B.append(-v)

    return sub_A, sub_B


def calculate_rows(exp, i, clocks, cumul_vars, cumul_vals, var_count, A, B):
    if exp[0].getKind() == Constants.IDENTIFIER:
        cumul_var = cumul_vars[clocks.index(exp[0].toString())]
        cumul_val = cumul_vals[str(exp[0].toString())]
        v = exp[1].getValue() - cumul_val
        sub_A, sub_B = calculate_subrow(exp, i, cumul_var, var_count, v)
        A += sub_A
        B += sub_B
    else:
        cumul_var1 = cumul_vars[clocks.index(exp[0][0].toString())]
        cumul_val1 = cumul_vals[str(exp[0][0].toString())]
        v1 = exp[1].getValue() - cumul_val1
        sub_A1, sub_B1 = calculate_subrow(exp, i, cumul_var1, var_count, v1)

        cumul_var2 = cumul_vars[clocks.index(exp[0][1].toString())]
        cumul_val2 = cumul_vals[str(exp[0][1].toString())]
        v2 = -cumul_val2
        sub_A2, sub_B2 = calculate_subrow(exp, i, cumul_var2, var_count, v2)

        if exp[0].getKind() == Constants.PLUS:
            for i in range(len(sub_A1)):
                temp_A = []
                temp_B = 0
                for j in range(len(sub_A1[i])):
                    temp_A.append(sub_A1[i][j] + sub_A2[i][j])
                    temp_B = sub_B1[i] + sub_B2[i]
                A.append(temp_A)
                B.append(temp_B)

        elif exp[0].getKind() == Constants.MINUS:
            for i in range(len(sub_A1)):
                temp_A = []
                temp_B = 0
                for j in range(len(sub_A1[i])):
                    temp_A.append(sub_A1[i][j] - sub_A2[i][j])
                    temp_B = sub_B1[i] - sub_B2[i]
                A.append(temp_A)
                B.append(temp_B)


def calculate_constraint_matrices(path, initial_clock_values=None):
    A = []
    B = []
    var_count = len(path)
    clocks = list(find_used_clocks(path))
    num_clocks = len(clocks)

    cumul_vars = [0] * num_clocks
    cumul_vals = {}
    if initial_clock_values is not None:
        cumul_vals = initial_clock_values
    else:
        cumul_vals = {clock: 0 for clock in clocks}

    for i, edge in enumerate(path):
        src_exp_list = get_expression_list(edge.src.invariant)
        for exp in src_exp_list:
            if exp.usesClock():
                calculate_rows(exp, i, clocks, cumul_vars, cumul_vals, var_count, A, B)

        guard_exp_list = get_expression_list(edge.guard)
        for exp in guard_exp_list:
            if exp.usesClock():
                calculate_rows(exp, i, clocks, cumul_vars, cumul_vals, var_count, A, B)

        assign_exp_list = get_expression_list(edge.assign)
        for exp in assign_exp_list:
            if exp.usesClock():
                cumul_vars[clocks.index(exp[0].toString())] = i + 1
                cumul_vals[str(exp[0].toString())] = exp[1].getValue()

    return A, B


def is_path_realizable(path, initial_clock_vals=None, print_matrices=False, print_solver=False):
    A, B = calculate_constraint_matrices(path, initial_clock_vals)
    if print_matrices:
        for i in range(len(A)):
            print(A[i], "<=", B[i])

    var_count = len(path)

    solver = pywraplp.Solver("", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    c = {}
    for j in range(var_count):
        c[j] = solver.NumVar(0, solver.infinity(), "x[%s]" % j)
    for i in range(len(A)):
        constraint = solver.RowConstraint(-solver.infinity(), B[i], "")
        for j in range(var_count):
            constraint.SetCoefficient(c[j], A[i][j])

    if print_solver:
        print(solver.ExportModelAsLpFormat(False))

    status = solver.Solve()
    delays = []
    if status == solver.OPTIMAL:
        for i in range(var_count):
            delays.append(c[i].solution_value())
        return True, delays

    if status == solver.INFEASIBLE:
        return False, []
