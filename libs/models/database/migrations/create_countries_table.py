sqlcommand="""
	CREATE TABLE IF NOT EXISTS countries(
		id INT UNSIGNED NOT NULL,
		source_id INT UNSIGNED NOT NULL,
		country VARCHAR(195),
		created_at VARCHAR(195),
		updated_at VARCHAR(195),
		deleted_at VARCHAR(195),
		PRIMARY KEY(id)
	)
"""

import mysql.connector
connection = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="",
			database="dops"
		)
cursor = connection.cursor()
cursor.execute(sqlcommand);