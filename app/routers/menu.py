
from typing import Literal

from fastapi import APIRouter, HTTPException, Query, Response, status

from app import repository
from app.schemas import (
    MenuItemCreate,
    MenuItemPatch,
    MenuItemResponse,
)

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])


@router.get("", response_model=list[MenuItemResponse])
def get_menu_items(
    category: str | None = None,
    available: bool | None = None,
    max_price: int | None = Query(default=None, gt=0),
    sort: Literal["id", "price", "name"] = "id",
    order: Literal["asc", "desc"] = "asc",
):
    items = repository.list_items()

    if category is not None:
        valid_categories = {"com", "bun_pho", "do_uong", "an_vat"}
        if category not in valid_categories:
            raise HTTPException(status_code=422, detail="Danh mục không hợp lệ")
        items = [item for item in items if item["category"] == category]

    if available is not None:
        items = [item for item in items if item["available"] == available]

    if max_price is not None:
        items = [item for item in items if item["price"] <= max_price]

    items.sort(key=lambda item: item[sort], reverse=(order == "desc"))
    return items


@router.get("/{item_id}", response_model=MenuItemResponse)
def get_menu_item(item_id: int):
    item = repository.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
    return item


@router.post(
    "",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_menu_item(data: MenuItemCreate, response: Response):
    item = repository.create_item(data)
    if item is None:
        raise HTTPException(status_code=409, detail="Tên món ăn đã tồn tại")

    response.headers["Location"] = f"/menu-items/{item['id']}"
    return item


@router.put("/{item_id}", response_model=MenuItemResponse)
def replace_menu_item(item_id: int, data: MenuItemCreate):
    item = repository.replace_item(item_id, data)
    if item is None:
        if repository.get_item(item_id) is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
        raise HTTPException(status_code=409, detail="Tên món ăn đã tồn tại")
    return item


@router.patch("/{item_id}", response_model=MenuItemResponse)
def patch_menu_item(item_id: int, data: MenuItemPatch):
    if data.model_dump(exclude_unset=True) == {}:
        raise HTTPException(status_code=422, detail="Chưa có trường nào để cập nhật")

    try:
        item = repository.patch_item(item_id, data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    if item is None:
        if repository.get_item(item_id) is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
        raise HTTPException(status_code=409, detail="Tên món ăn đã tồn tại")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(item_id: int):
    deleted = repository.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
