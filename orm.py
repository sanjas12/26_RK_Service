from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Создаем соединение с базой данных (в данном случае SQLite)
engine = create_engine('sqlite:///database/list.db', echo=True)

# Создаем базовый класс для объявления моделей
Base = declarative_base()

# Определяем модель таблицы modules
class Module(Base):
    __tablename__ = 'modules'
    # __table_args__ = {'mysql_engine':'InnoDB'}

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    type = Column('type_module', String(100), unique=False)
    ser = Column(String(100), unique=True)
    mac = Column(String(100), unique=True)

# Создаем таблицу в базе данных
Base.metadata.create_all(engine)

class DbSession:
    def __init__(self):
        pass
    
    def __enter__(self)-> None:
        self.connection = engine.connect()
        self.session = scoped_session(sessionmaker(
                                        autocommit=False,
                                        autoflush=False,
                                        bind=engine)
                                        )
        return self.session

    def __exit__(self, exc_type, value, traceback):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.connection.close()

    def __repr__(self):
            return f"<News(id={self.id}, name={self.name}, ser={self.ser}, mac={self.mac})>"

if __name__ == "__main__":
    with DbSession() as db_session:
        desired_mac = '70-B3-D5-22-34-A0'

        # Запрос к базе данных для проверки существования mac в таблице modules
        # print(f'{db_session.query(Module).filter_by(mac)}')
        # existing_module = db_session.query(Module).filter_by(mac=desired_mac).first()
        # print(db_session.query(Module).filter_by(type).first())

        if existing_module:
            print(f"Значение MAC '{desired_mac}' уже существует в таблице modules.")
        else:
            print(f"Значение MAC '{desired_mac}' не существует в таблице modules и может быть вставлено без нарушения уникального ограничения.")




        # mac_l = ['70-B3-D5-22-34-A0']

        # for mac in mac_l:
        #     print(db_session.query(Module).filter_by(mac=mac))

            # print(existing_module)
            # new_entry = Module(type="NLS-16DI-Ethernet",
            #                     ser='123',
            #                     mac='70-B3-D5-22-34-A0') 
            
            # new_entry_2 = Module(type="NLS-8R-Ethernet",
            #                     ser='345',
            #                     mac='70-B3-D5-22-35-63') 

            # db_session.add(new_entry)
            # db_session.add(new_entry_2)