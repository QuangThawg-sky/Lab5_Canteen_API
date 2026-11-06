from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator


class MenuCategory(str, Enum):
    com = "com"
    bun_pho = "bun_pho"
    do_uong = "do_uong"
    an_vat = "an_vat"


class MenuItemBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=2, max_length=100)
    category: MenuCategory
    price: int = Field(..., gt=0, le=200000)
    available: bool = True

    @field_validator("price")
    @classmethod
    def validate_price_multiple_of_1000(cls, value):
        if value % 1000 != 0:
            raise ValueError("Giá phải chia hết cho 1000")
        return value


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(MenuItemBase):
    pass


class MenuItemPatch(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=2, max_length=100)
    category: MenuCategory | None = None
    price: int | None = Field(default=None, gt=0, le=200000)
    available: bool | None = None


class MenuItemResponse(MenuItemBase):
    id: int