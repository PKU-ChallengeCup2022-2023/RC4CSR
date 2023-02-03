from Recommendation.models import Tags, Book_Tag
from django.db.utils import IntegrityError

for _ in Tags:
    for __ in _[1]:
        try:
            Book_Tag.objects.create(book_tag=_[0]+'-'+__[1])
        except IntegrityError:
            pass