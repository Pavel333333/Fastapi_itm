from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import func, ForeignKey


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

class Document(Base):
    __tablename__ = 'documents'

    path: Mapped[str] = mapped_column()

    documents_text: Mapped[list['DocumentText']] = relationship('DocumentText',
                                                                back_populates='document',
                                                                cascade='all, delete-orphan',
                                                                lazy="joined")

class DocumentText(Base):
    __tablename__ = 'documents_text'

    id_doc: Mapped[int] = mapped_column(ForeignKey('documents.id'))
    text: Mapped[str] = mapped_column()

    document: Mapped[list['Document']] = relationship('Document',
                                                                back_populates='documents_text')
