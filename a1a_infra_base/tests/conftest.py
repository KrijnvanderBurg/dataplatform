"""
Fixtures to reuse.
"""

pytest_plugins: list[str] = [
    "tests.constructs.level0.test_management_lock",
    "tests.constructs.level0.test_resource_group",
    "tests.constructs.level0.test_storage_account",
    "tests.constructs.level0.test_storage_container",
    "tests.constructs.level1.test_storage_account_locked",
    "tests.constructs.level1.test_resource_group_locked",
    "tests.constructs.level2.test_storage_account_with_containers",
    "tests.constructs.level3.test_terraform_backend",
]
