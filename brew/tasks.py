import httpx
from rearq import ReArq
from tortoise import Tortoise

from brew.models import App
from brew.settings import settings

rearq = ReArq(
    db_url=settings.DB_URL, redis_url=settings.REDIS_URL, keep_job_days=7, job_retry=0
)


@rearq.on_startup
async def startup():
    await Tortoise.init(
        db_url=settings.DB_URL,
        modules={"models": ["brew.models"]},
    )


@rearq.on_shutdown
async def shutdown():
    await Tortoise.close_connections()


@rearq.task()
async def get_cask():
    url = "https://formulae.brew.sh/api/cask.json"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        ret = res.json()
    apps = []
    for item in ret:
        apps.append(
            App(
                token=item["token"],
                name=",".join(item["name"]),
                desc=item["desc"],
                homepage=item["homepage"],
                url=item["url"],
                version=item["version"],
                sha256=item["sha256"],
            )
        )
    await App.bulk_create(
        apps,
        on_conflict="token",
        update_fields=["name", "desc", "homepage", "url", "version", "sha256"],
    )
    return len(apps)


@rearq.task()
async def get_app_icon(app_id: int):
    app = await App.get(pk=app_id).only("url")
    async with httpx.AsyncClient() as client:
        res = await client.get(app.url)
