import sys
sys.path.append("../..")
import project_config as config

sqlcommand="""
	CREATE TABLE IF NOT EXISTS files(
		id INT UNSIGNED AUTO_INCREMENT NOT NULL,
		filename VARCHAR(195) NOT NULL,
		category VARCHAR(195),
		created_at VARCHAR(195),
		updated_at VARCHAR(195),
		deleted_at VARCHAR(195),
		PRIMARY KEY(id)
	)
"""

import mysql.connector
connection = mysql.connector.connect(
			host=config.__mysql_host__,
			user=config.__mysql_username__,
			passwd=config.__mysql_password__,
			database=config.__mysql_database__
		)
cursor = connection.cursor()
cursor.execute(sqlcommand);