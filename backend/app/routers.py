from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.crud import (
    get_battery, get_batteries, create_battery,
    update_battery, delete_battery,
    get_devices, create_device, attach_battery_to_device,
    update_device, delete_device, get_device_with_batteries
)
from app.database import get_db
from app.schemas import (
    BatteryCreate, BatteryUpdate, BatteryRead,
    DeviceCreate, DeviceUpdate, DeviceRead
)

router = APIRouter()


@router.get(
    "/batteries/{battery_id}/",
    response_model=BatteryRead,
    tags=['batteries']
)
def read_battery(
    battery_id: int,
    db: Session = Depends(get_db)
):
    """
    Получает информацию о батарее по ее идентификатору.

    :param battery_id: Идентификатор батареи.
    :param db: Сессия базы данных.
    :return: Информация о батарее.
    :raises HTTPException: Если батарея не найдена.
    """
    db_battery = get_battery(db=db, battery_id=battery_id)
    if db_battery is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    return db_battery


@router.get(
    "/batteries/",
    response_model=List[BatteryRead],
    tags=['batteries']
)
def read_batteries(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Получает список батарей с возможностью пагинации.

    :param skip: Количество пропущенных записей.
    :param limit: Максимальное количество возвращаемых записей.
    :param db: Сессия базы данных.
    :return: Список батарей.
    """
    return get_batteries(db=db, skip=skip, limit=limit)


@router.post(
    "/batteries/",
    response_model=BatteryRead,
    tags=['batteries']
)
def create_battery_endpoint(
    battery: BatteryCreate,
    db: Session = Depends(get_db)
):
    """
    Создает новую батарею.

    :param battery: Данные для создания батареи.
    :param db: Сессия базы данных.
    :return: Созданная батарея.
    """
    return create_battery(db=db, name=battery.name)


@router.put(
    "/batteries/{battery_id}/",
    response_model=BatteryRead,
    tags=['batteries']
)
def update_battery_endpoint(
    battery_id: int,
    battery: BatteryUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновляет информацию о батарее по ее идентификатору.

    :param battery_id: Идентификатор батареи.
    :param battery: Новые данные для батареи.
    :param db: Сессия базы данных.
    :return: Обновленная батарея.
    :raises HTTPException: Если батарея не найдена.
    """
    db_battery = update_battery(db=db, battery_id=battery_id, name=battery.name)
    if db_battery is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    return db_battery


@router.delete(
    "/batteries/{battery_id}/",
    response_model=BatteryRead,
    tags=['batteries']
)
def delete_battery_endpoint(
    battery_id: int,
    db: Session = Depends(get_db)
):
    """
    Удаляет батарею по ее идентификатору.

    :param battery_id: Идентификатор батареи.
    :param db: Сессия базы данных.
    :return: Удаленная батарея.
    :raises HTTPException: Если батарея не найдена.
    """
    db_battery = delete_battery(db=db, battery_id=battery_id)
    if db_battery is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    return db_battery


@router.get(
    "/devices/{device_id}/",
    response_model=DeviceRead,
    tags=['devices']
)
def read_device(
    device_id: int,
    db: Session = Depends(get_db)
):
    """
    Получает информацию об устройстве по его идентификатору вместе с привязанными батареями.

    :param device_id: Идентификатор устройства.
    :param db: Сессия базы данных.
    :return: Информация об устройстве и его батареях.
    :raises HTTPException: Если устройство не найдено.
    """
    db_device = get_device_with_batteries(db=db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@router.get(
    "/devices/",
    response_model=List[DeviceRead],
    tags=['devices']
)
def read_devices(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Получает список устройств с возможностью пагинации.

    :param skip: Количество пропущенных записей.
    :param limit: Максимальное количество возвращаемых записей.
    :param db: Сессия базы данных.
    :return: Список устройств.
    """
    return get_devices(db=db, skip=skip, limit=limit)


@router.post(
    "/devices/",
    response_model=DeviceRead,
    tags=['devices']
)
def create_device_endpoint(
    device: DeviceCreate,
    db: Session = Depends(get_db)
):
    """
    Создает новое устройство.

    :param device: Данные для создания устройства.
    :param db: Сессия базы данных.
    :return: Созданное устройство.
    """
    return create_device(db=db, name=device.name)


@router.post(
    "/devices/{device_id}/batteries/{battery_id}/attach",
    response_model=BatteryRead,
    tags=['devices']
)
def attach_battery_to_device_endpoint(
    device_id: int,
    battery_id: int,
    db: Session = Depends(get_db)
):
    """
    Присоединяет батарею к устройству.

    :param device_id: Идентификатор устройства.
    :param battery_id: Идентификатор батареи.
    :param db: Сессия базы данных.
    :return: Обновленная батарея.
    :raises HTTPException: Если батарея или устройство не найдены,
    или если батарея уже привязана к другому устройству.
    """
    try:
        battery = attach_battery_to_device(
            db=db, battery_id=battery_id, device_id=device_id
        )
        return battery
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/devices/{device_id}/",
    response_model=DeviceRead,
    tags=['devices']
)
def update_device_endpoint(
    device_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновляет информацию об устройстве по его идентификатору.

    :param device_id: Идентификатор устройства.
    :param device: Новые данные для устройства.
    :param db: Сессия базы данных.
    :return: Обновленное устройство.
    :raises HTTPException: Если устройство не найдено.
    """
    db_device = update_device(db=db, device_id=device_id, name=device.name)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@router.delete(
    "/devices/{device_id}/",
    response_model=DeviceRead,
    tags=['devices']
)
def delete_device_endpoint(
    device_id: int,
    db: Session = Depends(get_db)
):
    """
    Удаляет устройство по его идентификатору.

    :param device_id: Идентификатор устройства.
    :param db: Сессия базы данных.
    :return: Удаленное устройство.
    :raises HTTPException: Если устройство не найдено.
    """
    db_device = delete_device(db=db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device
