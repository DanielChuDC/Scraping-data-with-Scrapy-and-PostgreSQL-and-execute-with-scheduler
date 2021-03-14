import pandas as pd
from sqlalchemy import create_engine

DATABASE = {
    "host": 'localhost',
    "port": '5432',
    "username": 'postgres',
    "password": 'weakpassword',
    "database": 'tutorialdb',
}
db_string = f"postgres://{DATABASE['username']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"

engine = create_engine(db_string)

df = pd.read_sql_query('SELECT * FROM mystocklists',
                       con=engine)
print(df.to_string())