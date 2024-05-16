from ninja import Schema


class PaginationIn(Schema):
    offset: int = 0
    limit: int = 20


class PaginationOut(Schema):
    offset: int
    limit: int
    total: int
