from typing import List

from pydantic import BaseModel


class BatteryAttach(BaseModel):
    device_id: int


class BatteryBase(BaseModel):
    name: str


class BatteryCreate(BatteryBase):
    pass


class BatteryUpdate(BatteryBase):
    pass


class BatteryRead(BatteryBase):
    id: int

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    name: str


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class DeviceRead(DeviceBase):
    id: int
    batteries: List[BatteryRead] = []

    class Config:
        orm_mode = True
