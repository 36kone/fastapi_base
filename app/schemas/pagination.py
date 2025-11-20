from typing import List, Optional, TypeVar, Generic

from app.schemas.base import BaseSchema

T = TypeVar("T")


class Pagination(BaseSchema):
    total: int
    size: int
    current: int
    pages: int
    previous: Optional[bool]
    next: Optional[bool]


# class PaginatedResponse(BaseModel, Generic[T]):
#     pagination: Pagination
#     list: List[T]


class PaginatedResponse(BaseSchema, Generic[T]):
    pagination: Pagination
    list: List[T]

    @classmethod
    def create(
        cls, *, total: int, page: int, size: int, items: List[T]
    ) -> "PaginatedResponse[T]":
        pages = (total // size) + (1 if total % size > 0 else 0)
        previous = page > 1
        next_ = page < pages

        pagination = Pagination(
            total=total,
            size=size,
            current=page,
            pages=pages,
            previous=previous,
            next=next_,
        )

        return cls(pagination=pagination, list=items)
