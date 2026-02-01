import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

#DEFAULT_DATABASE_URL = "sqlite:///project.db"
DEFAULT_DATABASE_URL="cockroachdb://venky:GlPaYWo1DAuDf76pMgUlkw@opal-ent-20761.j77.aws-ap-south-1.cockroachlabs.cloud:26257/projectdb?sslmode=require"

DATABASE_URL = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)

    assignments = relationship(
        "Assignment",
        back_populates="student",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name, "status": self.status}

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String, nullable=False)
    status = Column(String, nullable=False)
    student_id = Column(
        Integer,
        ForeignKey("student.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    student = relationship("Student", back_populates="assignments")

    def to_dict(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "student": self.student_id,
            "status": self.status,
        }

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("Tables created")