# vim: tabstop=4 shiftwidth=4 softtabstop=4
# Copyright 2012 Nebula, Inc.
# Copyright 2013 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo.config import cfg

from nova.tests.integrated.v3 import test_servers

CONF = cfg.CONF


class ShelveJsonTest(test_servers.ServersSampleBase):
    extension_name = "os-shelve"

    def setUp(self):
        super(ShelveJsonTest, self).setUp()
        # Don't offload instance, so we can test the offload call.
        CONF.shelved_offload_time = -1

    def _test_server_action(self, uuid, action):
        response = self._do_post('servers/%s/action' % uuid,
                                 'os-shelve',
                                 {'action': action})
        self.assertEqual(response.status, 202)
        self.assertEqual(response.read(), "")

    def test_shelve(self):
        uuid = self._post_server()
        self._test_server_action(uuid, 'shelve')

    def test_shelve_offload(self):
        uuid = self._post_server()
        self._test_server_action(uuid, 'shelve')
        self._test_server_action(uuid, 'shelve_offload')

    def test_unshelve(self):
        uuid = self._post_server()
        self._test_server_action(uuid, 'shelve')
        self._test_server_action(uuid, 'unshelve')


class ShelveXmlTest(ShelveJsonTest):
    ctype = 'xml'
