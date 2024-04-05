from pydantic import BaseModel


class CategoryModel(BaseModel):
    pk: int
    name: str


class SubCategoryModel(BaseModel):
    pk: int
    name: str


class ProductModel(BaseModel):
    pk: int
    title: str
    description: str
    photo: str
