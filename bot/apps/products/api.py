from common.api import BaseBackendAPI
from .models import CategoryModel, SubCategoryModel, ProductModel
from aiohttp import ClientSession


class ProductsAPI(BaseBackendAPI):
    async def get_categories(self, session: ClientSession):
        async with session.get(self._base + "/products/categories/") as response:
            categories = await response.json()
        return [CategoryModel.model_validate(category) for category in categories]

    async def get_subcategories(self,
                                session: ClientSession,
                                category_id: str | int):
        async with session.get(self._base + f"/products/categories/{category_id}/") as response:
            subcategories = await response.json()
        return [SubCategoryModel.model_validate(subcategory) for subcategory in subcategories]

    async def get_products(self,
                           session: ClientSession,
                           category_id: str | int,
                           subcategory_id: str | int,
                           local: bool = True):
        _request_base = self._get_base(local)
        async with session.get(_request_base + f"/products/categories/{category_id}/{subcategory_id}/") as response:
            products = await response.json()
        return [ProductModel.model_validate(product) for product in products]

    async def get_product(self,
                          session: ClientSession,
                          product_id: str | int,
                          local: bool = True):
        _request_base = self._get_base(local)
        async with session.get(_request_base + f"/products/{product_id}/") as response:
            product = await response.json()
        return ProductModel.model_validate(product)

    async def add_product_in_cart(self,
                                  session: ClientSession,
                                  user_id: int,
                                  product_id: str | int,
                                  count: int):
        async with session.post(
                url=self._base + f"/cart/{user_id}",
                data={
                    "product_id": product_id,
                    "count": count
                }
        ) as response:
            if response.status == 200:
                return True
            raise ValueError(f"error {response.status} while add product in cart")
