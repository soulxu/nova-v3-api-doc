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

from nova import db
from nova.db.sqlalchemy import models
from nova.tests.integrated.v3 import api_sample_base


class AgentsJsonTest(api_sample_base.ApiSampleTestBaseV3):
    extension_name = "os-agents"
    section_name = "Guest Agents"
    section_doc = ("Creates, updates, and deletes guest agents. Use guest "
                   "agents to access files on the disk, configure networking, "
                   "or run other applications or scripts in the guest while "
                   "it runs. This hypervisor-specific extension is not "
                   "currently enabled for KVM. Use of guest agents is "
                   "possible only if the underlying service provider "
                   "uses the Xen driver. ")

    def setUp(self):
        super(AgentsJsonTest, self).setUp()

        fake_agents_list = [{'url': 'xxxxxxxxxxxx',
                             'hypervisor': 'hypervisor',
                             'architecture': 'x86',
                             'os': 'os',
                             'version': '8.0',
                             'md5hash': 'add6bb58e139be103324d04d82d8f545',
                             'id': '1'}]

        def fake_agent_build_create(context, values):
            values['id'] = '1'
            agent_build_ref = models.AgentBuild()
            agent_build_ref.update(values)
            return agent_build_ref

        def fake_agent_build_get_all(context, hypervisor):
            agent_build_all = []
            for agent in fake_agents_list:
                if hypervisor and hypervisor != agent['hypervisor']:
                    continue
                agent_build_ref = models.AgentBuild()
                agent_build_ref.update(agent)
                agent_build_all.append(agent_build_ref)
            return agent_build_all

        def fake_agent_build_update(context, agent_build_id, values):
            pass

        def fake_agent_build_destroy(context, agent_update_id):
            pass

        self.stubs.Set(db, "agent_build_create",
                       fake_agent_build_create)
        self.stubs.Set(db, "agent_build_get_all",
                       fake_agent_build_get_all)
        self.stubs.Set(db, "agent_build_update",
                       fake_agent_build_update)
        self.stubs.Set(db, "agent_build_destroy",
                       fake_agent_build_destroy)

    def test_agent_create(self):
        # Creates a new agent build.
        project = {'url': 'xxxxxxxxxxxx',
                'hypervisor': 'hypervisor',
                'architecture': 'x86',
                'os': 'os',
                'version': '8.0',
                'md5hash': 'add6bb58e139be103324d04d82d8f545'
                }
        response = self._doc_do_post('os-agents', (), (), 'agent-post-req',
                                     project,
                                     api_desc='Creates an agent build')
        project['agent_id'] = 1
        self._verify_response('agent-post-resp', project, response, 201)
        return project

    def test_agent_list(self):
        # Return a list of all agent builds.
        response = self._doc_do_get('os-agents', (), (),
                                    api_desc='Lists all agent builds')
        project = {'url': 'xxxxxxxxxxxx',
                'hypervisor': 'hypervisor',
                'architecture': 'x86',
                'os': 'os',
                'version': '8.0',
                'md5hash': 'add6bb58e139be103324d04d82d8f545',
                'agent_id': 1
                }
        self._verify_response('agents-get-resp', project, response, 200)

    def test_agent_update(self):
        # Update an existing agent build.
        agent_id = 1
        subs = {'version': '7.0',
                'url': 'xxx://xxxx/xxx/xxx',
                'md5hash': 'add6bb58e139be103324d04d82d8f545'}
        response = self._doc_do_put('os-agents/%s', agent_id, 'id',
                                    'agent-update-put-req', subs,
                                    api_desc='Updates an agent build')
        subs['agent_id'] = 1
        self._verify_response('agent-update-put-resp', subs, response, 200)

    def test_agent_delete(self):
        # Deletes an existing agent build.
        agent_id = 1
        response = self._doc_do_delete(
            'os-agents/%s', agent_id, 'id',
            api_desc='Deletes an existing agent build')
        self._verify_no_response('agent-delete', response, 204)
        self.assertEqual(response.status, 204)


class AgentsXmlTest(AgentsJsonTest):
    ctype = "xml"
