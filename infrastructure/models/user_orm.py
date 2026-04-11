from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.db.base import Base


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    oauth_account: Mapped["OAuthAccountsORM"] = relationship(
        back_populates='user',
        passive_deletes=True,
        uselist=False,
    )


class OAuthAccountsORM(Base):
    __tablename__ = "oauth_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(String(120), nullable=False)
    provider_user_id: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    user: Mapped[UserORM] = relationship(back_populates='oauth_account')

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_user_id",
            name="unique_oauth_provider"
        ),
        # поля в паре должны быть уникальны
    )
