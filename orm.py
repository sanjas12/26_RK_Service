from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Создаем соединение с базой данных (в данном случае SQLite)
engine = create_engine('sqlite:///database/list.db', echo=True)

# Создаем базовый класс для объявления моделей
Base = declarative_base()


class Module(Base):
    __tablename__ = 'modules'
    # __table_args__ = {'mysql_engine':'InnoDB'}

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(100), unique=False)
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
        # Perform database operations using db_session
        new_entry = Module(name="NLS-16DI-Ethernet",
                            ser='123',
                            mac='70-B3-D5-22-34-A0') 
        
        new_entry_2 = Module(name="NLS-8R-Ethernet",
                            ser='345',
                            mac='70-B3-D5-22-35-63') 

        db_session.add(new_entry)
        db_session.add(new_entry_2)