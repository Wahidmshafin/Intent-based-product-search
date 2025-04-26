from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
import pandas as pd

from backend.db.dao.product_dao import ProductDAO
from backend.db.models.dummy_model import ProductTable
from backend.web.api.search.rag import SearchPipeline
from backend.web.api.productTable.schema import ProductUpload, Products,ProductItem
from datasets import load_dataset


router = APIRouter()
search_pipeline = SearchPipeline()

@router.post("/upload", response_model=ProductUpload)
async def create_product_models(
    limit: int = 50,
    offset: int = 0,
    product_dao: ProductDAO = Depends(),
) -> ProductUpload:
    """
    Upload all the products from CSV file to the Database

    :param limit: limit of Product, defaults to 10.
    :param offset: offset of Product, defaults to 0.
    :param product_dao: DAO for productTable models.
    :return: If products uploaded or not.
    """
    ds = load_dataset("wdc/products-2017","cameras_small")
    cnt=0
    for i, example in enumerate(ds['train'].select(range(limit))):
        await product_dao.add_product(
            new_id = example["id_left"],
            category = example["category_left"],
            brand = example["brand_left"],
            title = example["title_left"],
            description = example["description_left"],
            price = example["price_left"],
            spec = example["specTableContent_left"],
            embedding = search_pipeline.generate_embedding(
    f"category:{str(example['category_left'])}\nbrand:{str(example['brand_left'])}\ntitle:{str(example['title_left'])}\ndescription:{str(example['description_left'])}"
)
        )
        print(cnt)
        cnt=cnt+1
    ds = load_dataset("wdc/products-2017","watches_small")
    cnt=0
    for i, example in enumerate(ds['train'].select(range(limit))):
        await product_dao.add_product(
            new_id = example["id_left"],
            category = example["category_left"],
            brand = example["brand_left"],
            title = example["title_left"],
            description = example["description_left"],
            price = example["price_left"],
            spec = example["specTableContent_left"],
            embedding = search_pipeline.generate_embedding(
    f"category:{str(example['category_left'])}\nbrand:{str(example['brand_left'])}\ntitle:{str(example['title_left'])}\ndescription:{str(example['description_left'])}"
)
        )
        print(cnt)
        cnt=cnt+1
    ds = load_dataset("wdc/products-2017","computers_small")
    cnt=0
    for i, example in enumerate(ds['train'].select(range(limit))):
        await product_dao.add_product(
            new_id = example["id_left"],
            category = example["category_left"],
            brand = example["brand_left"],
            title = example["title_left"],
            description = example["description_left"],
            price = example["price_left"],
            spec = example["specTableContent_left"],
            embedding = search_pipeline.generate_embedding(
    f"category:{str(example['category_left'])}\nbrand:{str(example['brand_left'])}\ntitle:{str(example['title_left'])}\ndescription:{str(example['description_left'])}"
)
        )
        print(cnt)
        cnt=cnt+1
    
    # for index,row in df.iterrows():
    #     await product_dao.add_product(
    #         colorname=str(row["colorname"]),
    #         description=str(row["description"]),
    #         name=str(row["name"]),
    #         fulldescription=str(row["fulldescription"]),
    #         embedding= search_pipeline.generate_embedding(str(row["name"])+"\n"+str(row["fulldescription"]))
    #                             )
    #     cnt = cnt+1
    #     if cnt==limit:
    #         break
    return {"response":"Done"}


@router.get("/all", response_model=List[ProductItem])
async def get_all_products(
    limit: int=8,
    product_dao: ProductDAO = Depends(),
) -> List[ProductItem]:
    """
    Creates dummy model in the database.

    :param new_dummy_object: new dummy model item.
    :param dummy_dao: DAO for dummy models.
    """
    return await product_dao.get_all_products(limit)

