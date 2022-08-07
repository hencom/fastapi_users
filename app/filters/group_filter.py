from fastapi_filter.contrib.sqlalchemy import Filter
from models import user_models


class AddressFilter(Filter):
    name: str | None
    comment: str | None
    # city: str | None
    # city__in: list[str] | None
    custom_order_by: list[str] | None

    class Constants(Filter.Constants):
        model = user_models.Group
        ordering_field_name = "custom_order_by"
