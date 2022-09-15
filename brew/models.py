from tortoise import Model, fields
from tortoise.contrib.mysql.indexes import FullTextIndex


class App(Model):
    token = fields.CharField(max_length=50, unique=True)
    name = fields.CharField(max_length=200)
    desc = fields.TextField(null=True)
    homepage = fields.CharField(max_length=500)
    url = fields.CharField(max_length=500)
    version = fields.CharField(max_length=200)
    sha256 = fields.CharField(max_length=64)

    class Meta:
        indexes = [FullTextIndex(fields={"name", "desc"})]
