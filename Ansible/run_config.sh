#!/bin/bash

./unimelb-comp90024-2021-grp-58-openrc.sh; ansible-playbook --ask-become-pass config.yaml -i inventory/inventory.ini