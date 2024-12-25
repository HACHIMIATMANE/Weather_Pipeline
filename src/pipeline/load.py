import sqlite3

def load_data(transformed_data, db_path_prefix='data'):
    db_name = f"{db_path_prefix}_weather.db"
    table_name = "Weather_Table"
    conn = sqlite3.connect(db_name)
    transformed_data.to_sql(table_name, conn, if_exists='replace', index=True)
    conn.close()