from sqlalchemy.orm import Session

from app.models import Device, Battery


def create_device(db: Session, name: str):
    """
    Создает новое устройство и сохраняет его в базе данных.

    :param db: Сессия базы данных.
    :param name: Имя устройства.
    :return: Созданное устройство.
    """
    db_device = Device(name=name)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def get_device_with_batteries(db: Session, device_id: int):
    """
    Получает устройство по его идентификатору вместе с привязанными к нему батареями.

    :param db: Сессия базы данных.
    :param device_id: Идентификатор устройства.
    :return: Словарь с данными об устройстве и привязанных к нему батареях.
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    if device:
        return {
            'id': device.id,
            'name': device.name,
            'batteries': [{'id': b.id, 'name': b.name} for b in device.batteries]
        }
    return None


def get_devices(db: Session, skip: int = 0, limit: int = 10):
    """
    Получает список устройств с возможностью пропуска и ограничения количества результатов.

    :param db: Сессия базы данных.
    :param skip: Количество пропущенных записей (для пагинации).
    :param limit: Максимальное количество возвращаемых записей.
    :return: Список устройств.
    """
    return db.query(Device).offset(skip).limit(limit).all()


def update_device(db: Session, device_id: int, name: str):
    """
    Обновляет имя устройства по его идентификатору.

    :param db: Сессия базы данных.
    :param device_id: Идентификатор устройства.
    :param name: Новое имя устройства.
    :return: Обновленное устройство или None, если устройство не найдено.
    """
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if db_device:
        db_device.name = name
        db.commit()
        db.refresh(db_device)
        return db_device
    return None


def delete_device(db: Session, device_id: int):
    """
    Удаляет устройство по его идентификатору.

    :param db: Сессия базы данных.
    :param device_id: Идентификатор устройства.
    :return: Удаленное устройство или None, если устройство не найдено.
    """
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if db_device:
        db.delete(db_device)
        db.commit()
        return db_device
    return None


def attach_battery_to_device(db: Session, battery_id: int, device_id: int):
    """
    Присоединяет аккумулятор к устройству.

    :param db: Сессия базы данных.
    :param battery_id: Идентификатор батареи.
    :param device_id: Идентификатор устройства.
    :return: Обновленная батарея.
    :raises ValueError: Если батарея или устройство не найдены,
                        батарея уже привязана к другому устройству,
                        или устройство имеет уже 5 привязанных батарей.
    """
    battery = db.query(Battery).filter(Battery.id == battery_id).first()
    device = db.query(Device).filter(Device.id == device_id).first()

    if not battery:
        raise ValueError("Battery not found")
    if not device:
        raise ValueError("Device not found")
    if battery.device_id:
        raise ValueError("Battery is already assigned to another device")
    if len(device.batteries) >= 5:
        raise ValueError("Cannot add more than 5 batteries to a device")

    battery.device_id = device_id
    db.commit()
    db.refresh(battery)
    return battery


def create_battery(db: Session, name: str):
    """
    Создает новую батарею и сохраняет ее в базе данных.

    :param db: Сессия базы данных.
    :param name: Имя батареи.
    :return: Созданная батарея.
    """
    db_battery = Battery(name=name)
    db.add(db_battery)
    db.commit()
    db.refresh(db_battery)
    return db_battery


def get_battery(db: Session, battery_id: int):
    """
    Получает батарею по ее идентификатору.

    :param db: Сессия базы данных.
    :param battery_id: Идентификатор батареи.
    :return: Батарея или None, если батарея не найдена.
    """
    return db.query(Battery).filter(Battery.id == battery_id).first()


def get_batteries(db: Session, skip: int = 0, limit: int = 10):
    """
    Получает список батарей с возможностью пропуска и ограничения количества результатов.

    :param db: Сессия базы данных.
    :param skip: Количество пропущенных записей (для пагинации).
    :param limit: Максимальное количество возвращаемых записей.
    :return: Список батарей.
    """
    return db.query(Battery).offset(skip).limit(limit).all()


def update_battery(db: Session, battery_id: int, name: str):
    """
    Обновляет имя батареи по ее идентификатору.

    :param db: Сессия базы данных.
    :param battery_id: Идентификатор батареи.
    :param name: Новое имя батареи.
    :return: Обновленная батарея или None, если батарея не найдена.
    """
    db_battery = db.query(Battery).filter(Battery.id == battery_id).first()
    if db_battery:
        db_battery.name = name
        db.commit()
        db.refresh(db_battery)
        return db_battery
    return None


def delete_battery(db: Session, battery_id: int):
    """
    Удаляет батарею по ее идентификатору.

    :param db: Сессия базы данных.
    :param battery_id: Идентификатор батареи.
    :return: Удаленная батарея или None, если батарея не найдена.
    """
    db_battery = db.query(Battery).filter(Battery.id == battery_id).first()
    if db_battery:
        db.delete(db_battery)
        db.commit()
        return db_battery
    return None
