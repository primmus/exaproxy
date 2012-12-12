# encoding: utf-8
"""
http.py

Created by Thomas Mangin on 2011-12-02.
Copyright (c) 2011 Exa Networks. All rights reserved.
"""

#import re
#reg=re.compile('(\w+)[:=] ?"?(\w+)"?')
#reg=re.compile('(\w+)[:=] ?"?([^" ,]+)"?')
#dict(reg.findall(headers))


class Headers (object):
	def __init__ (self,separator):
		self._order = []
		self._data = {}
		self.separator = separator

	def get (self,key,default):
		return self._data.get(key,default)

	def set (self,key,value):
		if key not in self._order:
			self._order.append(key)

		self._data[key] = [value]
		return self

	def replace (self,key,value):
		self._data[key] = [value]

	def default (self,key,value):
		if key not in self._data:
			self._data[key] = [value]

	def extend (self,key,value):
		if key in self._order:
			self._data[key].append(value)
			return self
		self._order.append(key)
		self._data[key] = [value]
		return self

	def pop (self, key, default=None):
		if key in self._data:
			value = self._data.pop(key)
			self._order.remove(key)
			return value
		else:
			return default

	def parse (self, lines):
		if lines and lines[0].isspace():
			raise ValueError('Malformed headers, headers starts with a white space')

		try:
			key = ''

			for line in lines.split('\n'):
				line = line.strip('\r')
				if not line: break

				if line[0].isspace():
					# ValueError if key is not already there
					# IndexError the list is empty
					self.extend(key,line)
					continue

				# KeyError if split does not return two elements
				key, value = line.split(':', 1)
				key = key.strip().lower()
				self.set(key,line)
		except (KeyError,TypeError,IndexError):
			raise ValueError('Malformed headers (line : %s) headers %s' % (line,lines.replace('\n','\\n').replace('\r','\\r')))

		# we got a line starting with a :
		if '' in self._data:
			raise ValueError ('Malformed headers, line starts with colon (:)')
		
		return self

	def __str__ (self):
		return self.separator.join([self.separator.join(self._data[key]) for key in self._order])


