from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DBHandler:

    def __init__(self, destination=":memory:"):
        self.engine = create_engine(f"sqlite:///{destination}")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def add(self, corpus):
        with open("corpuses.csv", 'a+') as f:
            f.write(corpus.replace('\n', ' '))
        new_corpus = Corpus(corpus=corpus)
        self.session.add(new_corpus)
        self.session.commit()


class Corpus(Base):
    __tablename__ = 'corpuses'

    id = Column(Integer, primary_key=True)
    corpus = Column(String)

    def __repr__(self):
        return f"<Corpus(corpus='{self.corpus}')>"

