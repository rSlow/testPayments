from bot_common.api import BaseBackendAPI
from .models import CategoryModel, SubCategoryModel, ProductModel, CartModel
from aiohttp import ClientSession


class ProductsAPI(BaseBackendAPI):
    async def get_categories(self, session: ClientSession) -> list[CategoryModel]:
        async with session.get(self._base + "/products/category/") as response:
            categories = await response.json()
        return [CategoryModel.model_validate(category) for category in categories]

    async def get_category(self,
                           session: ClientSession,
                           category_id: str | int) -> CategoryModel:
        async with session.get(self._base + f"/products/category/{category_id}/") as response:
            category = await response.json()
        return CategoryModel.model_validate(category)

    async def get_subcategory(self,
                              session: ClientSession,
                              subcategory_id: str | int,
                              local: bool = True) -> SubCategoryModel:
        _request_base = self._get_base(local)
        async with session.get(_request_base + f"/products/subcategory/{subcategory_id}/") as response:
            subcategory = await response.json()
        return SubCategoryModel.model_validate(subcategory)

    async def get_product(self,
                          session: ClientSession,
                          product_id: str | int,
                          local: bool = True) -> ProductModel:
        _request_base = self._get_base(local)
        async with session.get(_request_base + f"/products/{product_id}/") as response:
            product = await response.json()
        return ProductModel.model_validate(product)

    async def get_cart(self,
                       session: ClientSession,
                       user_id: int):
        async with session.get(self._base + f"/cart/{user_id}/") as response:
            cart = await response.json()
        if response.status == 404:
            async with session.post(
                    url=self._base + f"/cart/{user_id}/",
                    data={"user_id": user_id}
            ) as response:
                cart = await response.json()
        return CartModel.model_validate(cart)

    async def add_product_in_cart(self,
                                  session: ClientSession,
                                  cart_id: int,
                                  product_id: str | int,
                                  count: int):
        async with session.post(
                url=self._base + f"/cart/add/",
                data={
                    "product_id": product_id,
                    "cart_id": cart_id,
                    "count": count
                }
        ) as response:
            if response.status == 200:
                return True
            raise ValueError(f"error {response.status} while add product in cart")
