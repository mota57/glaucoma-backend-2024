from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class user_type(Base):
    __tablename__ = "user_type"
    user_type_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50)) # patient, doctor
    def __repr__(self) -> str:
        return f"user_type(user_type_id={self.user_type_id!r}, name={self.name!r})"

class user_account(Base):
    __tablename__ = "user_account"
    user_account_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    patient_doctor_id: Mapped[Optional[int]] = mapped_column(Integer())
    user_type_id: Mapped[int] = mapped_column(ForeignKey("user_type.user_type_id"))
    identification_number: Mapped[Optional[str]] = mapped_column(String(100))
    # relation 1 to many
    email_addresses: Mapped[List["email_address"]] = relationship(
        back_populates="user_account", cascade="all, delete-orphan"
    )
    patient_files: Mapped[List["patient_file"]] = relationship(
        back_populates="user_account", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"user_account(user_account_id={self.user_account_id!r}, name={self.first_name!r}, fullname={self.last_name!r})"

class file_status(Base):
    __tablename__ = "file_status"
    file_status_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    def __repr__(self) -> str:
        return f"file_status(file_status_id={self.file_status_id!r}, name={self.name!r})"

    
class patient_file(Base):
    __tablename__ = "patient_file"
    patient_file_id: Mapped[int] = mapped_column(primary_key=True)
    # relation file status
    file_status_id: Mapped[int] = mapped_column(ForeignKey("file_status.file_status_id"))
    file_status: Mapped["file_status"] = relationship()
    # relation user account
    user_account_id: Mapped[int] = mapped_column(ForeignKey("user_account.user_account_id"))
    user_account: Mapped["user_account"] = relationship(back_populates="patient_files")
    # props
    message: Mapped[Optional[str]] = mapped_column(String(3000))
    path: Mapped[Optional[str]] = mapped_column(String(200))
    prediction_value: Mapped[Optional[int]] = mapped_column(Integer())

class email_address(Base):
    __tablename__ = "email_address"
    address_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    user_account_id: Mapped[int] = mapped_column(ForeignKey("user_account.user_account_id"))
    user_account: Mapped["user_account"] = relationship(back_populates="email_addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.address_id!r}, email_address={self.email_address!r})"