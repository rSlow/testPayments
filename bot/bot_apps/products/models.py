from typing import Optional

from pydantic import BaseModel


class CategoryModel(BaseModel):
    pk: int
    name: str
    subcategories: Optional[list["SubCategoryModel"]] = None


class SubCategoryModel(BaseModel):
    pk: int
    name: str
    products: Optional[list["ProductModel"]] = None


class ProductModel(BaseModel):
    pk: int
    title: str
    description: str
    photo: str


class CartModel(BaseModel):
    pk: int
