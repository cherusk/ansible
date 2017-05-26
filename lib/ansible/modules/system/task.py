#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017  Matthias Tafelmeier

# task is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# task is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: pkt_steering
short_description: Control active kernel scheduled tasks.
description:
     - This module abstracts away kernel scheduled tasks related attributes and other tasks dynamics adjustments.
author:
    - Matthias Tafelmeier (@cherusk)
'''

EXAMPLES = '''
'''

RETURN = '''
'''

import json
import re
from ansible.module_utils.basic import AnsibleModule


class SysInteractor:
    def __init__(self, module):
        self.module = module 

    def effect_assembly(self, proc, _cpus):
        cmd = 'taskset -p %s -c %s' % (proc, _cpus)

        rc, out, err = self.module.run_command(cmd, use_unsafe_shell=True)
        if rc == 0:
            return int(out)
        else:
            self.module.fail_json(msg="CMD: %s \n failed to pin %s" % (cmd, proc))

class Collector:
    def __init__(self, module, args):
        self.module = module 
        self.args = args

    def gather_procs(self):
        pass

class Discriminator:
    def __init__(self):
        pass

def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(required=True, choices=['present', 'absent']),
            assembly=dict(required=False, default=None)
        supports_check_mode=False)
    )

    args = {
        'state': module.params['state'],
        'assembly': module.params['assembly'],
    }

    if args['state'] == "present":
        if args['assembly'] is None:
            module.fail_json(msg="State %s: requires param assembly" % (args['state']))
        
        assembly = json.loads(args['assembly'])


if __name__ == '__main__':
    main()
