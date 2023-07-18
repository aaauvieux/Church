from ast import Name
from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv

load_dotenv()
server = os.getenv('SERVER')
server_port = os.getenv('SERVER_PORT')
db = os.getenv('DB')
user_db = os.getenv('USER_DB')
password_db = os.getenv('PASSWORD_DB')

print(server)
print(type(server_port))
print(db)
print(user_db)
print(password_db)

engine = create_engine("mysql+pymysql://4vdsco0al8bl02g10m90:pscale_pw_4SRWPf7EZpKMOwenhVMipEnMFJTcvoXAaOAB5BOBDLh@aws.connect.psdb.cloud:3306/church")
#engine = create_engine("mysql+pymysql://sql7631486:ra5aZaGJBR@sql7.freemysqlhosting.net:3306/sql7631486")
#engine = create_engine(f"mysql+pymysql://{user_db}:{password_db}@{server}:{server_port}/{db}")
#engine = create_engine("mysql+pymysql://mysql_adrian:123456@localhost:3306/church")

meta_data = MetaData()
