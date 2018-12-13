sources_table="""
	CREATE TABLE IF NOT EXISTS sources(
		id INT UNSIGNED NOT NULL,
		source_id INT UNSIGNED NOT NULL,
		name VARCHAR(195) NOT NULL,
		homepage VARCHAR(195),
		type VARCHAR(195),
		created_at VARCHAR(195),
		updated_at VARCHAR(195),
		deleted_at VARCHAR(195),
		PRIMARY KEY(id)
	)
"""