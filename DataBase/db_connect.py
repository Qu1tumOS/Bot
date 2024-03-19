from sqlalchemy import create_engine, Column, Integer, String, BigInteger, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from environs import Env

env = Env()
env.read_env()

print('Подключение к базе данных...')
engine = create_engine(url = f'''postgresql+psycopg2://{env('DB_USER')}:{env('DB_PASS')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}''',
                       echo=False)

Session = sessionmaker(bind=engine,
                       expire_on_commit=False)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'nnst_users'

    tg_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    user_name = Column(String)
    collage = Column(String(5), default=None)
    group = Column(String, default=None)
    subgroup = Column(Integer, default=None)
    # date_of_registration = Column()
    # subscription_activation = Column()
    # date_subscription_activation = Column()

class Lesson(Base):
    __tablename__ = 'lessons_on_groups'

    day = Column(String, primary_key=True)
    lessons = Column(JSON)



Base.metadata.create_all(engine)

DB_NAME_LIST = {'User':'nnst_users',
                'Lesson':'lessons_on_groups'}
