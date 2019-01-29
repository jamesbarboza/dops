source_webrelief_table="""
	CREATE TABLE IF NOT EXISTS source_webrelief(
		id INT UNSIGNED NOT NULL,
		source_id INT UNSIGNED NOT NULL,
		title VARCHAR(195) NOT NULL,
		status VARCHAR(195),
		body TEXT,
		file_id INT,
		primary_country_id INT
		language_code VARCHAR(10),
		created_at VARCHAR(195),
		updated_at VARCHAR(195),
		deleted_at VARCHAR(195),
		FOREIGN KEY(source_id) references sources(id),
		FOREIGN KEY(file_id) references files(id),
		FOREIGN KEY(primary_country_id) references countries(id),
		PRIMARY KEY(id)
	)
"""



