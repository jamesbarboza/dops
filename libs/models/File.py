from dops.libs.models.database.MySQLModel import MySQLModel

from os import listdir
from os.path import isdir, isfile

class File(MySQLModel):

	def __init__(self):
		self._table = "files"
		self._fillable = [ 'filename', 'category' ]
		super(File, self).__init__(self._table, self._fillable)

	#	Get all the files recursively in the training folder
	#	folders will be treated as categories
	#	eg: All the files in the news folder will belong to the category "news"
	def getTrainingFiles(self, system_path, p_category):
		files = []
		paths = [ file for file in listdir(system_path) ]
		for path in paths:
			category = p_category
			if isdir(system_path + "/" + path):
				category = category + "__" + path
				files = files + self.getTrainingFiles(system_path + "/" + path, category)
			else:		
				files.append((category, path))

		return files

	#	Get all files in a particular directory
	#	doesn't return the category
	def getFiles(self, system_path):
		files = []
		if isdir(system_path):
			paths = [ file for file in listdir(system_path)]
			for path in paths:
				path = system_path + "/" + path
				if isdir(path):
					files = files + self.getFiles(path)
				else:
					files.append(path)
		else:
			files.append(system_path)
		return files