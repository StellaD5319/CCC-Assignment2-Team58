#!/bin/bash

ansible-playbook --ask-become-pass front-end.yaml -i inventory/inventory.ini
