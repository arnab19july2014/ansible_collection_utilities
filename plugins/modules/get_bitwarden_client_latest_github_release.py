"""
Ansible Module for adding github action secret
"""
#!/usr/bin/env python3

# Copyright: (c) 2022, Arpan Mandal <arpan.rec@gmail.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)
from __future__ import absolute_import, division, print_function

import requests
from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = r"""
---
module: get_bitwarden_client_latest_github_release
"""

def run_module():
    """
    Ansible main module
    """
    module = AnsibleModule(
        argument_spec={}
    )
    url = "https://api.github.com/repos/bitwarden/clients/releases"
    which = "desktop"

    headers = {
        "Accept": "application/vnd.github.v3+json",
    }

    params = {
        "per_page": 50,
    }

    PAGE_NUM = 0
    TAG_FOUND = False

    while True:
        params["page"] = PAGE_NUM
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            return module.fail_json(
                msg="Something went wrong", **response.json()
            )
        response_data = response.json()

        if len(response_data) == 0:
            break
        for release in response_data:
            tag_name = release["tag_name"]
            if tag_name.lower().startswith(f"{which}-"):
                TAG_FOUND = True
                tag_version = tag_name.replace(f"{which}-", "", 1)
                break
        if TAG_FOUND:
            break
        PAGE_NUM += 1

    module.exit_json(**{"msg": tag_version})

def main():
  """
  Python Main Module
  """
  run_module()


if __name__ == "__main__":
  main()
