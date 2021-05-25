#!/bin/bash

ansible-playbook --ask-become-pass database.yaml -i inventory/inventory.ini
