# -*- coding: utf-8 -*-
"""
    Original Author:    Scott Barnham (first version)
    Date:               2008/August/21 (first version)
    Site:               http://scottbarnham.com/blog/2008/08/21/extending-the-django-user-model-with-inheritance/
    Modified by:        GestorPsi - Danilo S. Sanches 
    Date:               2008/September/1
    Description:        This is an authentication backend to return an instance of CustomUser instead of User.
"""

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:            
            user = self.user_class.objects.get(username=username)
            if user.check_password(password):
                #print user.username
                #print user.organization.all()
                return user
        except self.user_class.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class