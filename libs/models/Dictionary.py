from libs.models.database.MySQLModel import MySQLModel

class Dictionary(MySQLModel):

	def __init__(self):
		self._table = "dictionaries"
		self._fillable = [ 'category' ]
		super(Dictionary, self).__init__(self._table, self._fillable)
