#TODO: Check dependencies

import cppyy

cppyy.add_library_path("/usr/lib")
cppyy.add_library_path("/usr/local/lib")
cppyy.add_include_path("/usr/local/include")
cppyy.add_include_path("/usr/include/libxml2")

cppyy.load_library("libutap")

# TODO: Filter out unused ones, maybe include from a different file
cppyy.include("utap/abstractbuilder.h")
cppyy.include("utap/builder.h")
cppyy.include("utap/common.h")
cppyy.include("utap/expressionbuilder.h")
cppyy.include("utap/expression.h")
cppyy.include("utap/position.h")
cppyy.include("utap/prettyprinter.h")
cppyy.include("utap/signalflow.h")
cppyy.include("utap/statementbuilder.h")
cppyy.include("utap/statement.h")
cppyy.include("utap/symbols.h")
cppyy.include("utap/systembuilder.h")
cppyy.include("utap/system.h")
cppyy.include("utap/typechecker.h")
cppyy.include("utap/type.h")
cppyy.include("utap/utap.h")
cppyy.include("utap/xmlwriter.h")

from cppyy.gbl import UTAP

from cppyy.gbl import parseXTA
from cppyy.gbl import parseXMLBuffer
from cppyy.gbl import parseXMLFile
from cppyy.gbl import parseExpression
from cppyy.gbl import writeXMLFile

# TODO: Add useful functions
# TODO: Additional pythonizations

# TODO: Implement compute clock constraints
#def get_clocks(system, path):
#    res = []
#    for element in path:
#        constraints = get_constraints(system) # get constraints
#        for c in constraints:
#            pass # TODO: Check if constraint

#def compute_clock_constraints(ta_system):
#    pass

# TODO: Is path realizable
# TODO: Is there a parameter valuation to make path realizable