import sqlalchemy
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from backend.config import settings

Base = declarative_base()

class QuestionAndResponse(Base):
    __tablename__ = "question_and_responses"
    question_id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    date_of_add = Column(DateTime, default=datetime.now())
    document = Column(String, nullable=True)
    page = Column(Integer, nullable=True)
    author = Column(String)
    subject = Column(String, nullable=True)

class QaADatabase:
    def __init__(self):
        # settings.DATABASE_URL deve ser uma string de conexão SQLAlchemy, ex: "sqlite:///./test.db"

        self.engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_question(self, question : str, 
                     answer : str, 
                     document : str = None, 
                     page : int = None, 
                     author : str = None, 
                     subject : str = None, 
                     date_of_add : datetime = None):
        session = self.Session()
        try:
            q = QuestionAndResponse(
                question=question,
                answer=answer,
                date_of_add=date_of_add or datetime.utcnow(),
                document=document,
                page=page,
                author=author,
                subject=subject
            )
            session.add(q)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


    def get_all_questions_from_user(self, user_name: str):
        session = self.Session()
        try:
            return session.query(QuestionAndResponse).filter_by(author=user_name).all()
        finally:
            session.close()

    def get_question(self, question):
        session = self.Session()
        try:
            return session.query(QuestionAndResponse).filter_by(question=question).first()
        finally:
            session.close()

    def get_all_questions(self):
        session = self.Session()
        try:
            return session.query(QuestionAndResponse).all()
        finally:
            session.close()

    def delete_question(self, question):
        session = self.Session()
        try:
            q = session.query(QuestionAndResponse).filter_by(question=question).first()
            if q:
                session.delete(q)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
