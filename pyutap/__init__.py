#TODO: Check dependencies
import os
from pathlib import Path
import cppyy

cppyy.add_library_path("/usr/lib")
cppyy.add_library_path("/usr/local/lib")
cppyy.add_include_path("/usr/local/include")
cppyy.add_include_path("/usr/include/libxml2")

cppyy.load_library("libutap")

src_dir = Path(__file__).parent.parent
cppyy.load_reflection_info(os.path.join(src_dir, "rfiles/utap_rflx.so"))
cppyy.add_autoload_map(os.path.join(src_dir, "rfiles/utap.rootmap"))

cppyy.include("utap/signalflow.h")
cppyy.include("utap/utap.h")


from cppyy.gbl import UTAP

from cppyy.gbl import parseXTA
from cppyy.gbl import parseXMLBuffer
from cppyy.gbl import parseXMLFile
from cppyy.gbl import parseExpression
from cppyy.gbl import writeXMLFile

# TODO: Add useful functions, additional pythonizations

# Import functions from a different file?
# Convert std::list, std::deque or other non-indexable types to python list
def stdlist_to_list(stdlist):
	return [x for x in stdlist]


# Returns the set of symbols in an expression
def get_symbols(expression):
        res = set()
        if (expression.getSize() == 0):
                if (expression.getKind() == UTAP.Constants.IDENTIFIER):
                        res.add(expression.toString())
                        return res
                return res

        for i in range(expression.getSize()):
                res = res.union(get_symbols(expression[i]))

        return res


# Change the value that the given expression has at a given index
def change_expression_value(expression, newval, index=1):
        expression[index] = expression[index].createConstant(newval, expression.getPosition())

# TODO: Implement compute clock constraints
# TODO: Is path realizable
# TODO: Is there a parameter valuation to make path realizable

from . import verify
from . import path_analysis
