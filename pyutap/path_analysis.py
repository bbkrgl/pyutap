from pyutap import *
from ortools.linear_solver import pywraplp
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
        if edge.src.invariant.usesClock(): # TODO: Check if symbols are not clocks
            res = res.union(get_symbols(edge.src.invariant))

    return res


def calculate_constraint_matrices(path): # TODO: Initial clock vals, parametric clock vals etc.
	A = []
	B = []
	var_count = len(path)
	clocks = list(find_used_clocks(path))
	num_clocks = len(clocks)

	cumul_vars = [0] * num_clocks
	for i, edge in enumerate(path):
		src_exp_list = get_expression_list(edge.src.invariant)
		for exp in src_exp_list:
			if exp.usesClock():
				cumul_var = cumul_vars[clocks.index(exp[0].toString())]
				a = [0 for _ in range(var_count)]
				a[cumul_var:i+1] = [1 for _ in range(i - cumul_var + 1)]
				A.append(a)
				B.append(exp[1].getValue())

		guard_exp_list = get_expression_list(edge.guard)
		for exp in guard_exp_list:
			if exp.usesClock():
				cumul_var = cumul_vars[clocks.index(exp[0].toString())]
				a = [0 for _ in range(var_count)]
				a[cumul_var:i+1] = [1 for _ in range(i - cumul_var + 1)]
				A.append(a)
				B.append(exp[1].getValue())

		assign_exp_list = get_expression_list(edge.assign)
		for exp in assign_exp_list:
			if exp.usesClock():
				cumul_vars[clocks.index(exp[0].toString())] = i

	return A, B


def is_path_realizable(path, initial_clock_vals=None):
	A, B = calculate_constraint_matrices(path)
	var_count = len(path)

	solver = pywraplp.Solver("", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
	c = {}
	for j in range(var_count):
		c[j] = solver.NumVar(0, solver.infinity(), "x[%s]" % j)
	for i in range(len(A)):
		constraint = solver.RowConstraint(-solver.infinity(), B[i], "")
	for j in range(var_count):
		constraint.SetCoefficient(c[j], A[i][j])

	status = solver.Solve()
	delays = []
	if status == solver.OPTIMAL:
		for i in range(var_count):
			delays.append(c[i].solution_value())
		return True, delays
	
	if status == solver.INFEASIBLE:
		return False, []
