from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    batteries = relationship(
        "Battery", back_populates="device",
        cascade="all, delete", passive_deletes=True
    )


class Battery(Base):
    __tablename__ = "batteries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    device_id = Column(
        Integer, ForeignKey("devices.id", ondelete="CASCADE")
    )
    device = relationship("Device", back_populates="batteries")
