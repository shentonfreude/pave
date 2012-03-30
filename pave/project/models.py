from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, ManyToManyField
from django.db.models import BooleanField, CharField, DateField, EmailField, IntegerField, TextField
from autoslug import AutoSlugField

# TBD for forms get choices:
# class ProfileForm(forms.ModelForm):
#     the_choices = forms.ModelMultipleChoiceField(queryset=Choices.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

class Center(Model):
    code        = IntegerField()  # 5100
    name        = CharField(max_length=8) # GSFC

    def __unicode__(self):
        return u'%s' % self.name

class Status(Model):
    name      = CharField(max_length=16) # Announced, Closed, Cancelled

    def __unicode__(self):
        return u'%s' % self.name

class GradeLevel(Model):
    name        = CharField(max_length=8) # 15 (as in GS-15, but can we also have SES-18?)

    def __unicode__(self):
        return u'%s' % self.name

class JobCode(Model):
    code        = CharField(max_length=8)   # GS-1550
    name        = CharField(max_length=128) # GS-1550 - Computer Science

    def __unicode__(self):
        return u'%s' % self.name

class Applicant(Model):
    # First form verified against LDAP
    center                      = ForeignKey(Center)
    last_name                   = CharField(max_length=80)
    first_name                  = CharField(max_length=80)
    # Second form not verified: why not populated from LDAP?
    email                       = EmailField(max_length=80)
    phone                       = CharField(max_length=80)
    # Third form
    supervisor_name             = CharField(max_length=80) # combined first and last, stupidly
    supervisor_phone            = CharField(max_length=80) # why not looked up from LDAP?
    supervisor_email            = EmailField(max_length=80) # why not looked up from LDAP?
    comments                    = TextField(max_length=800)
    relevant_experience         = TextField(max_length=2000)
    anticipated_gain            = TextField(max_length=2000)

    def __unicode__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, self.center)

def _create_slug(instance):
    """Return urPAVE-shaped slug: PAVE-yy-center-officeid-###
    yy:         last 2 digites of year
    center:     like HQ
    officeid:   like LM020
    ####:       monotonically-increasing nubmer
    For ###, can't use .id as we don't have it yet, instance isn't saved;
    let AutoSlugify uniqify it.
    This doesn't fit urPAVE as the uniqififier is only appended if needed, so we get
      pave-12-hq-lmao
      pave-12-hq-lmao-2
    but we want
      pave-12-hq-lmao-376
      pave-12-hq-lmao-377

    Note that the Admin UI doesn't change the slug if the fields are changed.

    IMHO it's *wrong* to encode information in a unique ID.
    What happens if someone needs to change the Center? the URL changes.
    """
    return 'PAVE %02d %s %s' % (
        datetime.now().year % 100,
        instance.nasa_center,
        instance.office_id,
        )


class Project(Model):
    position_title		= CharField(max_length=80)
    brief_description           = TextField(max_length=2000)
    objectives                  = TextField(max_length=2000, blank=True)
    contact_name		= CharField(max_length=150) # For Donnie's over-long name AAAAAA...
    contact_phone		= CharField(max_length=80)
    project_starts		= DateField(help_text="YYYY-MM-DD")
    project_ends		= DateField(help_text="YYYY-MM-DD")
    announcement_closes         = DateField(help_text="YYYY-MM-DD")
    cancel_date                 = DateField(blank=True, null=True, help_text="YYYY-MM-DD") # move these to end of schema?
    cancel_reason               = TextField(max_length=2000, blank=True)
    project_number		= AutoSlugField(unique=True, populate_from=_create_slug)
    security_clearance_required = BooleanField()
    nasa_center                 = ForeignKey(Center, related_name='Center')
    office_id                   = CharField(max_length=80)
    office_title		= CharField(max_length=200)
    skill_mix                   = TextField(max_length=2000, blank=True)
    detail_description          = TextField(max_length=2000, blank=True)
    pay_plan                    = CharField(max_length=80, default='GS') # GS, are there others?
    series_codes		= ManyToManyField(JobCode)
    grade_levels		= ManyToManyField(GradeLevel)
    nasa_centers		= ManyToManyField(Center, related_name='Centers')
    owner                       = ForeignKey(User, unique=False, blank=False)
    status                      = ForeignKey(Status, unique=False, blank=False)
    applicant                   = ForeignKey(Applicant, unique=False, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.position_title


