import json
import os
from typing import List

from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise

from .models import Rates_Pydantic, Rates

app = FastAPI(title="Tortoise ORM FastAPI example")


@app.post("/")
async def create_rate(json_data):
    data = json.loads(json_data)
    for date in data.keys():
        d = dict()
        for v in data[date]:
            try:
                rate = float(v["rate"])
            except Exception:
                raise HTTPException(status_code=422,
                                    detail=f'Unprocessable Entity in {date} {v["cargo_type"]}')
            d[v["cargo_type"]] = rate
        await Rates.create(date=date, data=json.dumps(d))
    return await Rates_Pydantic.from_queryset(Rates.all())


@app.get("/", response_model=List[Rates_Pydantic])
async def get_rates():
    return await Rates_Pydantic.from_queryset(Rates.all())


# http://127.0.0.1:8000/calc?date=2020-06-01&cargo_type=Glass&cost=100
@app.get("/calc")
async def get_rate(date: str, cargo_type: str, cost: int):
    rate = await Rates_Pydantic.from_queryset_single(Rates.get(date=date))
    if rate.data.get(cargo_type) is None:
        raise HTTPException(status_code=404, detail=f"{cargo_type} not found")
    return float(rate.data[cargo_type]) * cost


register_tortoise(
    app,
    db_url=os.environ.get("DATABASE_URL"),
    # db_url="sqlite://test.db",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
