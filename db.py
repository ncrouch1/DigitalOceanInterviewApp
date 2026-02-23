from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    score = Column(Integer, nullable=False)

class DatabaseWrapper():
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        User.metadata.create_all(self.engine)

    def get_connection(self):
        return self.engine.connect()

    def create_user(self, username):
        new_user_id = uuid.uuid4()
        with self.get_connection() as connection:
            new_user = User(username=username, score=0)
            connection.execute(User.__table__.insert(), [
                {"id": new_user_id, "username": new_user.username, "score": 0}
            ])
            return new_user_id

    def update_score(self, user_id, score):
        with self.get_connection() as connection:
            connection.execute(
                User.__table__.update().where(User.id == user_id).values(score=score)
            )

    def get_score(self, user_id):
        with self.get_connection() as connection:
            result = connection.execute(
                User.__table__.select().where(User.id == user_id)
            ).fetchone()
            return result.score if result else None

    def get_top_x_scores(self, x):
        with self.get_connection() as connection:
            result = connection.execute(
                User.__table__.select().order_by(User.score.desc()).limit(x)
            ).fetchall()
            return [{"username": row.username, "score": row.score} for row in result]

    def get_user_with_neighbors(self, user_id: uuid.UUID):
        with self.get_connection() as conn:
            # Fetch target user
            target_row = conn.execute(
                User.__table__.select().where(User.id == user_id)
            ).mappings().fetchone()

            if not target_row:
                return {"above": None, "target": None, "below": None}

            target = _row_to_dict(target_row)
            score = target_row["score"]

            # Nearest user with a higher score (better rank)
            above_row = conn.execute(
                User.__table__.select().where(User.score > score).order_by(User.score.asc(), User.id.asc()).limit(1)
            ).mappings().fetchone()

            # Nearest user with a lower score (worse rank)
            below_row = conn.execute(
                User.__table__.select().where(User.score < score).order_by(User.score.desc(), User.id.asc()).limit(1)
            ).mappings().fetchone() 

            return {
                "above": _row_to_dict(above_row) if above_row else None,
                "target": target,
                "below": _row_to_dict(below_row) if below_row else None,
            }