import mysql.connector
import dops.project_config as config

class MySQLModel:
	def __init__(self, table, fillable):
		self._table = table
		self._fillable = fillable
		self._timestamps = [ 'created_at', 'updated_at', 'deleted_at' ]
		self.connection = mysql.connector.connect(
			host=config.__mysql_host__,
			user=config.__mysql_username__,
			passwd=config.__mysql_password__,
			database=config.__mysql_database__
		)
		self.cursor = self.connection.cursor()
		#self._id = self.getId()

	#def __del__():

	def find(self, id):
		query = "SELECT * FROM " + self._table + " WHERE id=" + str(id) + ";"
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def findAll(self):
		query = "SELECT * FROM " + self._table + ";"
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def where(self, column, value):
		query = "SELECT * FROM " + self._table + " WHERE " + column +"='" + str(value) + "';"
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def insert(self, values):
		columns = self._fillable + self._timestamps
		columns_str = "".join(str(i)+"," for i in columns)
		columns_str = columns_str[0:len(columns_str)-1]
		values_str = "".join("'"+str(i)+"'," for i in values)
		values_str = values_str[0:len(values_str)-1]
		query = "INSERT INTO " + self._table + "(" + columns_str + ") values( " + values_str + ");"
		self.cursor.execute(query)
		self.connection.commit()
		return self.cursor.lastrowid

	def update(self, id, commitolumn, value):
		query = "UPDATE " + self._table + " SET " + column + "='" + str(value) + "' where id=" + str(id) + ";"
		self.cursor.execute(query)
		self.connection.commit()
		return self.cursor.lastrowid

	#def getId(self):
	#	query = "SELECT  LAST_INSERT_ID() AS id"
	#	self.cursor.execute(query)
	#	id = self.cursor.fetchall()
	#	return (id[0][0]+1)