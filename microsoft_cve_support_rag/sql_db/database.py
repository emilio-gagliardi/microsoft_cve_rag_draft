# import psycopg2

# # Connect to the server instance
# conn = psycopg2.connect(
#     dbname='',  # Connect to the default database
#     user='username',
#     password='password',
#     host='localhost',
#     port='5432'
# )

# # Create a cursor object
# cur = conn.cursor()

# # Switch to a specific database
# cur.execute("SELECT pg_catalog.set_config('search_path', '', false);")
# cur.execute("SELECT pg_catalog.set_config('search_path', 'mydatabase', false);")

# # Now you can execute queries on 'mydatabase'
# cur.execute("SELECT * FROM my_table;")
# rows = cur.fetchall()

# for row in rows:
#     print(row)

# # Close the cursor and connection
# cur.close()
# conn.close()
