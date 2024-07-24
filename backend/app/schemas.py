from typing import List

from pydantic import BaseModel


class BatteryAttach(BaseModel):
    """
    Схема для привязки батареи к устройству.

    :param device_id: Идентификатор устройства, к которому будет привязана батарея.
    """
    device_id: int


class BatteryBase(BaseModel):
    """
    Базовая схема для батарей.

    :param name: Имя батареи.
    """
    name: str


class BatteryCreate(BatteryBase):
    """
    Схема для создания новой батареи.

    Наследует от `BatteryBase` и не добавляет новых полей.
    """
    pass


class BatteryUpdate(BatteryBase):
    """
    Схема для обновления информации о батарее.

    Наследует от `BatteryBase` и не добавляет новых полей.
    """
    pass


class BatteryRead(BatteryBase):
    """
    Схема для чтения информации о батарее.

    :param id: Идентификатор батареи.
    """
    id: int

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    """
    Базовая схема для устройств.

    :param name: Имя устройства.
    """
    name: str


class DeviceCreate(DeviceBase):
    """
    Схема для создания нового устройства.

    Наследует от `DeviceBase` и не добавляет новых полей.
    """
    pass


class DeviceUpdate(DeviceBase):
    """
    Схема для обновления информации об устройстве.

    Наследует от `DeviceBase` и не добавляет новых полей.
    """
    pass


class DeviceRead(DeviceBase):
    """
    Схема для чтения информации об устройстве.

    :param id: Идентификатор устройства.
    :param batteries: Список батарей, привязанных к устройству.
    """
    id: int
    batteries: List[BatteryRead] = []

    class Config:
        orm_mode = True
