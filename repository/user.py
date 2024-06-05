from datetime import datetime

from sqlalchemy.orm import Session

from database.base import session
from database.user import User
from schema.user import UserInDB, UserOutput


class UserRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[UserOutput] | None:
        users_db = self.db.query(User).all()
        users = [UserOutput(**user.__dict__) for user in users_db]
        return users

    def get_by_id(self, id: int) -> UserOutput | None:
        user_db = self.db.query(User).filter(User.id == id).first()
        if user_db:
            user = UserOutput(**user_db.__dict__)
            return user
        return None

    def get_by_username(self, username: str) -> UserOutput | None:
        user_db = self.db.query(User).filter(User.username == username).first()
        if user_db:
            user = UserOutput(**user_db.__dict__)
            return user
        return None

    def get_by_email(self, email: str) -> UserOutput | None:
        user_db = self.db.query(User).filter(User.email == email).first()
        if user_db:
            user = UserOutput(**user_db.__dict__)
            return user
        return None

    def create(self, item: UserInDB) -> UserOutput:
        user_db = User(**item.__dict__)
        try:
            self.db.add(user_db)
            self.db.commit()
            self.db.refresh(user_db)
            user = UserOutput(**user_db.__dict__)
            return user
        except Exception as e:
            # TODO raise appropriate exception, Duplicate Email or username
            pass

    def update(self, item: UserInDB) -> UserOutput:
        user_db = self.db.query(User).filter(User.id == item.id).first()
        if user_db:
            try:
                user_db.update(**item.__dict__)
                self.db.commit()
                self.db.refresh(user_db)
                user = UserOutput(**user_db.__dict__)
                return user
            except Exception as e:
                # TODO raise appropriate exception, Duplicate Email or username
                pass

        else:
            # TODO raise appropriate exception, Not found user
            pass

    def delete(self, id: int) -> bool:
        user_db = self.db.query(User).filter(User.id == id).first()
        if user_db:
            user_db.delete()
            self.db.commit()
            return True
        return False

    def set_last_login_now(self, id: int):
        user_db = self.db.query(User).get(id)
        user_db.update(last_login=datetime.now())
        self.db.commit()


user_repository = UserRepository(session)
