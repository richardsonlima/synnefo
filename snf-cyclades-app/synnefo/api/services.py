# Copyright 2013 GRNET S.A. All rights reserved.
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


# Required but undefined fields are given a value of None

cyclades_services = {
    'cyclades_compute': {
        'type': 'compute',
        'component': 'cyclades',
        'prefix': 'compute',
        'public': True,
        'endpoints': [
            {'versionId': 'v2.0',
             'publicURL': None},
        ],
        'resources': {
            'vm': {
                "name": "cyclades.vm",
                "desc": "Number of virtual machines",
                "service_type": "compute",
                "service_origin": "cyclades_compute",
            },
            'total_cpu': {
                "name": "cyclades.total_cpu",
                "desc": "Number of virtual machine processors",
                "service_type": "compute",
                "service_origin": "cyclades_compute",
                "ui_visible": False,
                "api_visible": False,
            },
            'cpu': {
                "name": "cyclades.cpu",
                "desc": "Number of virtual machine processors of running"
                        " servers",
                "service_type": "compute",
                "service_origin": "cyclades_compute",
            },
            'total_ram': {
                "name": "cyclades.total_ram",
                "desc": "Virtual machine memory size",
                "unit": "bytes",
                "service_type": "compute",
                "service_origin": "cyclades_compute",
                "ui_visible": False,
                "api_visible": False,
            },
            'ram': {
                "name": "cyclades.ram",
                "desc": "Virtual machine memory size of running servers",
                "unit": "bytes",
                "service_type": "compute",
                "service_origin": "cyclades_compute",
            },
            'disk': {
                "name": "cyclades.disk",
                "desc": "Virtual machine disk size",
                "unit": "bytes",
                "service_type": "compute",
                "service_origin": "cyclades_compute",
            },
        },
    },

    'cyclades_plankton': {
        'type': 'image',
        'component': 'cyclades',
        'prefix': 'image',
        'public': True,
        'endpoints': [
            {'versionId': 'v1.0',
             'publicURL': None},
        ],
        'resources': {},
    },

    'cyclades_network': {
        'type': 'network',
        'component': 'cyclades',
        'prefix': 'network',
        'public': True,
        'endpoints': [
            {'versionId': 'v2.0',
             'publicURL': None},
        ],
        'resources': {
            'network-private': {
                "name": "cyclades.network.private",
                "desc": "Number of private networks",
                "service_type": "network",
                "service_origin": "cyclades_network",
            },
            'floating_ip': {
                "name": "cyclades.floating_ip",
                "desc": "Number of Floating IP addresses",
                "service_type": "network",
                "service_origin": "cyclades_network",
            },
        },
    },

    'cyclades_vmapi': {
        'type': 'vmapi',
        'component': 'cyclades',
        'prefix': 'vmapi',
        'public': True,
        'endpoints': [
            {'versionId': 'v1.0',
             'publicURL': None},
        ],
        'resources': {},
    },

    'cyclades_helpdesk': {
        'type': 'cyclades_helpdesk',
        'component': 'cyclades',
        'prefix': 'helpdesk',
        'public': False,
        'endpoints': [
            {'versionId': '',
             'publicURL': None},
        ],
    },

    'cyclades_userdata': {
        'type': 'cyclades_userdata',
        'component': 'cyclades',
        'prefix': 'userdata',
        'public': False,
        'endpoints': [
            {'versionId': '',
             'publicURL': None},
        ],
        'resources': {},
    },

    'cyclades_ui': {
        'type': 'cyclades_ui',
        'component': 'cyclades',
        'prefix': 'ui',
        'public': False,
        'endpoints': [
            {'versionId': '',
             'publicURL': None},
        ],
        'resources': {},
    },

    'cyclades_admin': {
        'type': 'admin',
        'component': 'cyclades',
        'prefix': 'admin',
        'public': True,
        'endpoints': [
            {'versionId': '',
             'publicURL': None},
        ],
        'resources': {},
    },

    'cyclades_volume': {
        'type': 'volume',
        'component': 'cyclades',
        'prefix': 'volume',
        'public': True,
        'endpoints': [
            {'versionId': 'v2.0',
             'publicURL': None},
        ],
        'resources': {},
    },
}
