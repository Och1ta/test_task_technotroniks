from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Device(Base):
    """
    Модель для таблицы устройств в базе данных.

    :param id: Уникальный идентификатор устройства.
    :param name: Имя устройства, должно быть уникальным.
    :param batteries: Связь один-ко-многим с батареями, привязанными к устройству.
    """

    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    batteries = relationship(
        "Battery", back_populates="device",
        cascade="all, delete", passive_deletes=True
    )


class Battery(Base):
    """
    Модель для таблицы батарей в базе данных.

    :param id: Уникальный идентификатор батареи.
    :param name: Имя батареи, должно быть уникальным.
    :param device_id: Идентификатор устройства, к которому привязана батарея.
    :param device: Связь многие-к-одному с устройством, к которому привязана батарея.
    """

    __tablename__ = "batteries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    device_id = Column(
        Integer, ForeignKey("devices.id", ondelete="CASCADE")
    )
    device = relationship("Device", back_populates="batteries")
