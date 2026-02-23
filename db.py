from sqlalchemy import create_engine
from sqlalchemy import declarative_base

Base = declarative_base()

classs User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    score = Column(Integer, nullable=False)

class DatabaseWrapper()
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        User.metadata.create_all(self.engine)

    def get_connection(self):
        return self.engine.connect()

    