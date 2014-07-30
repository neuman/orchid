from carteblanche.mixins import DjangoVerb, availability_login_required
from carteblanche.base import Verb, Noun
from django.core.urlresolvers import reverse

APPNAME = 'core'

class CoreVerb(DjangoVerb):
    app = APPNAME
    condition_name = 'public'

class UnauthenticatedOnlyVerb(CoreVerb):
    condition_name = 'is_unauthenticated'
    required = True

    def is_available(self, user):
        #only available to non-logged in users
        if user.is_authenticated():
            return False
        return True

class AuthenticatedOnlyVerb(CoreVerb):
    condition_name = 'is_authenticated'
    required = True

    @availability_login_required
    def is_available(self, user):
        return True

class StaffVerb(CoreVerb):
    condition_name = 'is_staff'
    required = True

    @availability_login_required
    def is_available(self, user):
        return user.is_staff

class SiteLoginVerb(UnauthenticatedOnlyVerb):
    display_name = "Login"
    #no view name ok because this is always allowed, fb handles the authentication

    def get_url(self):
        return reverse('user_login')

class HistoryListVerb(CoreVerb):
    display_name = "View History"
    view_name='history_list'
    required = True
    denied_message = "Sorry, you can't view that history yet."

    def is_available(self, user):
        return self.noun.is_visible_to(user)

class LocationCreateVerb(AuthenticatedOnlyVerb):
    display_name = "Create New Location"
    view_name='location_create'

class LocationImageCreateVerb(AuthenticatedOnlyVerb):
    display_name = "Add Image To This Location"
    view_name='location_image_create'

class IndicatorCreateVerb(AuthenticatedOnlyVerb):
    display_name = "Create New Indicator"
    view_name='indicator_create'

class IndicatorDetailVerb(AuthenticatedOnlyVerb):
    display_name = "View Indicator"
    view_name='indicator_detail'

class IndicatorUpdateVerb(AuthenticatedOnlyVerb):
    display_name = "Update Indicator"
    view_name='indicator_update'

class IndicatorListVerb(AuthenticatedOnlyVerb):
    display_name = "View All Indicators"
    view_name='indicator_list'

class IndicatorRecordCreateVerb(AuthenticatedOnlyVerb):
    display_name = "Enter Data"
    view_name='indicator_record_create'

class FieldCreateVerb(AuthenticatedOnlyVerb):
    display_name = "Create New Field"
    view_name='field_create'

class LocationDetailVerb(CoreVerb):
    display_name = "View Location"
    view_name='location_detail'

class LocationFilterVerb(CoreVerb):
    display_name = "Filter Data"
    view_name='location_entries_filter'

class LocationListVerb(AuthenticatedOnlyVerb):
    display_name = "View All Locations"
    view_name='location_list'

class LocationIndicatorListVerb(CoreVerb):
    display_name = "View This Location's Indicators"
    view_name='location_indicator_list'

class SiteRoot(Noun):
    '''
    A hack that lets pages that have no actual noun have verbs and verb-based permissions. 
    '''
    verb_classes = [SiteLoginVerb, LocationListVerb, LocationCreateVerb, IndicatorCreateVerb, IndicatorListVerb]

    class Meta:
        abstract = True

    def __unicode__(self):
        return ''
