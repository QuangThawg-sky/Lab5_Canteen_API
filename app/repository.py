
from app.schemas import MenuItemCreate, MenuItemPatch

_menu_items: dict[int, dict] = {}
_next_id = 1


def list_items() -> list[dict]:
    return [item.copy() for item in _menu_items.values()]


def get_item(item_id: int) -> dict | None:
    item = _menu_items.get(item_id)
    return item.copy() if item else None


def create_item(data: MenuItemCreate) -> dict | None:
    global _next_id

    for item in _menu_items.values():
        if item["name"].casefold() == data.name.casefold():
            return None

    item = data.model_dump()
    item["id"] = _next_id
    _menu_items[_next_id] = item
    _next_id += 1

    return item.copy()


def replace_item(item_id: int, data: MenuItemCreate) -> dict | None:
    if item_id not in _menu_items:
        return None

    for existing_id, item in _menu_items.items():
        if (
            existing_id != item_id
            and item["name"].casefold() == data.name.casefold()
        ):
            return None

    updated = data.model_dump()
    updated["id"] = item_id
    _menu_items[item_id] = updated

    return updated.copy()


def patch_item(item_id: int, data: MenuItemPatch) -> dict | None:
    if item_id not in _menu_items:
        return None

    changes = data.model_dump(exclude_unset=True)
    current = _menu_items[item_id].copy()

    for key, value in changes.items():
        if value is not None:
            current[key] = value

    for existing_id, item in _menu_items.items():
        if (
            existing_id != item_id
            and item["name"].casefold() == current["name"].casefold()
        ):
            return None

    # Kiểm tra lại các trường hợp giá trị null không hợp lệ
    if (
        not isinstance(current["name"], str)
        or not isinstance(current["category"], str)
        or not isinstance(current["price"], int)
        or not isinstance(current["available"], bool)
    ):
        raise ValueError("Dữ liệu cập nhật không hợp lệ")

    _menu_items[item_id] = current
    return current.copy()


def delete_item(item_id: int) -> bool:
    if item_id not in _menu_items:
        return False

    del _menu_items[item_id]
    return True
