from django.contrib.auth.models import User
from django.db.models import Model, BooleanField, CharField, DateField, IntegerField, TextField, ForeignKey, ManyToManyField

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
    code        = CharField(max_length=8)  # GS-1550
    name        = CharField(max_length=64) # GS-1550 - Computer Science

    def __unicode__(self):
        return u'%s' % self.name

class Applicant(Model):         # aren't there phone, email and other validating models?
    # First form verified against LDAP
    center                      = ForeignKey(Center)
    last_name                   = CharField(max_length=80)
    first_name                  = CharField(max_length=80)
    # Second form not verified: why not populated from LDAP?
    email                       = CharField(max_length=80)
    phone                       = CharField(max_length=80)
    # Third form
    supervisor_name             = CharField(max_length=80) # combined first and last, stupidly
    supervisor_phone            = CharField(max_length=80) # why not looked up from LDAP?
    supervisor_email            = CharField(max_length=80) # why not looked up from LDAP?
    comments                    = TextField(max_length=800)
    relevant_experience         = TextField(max_length=2000)
    anticipated_gain            = TextField(max_length=2000)

    def __unicode__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, center)

class Project(Model):
    position_title		= CharField(max_length=80)
    brief_description           = TextField(max_length=2000)
    objectives                  = CharField(max_length=80, blank=True)
    contact_name		= CharField(max_length=80)
    contact_phone		= CharField(max_length=80)
    project_starts		= DateField()
    project_ends		= DateField()
    announcement_closes         = DateField()
    project_number		= CharField(max_length=80)#generated PAVE-yy-center-orgcode-###
    security_clearance_required = BooleanField()
    nasa_center                 = ForeignKey(Center, related_name='Center')
    office_id                   = CharField(max_length=80)
    office_title		= CharField(max_length=80)
    skill_mix                   = CharField(max_length=80, blank=True)
    detail_description          = TextField(max_length=2000, blank=True)
    pay_plan                    = CharField(max_length=80) # GS, are there others?
    series_codes		= ManyToManyField(JobCode)
    grade_levels		= ManyToManyField(GradeLevel)
    nasa_centers		= ManyToManyField(Center, related_name='Centers')
    owner                       = ForeignKey(User, unique=False, blank=False)
    applicant                   = ForeignKey(Applicant, unique=False, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.position_title



