from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, Table, UniqueConstraint

class Base(DeclarativeBase):
    pass

# جدول میانی user<->role
user_roles = Table(
    "user_roles",
    Base.metadata,
    mapped_column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    mapped_column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)

    roles = relationship("Role", secondary=user_roles, back_populates="users")

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)

    users = relationship("User", secondary=user_roles, back_populates="roles")