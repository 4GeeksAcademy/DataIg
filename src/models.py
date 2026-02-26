from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    signup_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.utcnow)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    likes: Mapped[list["Likes"]] = relationship("Likes", back_populates="user")
    comments: Mapped[list["Comments"]] = relationship("Comments", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "is_active": self.is_active,
            "signup_date": self.signup_date.isoformat()
        }
       
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(80), nullable=False)
    url_img: Mapped[str] = mapped_column(String(255), nullable=True)
    likes: Mapped[int] = mapped_column(Integer(), default=0)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="posts")
    likes_list: Mapped[list["Likes"]] = relationship("Likes", back_populates="post")
    comments_list: Mapped[list["Comments"]] = relationship("Comments", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "url_img": self.url_img,
            "id_user": self.id_user,
            "likes": self.likes
        }
    
class Followers(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_follower: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    id_followed: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "id_follower": self.id_follower,
            "id_followed": self.id_followed,
            "date": self.date.isoformat()
        }      
    
class Likes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_post: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="likes")
    post: Mapped["Post"] = relationship("Post", back_populates="likes_list")

    def serialize(self):
        return {
            "id": self.id,
            "id_post": self.id_post,
            "id_user": self.id_user,
            "date": self.date.isoformat()
        }

class Comments(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_post: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    comments: Mapped[str] = mapped_column(String(300), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments_list")

    def serialize(self):
        return {
            "id": self.id,
            "id_post": self.id_post,
            "id_user": self.id_user,
            "comments": self.comments,
            "date": self.date.isoformat()
        }