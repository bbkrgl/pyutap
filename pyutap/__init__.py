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

from . import verify
from . import path_analysis

# TODO: Add useful functions, additional pythonizations

# Import functions from a different file?
# Convert std::list, std::deque or other non-indexable types to python list
def stdlist_to_list(stdlist):
	return [x for x in stdlist]

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

# Change the value that the given expression has at a given index
def change_expression_value(expression, newval, index=0):
        expression[index] = expression[index].createConstant(newval, expression.getPosition())

# TODO: Implement compute clock constraints
# TODO: Is path realizable
# TODO: Is there a parameter valuation to make path realizable