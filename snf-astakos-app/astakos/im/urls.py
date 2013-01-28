# Copyright 2011-2012 GRNET S.A. All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
#   1. Redistributions of source code must retain the above
#      copyright notice, this list of conditions and the following
#      disclaimer.
#
#   2. Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY GRNET S.A. ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL GRNET S.A OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and
# documentation are those of the authors and should not be
# interpreted as representing official policies, either expressed
# or implied, of GRNET S.A.

from django.conf.urls.defaults import patterns, url

from astakos.im.forms import (
    ExtendedPasswordResetForm,
    ExtendedPasswordChangeForm,
    ExtendedSetPasswordForm, LoginForm)
from astakos.im.settings import IM_MODULES, INVITATIONS_ENABLED, EMAILCHANGE_ENABLED

urlpatterns = patterns(
    'astakos.im.views',
    url(r'^$', 'index', {}, name='index'),
    url(r'^login/?$', 'index', {}, name='login'),
    url(r'^profile/?$','edit_profile', {}, name='edit_profile'),
    url(r'^feedback/?$', 'feedback', {}, name='feedback'),
    url(r'^signup/?$', 'signup', {'on_success': 'index', 'extra_context': {'login_form': LoginForm()}}, name='signup'),
    url(r'^logout/?$', 'logout', {'template': 'im/login.html', 'extra_context': {'login_form': LoginForm()}}, name='logout'),
    url(r'^activate/?$', 'activate', {}, name='activate'),
    url(r'^approval_terms/?$', 'approval_terms', {}, name='latest_terms'),
    url(r'^approval_terms/(?P<term_id>\d+)/?$', 'approval_terms'),
    url(r'^send/activation/(?P<user_id>\d+)/?$', 'send_activation', {}, name='send_activation'),
    url(r'^resources/?$', 'resource_usage', {}, name='resource_usage'),

#    url(r'^billing/?$', 'billing', {}, name='billing'),
#    url(r'^timeline/?$', 'timeline', {}, name='timeline'),

    url(r'^projects/add/?$', 'project_add', {}, name='project_add'),
    url(r'^projects/update/(?P<application_id>\d+)/?$', 'project_update', {}, name='project_update'),
    url(r'^projects/?$', 'project_list', {}, name='project_list'),
    url(r'^projects/search/?$', 'project_search', {}, name='project_search'),
    url(r'^projects/(?P<application_id>\d+)/?$', 'project_detail', {}, name='project_detail'),
    url(r'^projects/(?P<application_id>\d+)/join/?$', 'project_join', {}, name='project_join'),
    url(r'^projects/(?P<application_id>\d+)/leave/?$', 'project_leave', {}, name='project_leave'),
    url(r'^projects/(?P<application_id>\d+)/(?P<user_id>\d+)/accept/?$', 'project_accept_member', {}, name='project_accept_member'),
    url(r'^projects/(?P<application_id>\d+)/(?P<user_id>\d+)/reject/?$', 'project_reject_member', {}, name='project_reject_member'),
    url(r'^projects/(?P<application_id>\d+)/(?P<user_id>\d+)/remove/?$', 'project_remove_member', {}, name='project_remove_member'),

    url(r'^projects/how_it_works/?$', 'how_it_works', {}, name='how_it_works'),
    url(r'^remove_auth_provider/(?P<pk>\d+)?$', 'remove_auth_provider', {}, name='remove_auth_provider'),
)


if EMAILCHANGE_ENABLED:
    urlpatterns += patterns(
        'astakos.im.views',
        url(r'^email_change/?$', 'change_email', {}, name='email_change'),
        url(r'^email_change/confirm/(?P<activation_key>\w+)/?$', 'change_email', {},
            name='email_change_confirm'))

urlpatterns += patterns(
    'astakos.im.target',
    url(r'^login/redirect/?$', 'redirect.login'))

if 'local' in IM_MODULES:
    urlpatterns += patterns(
        'astakos.im.target',
        url(r'^local/?$', 'local.login'),
        url(r'^password_change/?$', 'local.password_change', {
            'post_change_redirect':'profile',
            'password_change_form':ExtendedPasswordChangeForm},
            name='password_change'),
        url(r'^local/password_reset/done$', 'local.password_reset_done'),
        url(r'^local/reset/confirm/done$',
            'local.password_reset_confirm_done')
    )
    urlpatterns += patterns('django.contrib.auth.views',
        url(r'^local/password_reset/?$', 'password_reset', {
            'email_template_name':'registration/password_email.txt',
            'password_reset_form':ExtendedPasswordResetForm,
            'post_reset_redirect':'password_reset/done'}),
        url(r'^local/password_reset_done/?$', 'password_reset_done'),
        url(r'^local/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/?$',
         'password_reset_confirm', {
             'set_password_form':ExtendedSetPasswordForm,
             'post_reset_redirect': 'done'}),
        url(r'^local/password/reset/complete/?$', 'password_reset_complete')
    )

if INVITATIONS_ENABLED:
    urlpatterns += patterns(
        'astakos.im.views',
        url(r'^invite/?$', 'invite', {}, name='invite'))

if 'shibboleth' in IM_MODULES:
    urlpatterns += patterns(
        'astakos.im.target',
        url(r'^login/shibboleth/?$', 'shibboleth.login'),
    )

if 'twitter' in IM_MODULES:
    urlpatterns += patterns(
        'astakos.im.target',
        url(r'^login/twitter/?$', 'twitter.login'),
        url(r'^login/twitter/authenticated/?$',
            'twitter.authenticated'))

if 'google' in IM_MODULES:
    urlpatterns += patterns(
        'astakos.im.target',
        url(r'^login/goggle/?$', 'google.login'),
        url(r'^login/google/authenticated/?$',
            'google.authenticated'))

if 'linkedin' in IM_MODULES:
    urlpatterns += patterns(
        'astakos.im.target',
        url(r'^login/linkedin/?$', 'linkedin.login'),
        url(r'^login/linkedin/authenticated/?$',
            'linkedin.authenticated'))

urlpatterns += patterns(
    'astakos.im.api',
    url(r'^get_services/?$', 'get_services'),
    url(r'^get_menu/?$', 'get_menu'))

urlpatterns += patterns(
    'astakos.im.api',
    url(r'^get_services/?$', 'get_services'),
    url(r'^get_menu/?$', 'get_menu'))

urlpatterns += patterns(
    'astakos.im.api.user',
    url(r'^authenticate/?$', 'authenticate'))

urlpatterns += patterns(
    'astakos.im.api.service',
    url(r'^service/api/v2.0/feedback/?$', 'send_feedback'),
    url(r'^service/api/v2.0/users/?$', 'get_user_info'))