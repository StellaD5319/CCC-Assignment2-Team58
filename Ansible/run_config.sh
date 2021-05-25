#!/bin/bash

ansible-playbook --ask-become-pass config.yaml -i inventory/inventory.ini
