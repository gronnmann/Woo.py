import datetime
from enum import Enum
from pydantic import BaseModel, Field
from pydantic_changedetect import ChangeDetectionMixin


class ReviewStatus(str, Enum):
    APPROVED = "approved"
    HOLD = "hold"
    SPAM = "spam"
    UNSPAM = "unspam"
    TRASH = "trash"
    UNTRASH = "untrash"


class ProductReview(ChangeDetectionMixin, BaseModel):
    id: int | None = None
    date_created: datetime.datetime | None = None
    date_created_gmt: datetime.datetime | None = None
    product_id: int
    status: ReviewStatus = ReviewStatus.APPROVED
    reviewer: str
    reviewer_email: str
    review: str
    rating: int = Field(ge=0, le=5)
    verified: bool | None = None
    reviewer_avatar_urls: dict[str, str] | None = None
