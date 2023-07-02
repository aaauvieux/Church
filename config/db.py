from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://mysql_adrian:123456@localhost:3306/church")

meta_data = MetaData()
