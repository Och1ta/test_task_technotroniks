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
    DeviceCreate, DeviceUpdate, DeviceRead, BatteryAttach
)


router = APIRouter()


@router.get("/batteries/{battery_id}/", response_model=BatteryRead, tags=['batteries'])
def read_battery(battery_id: int, db: Session = Depends(get_db)):
    db_battery = get_battery(db=db, battery_id=battery_id)
    if db_battery is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    return db_battery


@router.get("/batteries/", response_model=List[BatteryRead], tags=['batteries'])
def read_batteries(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_batteries(db=db, skip=skip, limit=limit)


@router.post("/batteries/", response_model=BatteryRead, tags=['batteries'])
def create_battery_endpoint(battery: BatteryCreate, db: Session = Depends(get_db)):
    return create_battery(db=db, name=battery.name)


@router.put("/batteries/{battery_id}/", response_model=BatteryRead, tags=['batteries'])
def update_battery_endpoint(battery_id: int, battery: BatteryUpdate, db: Session = Depends(get_db)):
    db_battery = update_battery(db=db, battery_id=battery_id, name=battery.name)
    if db_battery is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    return db_battery


@router.delete("/batteries/{battery_id}/", response_model=BatteryRead, tags=['batteries'])
def delete_battery_endpoint(battery_id: int, db: Session = Depends(get_db)):
    db_battery = delete_battery(db=db, battery_id=battery_id)
    if db_battery is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    return db_battery


@router.get("/devices/{device_id}/", response_model=DeviceRead, tags=['devices'])
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = get_device_with_batteries(db=db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@router.get("/devices/", response_model=List[DeviceRead], tags=['devices'])
def read_devices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_devices(db=db, skip=skip, limit=limit)


@router.post("/devices/", response_model=DeviceRead, tags=['devices'])
def create_device_endpoint(device: DeviceCreate, db: Session = Depends(get_db)):
    return create_device(db=db, name=device.name)


@router.post("/devices/{device_id}/batteries/{battery_id}/attach", response_model=BatteryRead, tags=['devices'])
def attach_battery_to_device_endpoint(device_id: int, battery_id: int, db: Session = Depends(get_db)):
    try:
        battery = attach_battery_to_device(db=db, battery_id=battery_id, device_id=device_id)
        return battery
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/devices/{device_id}/", response_model=DeviceRead, tags=['devices'])
def update_device_endpoint(device_id: int, device: DeviceUpdate, db: Session = Depends(get_db)):
    db_device = update_device(db=db, device_id=device_id, name=device.name)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@router.delete("/devices/{device_id}/", response_model=DeviceRead, tags=['devices'])
def delete_device_endpoint(device_id: int, db: Session = Depends(get_db)):
    db_device = delete_device(db=db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device
