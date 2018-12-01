import os
from os.path import isfile
import json

import project_config as config
from libs.models.File import File


class RawFile(File):
	def __init__(self):
		super(RawFile, self).__init__()
		self._file_path = ""
		self._file_extension = ""
		self._file_content = {}

	#	use the function to set the file path
	#	works like the main function to load the document into the memory
	def load(self, path):
		self._file_path = path
		self._getFileType()
		self._loadFileContent()

	#	get the file extension
	#	used to determine the type of conversion on the basis of the extension
	def _getFileType(self):
		self._filename, self._file_extension = os.path.splitext(self._file_path)

	#	convert the file to readable text
	#	use conversion for different types of files
	#	eg: txt to binary
	#	eg: pdf to string to binary
	def _loadFileContent(self):
		if(self._file_extension == ".txt"):
			file = open(self._file_path, "rb")
			self._file_content['content'] = { 'content': file.read() }
			file.close()

		elif(self._file_extension == ".json"):
			file = open(self._file_path, "r")
			self._file_content = json.load(file)
			file.close()

	#	read the file contents
	def read(self):
		return self._file_content