from django.db import models
from django.db.models import Model, BooleanField, CharField, DateField, IntegerField, TextField

# Create your models here.

class Project(Model):
    position_title		= CharField(max_length=80)
    brief_description           = TextField(max_length=2000)
    objectives                  = CharField(max_length=80)
    contact_name		= CharField(max_length=80)
    contact_phone		= CharField(max_length=80)
    project_starts		= DateField()
    project_ends		= DateField()
    announcement_closes         = DateField()
    project_number		= CharField(max_length=80)#generated PAVE-yy-center-orgcode-###
    security_clearance_required = BooleanField()
    nasa_center                 = CharField(max_length=80) # pick-list
    office_id                   = CharField(max_length=80)
    office_title		= CharField(max_length=80)
    skill_mix                   = CharField(max_length=80)
    detail_description          = TextField(max_length=2000)
    pay_plan                    = CharField(max_length=80)
    series_codes		= CharField(max_length=80) # multiples
    grade_levels		= CharField(max_length=80) # multiples
    nasa_centers		= CharField(max_length=80) # multiples; how diff from nasa_center above?



