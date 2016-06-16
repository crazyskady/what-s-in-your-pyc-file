'''
Parse pyc file.
Author: crazy skady
'''
#!/usr/bin/python

import struct
from time import ctime
import marshal
import dis

class pycParser:
	def __init__(self, filename):
		self.filename       = filename
		self.magic          = 0
		self.createdtime    = 0
		self.pycCodeObjects = []

	def parse(self):
		fn = open(self.filename, 'rb')
		pycContext = fn.read()
		fn.close()

		# pyc is little endian
		magicAndTime       = struct.unpack('<2HI', pycContext[0:8])
		self.magic         = magicAndTime[0]
		self.createdtime   = magicAndTime[2]
		rootCodeObject     = marshal.loads(pycContext[8:])
		self.loopAddCodeObject(rootCodeObject)
		self.pycCodeObjects.reverse()

	def toFile(self):
		pass

	def loopAddCodeObject(self, pyCO):
		for idx, item in enumerate(pyCO.co_consts):
			if type(item) == type(pyCO):
				self.loopAddCodeObject(item)

		self.pycCodeObjects.append(pyCO)

	def showPyCodeObject(self, pyCO):
		print '-'*60
		print 'Arg counts        :', pyCO.co_argcount
		print 'Number of locals  :', pyCO.co_nlocals
		print 'Stack size        :', pyCO.co_stacksize
		print 'Flag (N/A)        :', pyCO.co_flags
		print 'Code Block        :'
		print '>'*40
		print dis.dis(pyCO.co_code)
		print '<'*40
		print 'Consts            :', pyCO.co_consts
		print 'Names             :', pyCO.co_names
		print 'Var names(Local)  :', pyCO.co_varnames
		print 'Free vars         :', pyCO.co_freevars
		print 'Cell vars         :', pyCO.co_cellvars
		print 'File name         :', pyCO.co_filename
		print 'Code Block name   :', pyCO.co_name
		print 'First line number :', pyCO.co_firstlineno
		print 'lnotab:           :'
		print '>'*40
		print dis.dis(pyCO.co_lnotab)
		print '<'*40
		print '-'*60

	def show(self):
		print 'Python magic word :', self.magic
		print 'Pyc created time  :', ctime(self.createdtime)

		for idx, item in enumerate(self.pycCodeObjects):
			self.showPyCodeObject(item)

if __name__ == '__main__':
	pInstance = pycParser('demo.pyc')
	pInstance.parse()
	pInstance.show()
