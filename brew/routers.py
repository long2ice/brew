from fastapi import APIRouter
from pydantic import conint, NonNegativeInt
from pypika.terms import Field, Term
from tortoise.contrib.mysql.search import SearchCriterion

from brew.models import App

router = APIRouter()


@router.get("/search")
async def search(
    keyword: str, limit: conint(gt=0, le=20) = 20, offset: NonNegativeInt = 0
):
    return (
        await App.annotate(
            score=SearchCriterion(
                Field("name"), Field("desc"), expr=Term.wrap_constant(keyword)
            )
        )
        .filter(score__gt=0)
        .order_by("-score")
        .limit(limit)
        .offset(offset)
    )
