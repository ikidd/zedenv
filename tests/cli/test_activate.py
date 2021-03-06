"""Test zedenv create command"""

import pytest
import datetime

import zedenv.cli.activate
import zedenv.cli.create

import pyzfscmds.utility
import pyzfscmds.cmd

require_root_dataset = pytest.mark.require_root_dataset
require_zfs_version = pytest.mark.require_zfs_version


@require_root_dataset
@pytest.fixture(scope="function")
def activate_pool_bootfs(root_dataset):

    pool = root_dataset.split("/")[0]
    pyzfscmds.cmd.zpool_set(pool, f"bootfs={root_dataset}")


def create_new_boot_environment(root_dataset):
    parent_dataset = pyzfscmds.utility.dataset_parent(root_dataset)

    boot_environment = f"zedenv-{datetime.datetime.now().isoformat()}"
    verbose = True
    existing = None

    zedenv.cli.create.zedenv_create(parent_dataset, root_dataset,
                                    boot_environment, verbose, existing, None)

    return f"{parent_dataset}/{boot_environment}"


@require_zfs_version
@require_root_dataset
def test_boot_environment_activated(activate_pool_bootfs, root_dataset):

    new_be = create_new_boot_environment(root_dataset)

    verbose = True
    be_root = pyzfscmds.utility.dataset_parent(new_be)
    be_name = pyzfscmds.utility.dataset_child_name(new_be)

    zedenv.cli.activate.zedenv_activate(be_name, be_root, verbose, None, True, False)
