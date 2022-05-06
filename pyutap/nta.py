import errno, os
from pyutap import *

class TemplateHelper:
	def __init__(self, template):
		self.template = template
		self.isTA = template.isTA

		# TODO: Apparently references are passed, but check to be sure
		self.instances = stdlist_to_list(template.instances)
		self.states = stdlist_to_list(template.states)
		self.branchpoints = stdlist_to_list(template.branchpoints)
		self.edges = stdlist_to_list(template.edges)

	# TODO: addLocation etc. functions that original class has

	def getTemplateObject(self):
		return self.template

class NTAHelper:
	def __init__(self, path, name = "nta"):
		self.name = name
		self.ta_system = UTAP.TimedAutomataSystem()

		t = parseXMLFile(path, self.ta_system, True)
		if t != 0:
			raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

		self.declarations = self.ta_system.getGlobals() # Global declarations, maybe helper class?

		self.templates = []
		for template in self.ta_system.getTemplates():
			self.templates.append(TemplateHelper(template))
		
		self.queries = self.ta_system.getQueries() # Queries

	def writeToXML(self):
		t = writeXMLFile(self.name + ".xml", self.ta_system)
		if t != 0:
			raise Exception("Could not write to file.")

	def getSystemObject(self):
		return self.ta_system