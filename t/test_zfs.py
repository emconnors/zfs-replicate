#!/usr/bin/env python

import os
import sys
import pytest
from fabric.api import *

# Add to module search path
app_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_root + "/../lib")

import zfs


#
# Setup "fixture" for dependency injection in test methods
#
# Creates new dataset 'tank/zfsreptest.' Requires zpool tank to
# already exist.

@pytest.fixture(scope="class", autouse=True)
def zfs_instance(request):
    local('zfs create tank/zfsreptest')
    yield zfs.Zfs("tank/zfsreptest",is_remote=False)
    
    # Destroy fixture when done
    local('zfs destroy -r tank/zfsreptest')


#
# Zfs test class
#
class TestZfs:

    # Instance is correct type
    def test_zfs_instance(self, zfs_instance):
        assert isinstance(zfs_instance, zfs.Zfs)

    # List returns expected result
    def test_zfs_list(self, zfs_instance):
        assert zfs_instance.list() == ["tank/zfsreptest"]
    
    # Snapshot is taken successfully
    def test_zfs_snapshot(self, zfs_instance):
        zfs_instance.snapshot("@testsnap")
        assert zfs_instance.exists("tank/zfsreptest@testsnap", type_snapshot=True) == True
