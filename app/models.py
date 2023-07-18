from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Rates(models.Model):
    """
    The Rates model
    """
    date = fields.DateField(pk=True)
    data = fields.JSONField()


Rates_Pydantic = pydantic_model_creator(Rates, name="Rates")
