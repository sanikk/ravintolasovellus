Use this to output schema from postgres db
```bash
pg_dump --dbname=your_database_name --username=your_username --host=localhost --port=5432 --schema-only > schema.sql
```
