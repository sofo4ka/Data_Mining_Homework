import datetime as dt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean


Base = declarative_base()


class IdMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)


class NameMixin:
    name = Column(String, nullable=False)


class UrlMixin:
    url = Column(String, nullable=False, unique=True)


tag_post = Table(
    "tag_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class Post(Base, IdMixin, UrlMixin):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author")
    tags = relationship("Tag", secondary=tag_post)
    comments = relationship("Comment")


class Author(Base, IdMixin, NameMixin, UrlMixin):
    __tablename__ = "author"
    posts = relationship("Post")


class Tag(Base, IdMixin, NameMixin, UrlMixin):
    __tablename__ = "tag"
    posts = relationship("Post", secondary=tag_post)

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    parent_id
    root_comment_id
    likes_count
    body
    html
    created_at - дейттайм '2021-02-22T14:42:03.547+03:00' строчный dt.datetime.fromisoformat()
    date_formatted '22 февраля 2021 в 14:42'

    author_id = Column(Integer, ForeignKey("author.id"))
    full_name
    url
    post_id = Column(Integer, ForeignKey("post.id"))
