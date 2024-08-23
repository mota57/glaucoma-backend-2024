from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)



class Thread2(Model):
    class Meta:
        table_name = 'Thread2'
        # Specifies the region
        region = 'us-east-1'
    forum_name = UnicodeAttribute(hash_key=True)
    subject = UnicodeAttribute(range_key=True)
    views = NumberAttribute(default=0)
    replies = NumberAttribute(default=0)
    answered = NumberAttribute(default=0)
    tags = UnicodeSetAttribute()
    last_post_datetime = UTCDateTimeAttribute()


Thread2.exists()
#if not Thread.exists():
#    res = Thread.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
 