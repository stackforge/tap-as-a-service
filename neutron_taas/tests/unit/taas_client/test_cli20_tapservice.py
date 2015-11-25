# Copyright 2015 NEC Corporation
# All Rights Reserved
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
#
import mock
import sys

from neutron_taas.taas_client import tapservice
from neutronclient import shell
from neutronclient.tests.unit import test_cli20


class CLITestV20TapServiceJSON(test_cli20.CLITestV20Base,
                               tapservice.TapService):

    non_admin_status_resources = [tapservice.TapService.resource]

    def setUp(self):
        self._mock_extension_loading()
        super(CLITestV20TapServiceJSON, self).setUp()

    def _create_patch(self, name, func=None):
        patcher = mock.patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def _mock_extension_loading(self):
        ext_pkg = 'neutronclient.common.extension'
        contrib = self._create_patch(ext_pkg + '._discover_via_entry_points')
        contrib.return_value = [("_tap_service", tapservice)]
        return contrib

    def test_ext_cmd_loaded(self):
        shell.NeutronShell('2.0')
        extension_cmd = {'tap-service-create': tapservice.CreateTapService,
                         'tap-service-delete': tapservice.DeleteTapService,
                         'tap-service-show': tapservice.ShowTapService,
                         'tap-service-list': tapservice.ListTapService}
        self.assertDictContainsSubset(extension_cmd, shell.COMMANDS['2.0'])

    def _test_create_tap_service(self, port_id="random_port",
                                 network_id="random_net", name='',
                                 args_attr=None, position_names_attr=None,
                                 position_values_attr=None):
        cmd = tapservice.CreateTapService(test_cli20.MyApp(sys.stdout), None)
        args_attr = args_attr or []
        position_names_attr = position_names_attr or []
        position_values_attr = position_values_attr or []
        name = name
        tenant_id = 'my-tenant'
        my_id = 'my-id'
        args = ['--tenant-id', tenant_id,
                '--port', port_id,
                '--network', network_id] + args_attr
        position_names = ['port_id', 'network_id'] + position_names_attr
        position_values = [port_id, network_id] + position_values_attr
        self._test_create_resource(self.resource, cmd, name, my_id, args,
                                   position_names, position_values,
                                   tenant_id=tenant_id)

    def test_create_tap_service_mandatory_params(self):
        self._test_create_tap_service()

    def test_create_tap_service_all_params(self):
        name = 'new-tap-service'
        description = 'This defines a new tap-service'
        args_attr = ['--name', name, '--description', description]
        position_names_attr = ['name', 'description']
        position_val_attr = [name, description]
        self._test_create_tap_service(name=name, args_attr=args_attr,
                                      position_names_attr=position_names_attr,
                                      position_values_attr=position_val_attr)
