#!/bin/bash

ansible-playbook --ask-become-pass crawler.yaml -i inventory/inventory.ini
