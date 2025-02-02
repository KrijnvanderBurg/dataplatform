"""
Fixtures to reuse.
"""

pytest_plugins: list[str] = [
    "tests.constructs.level0.test_management_lock",
    "tests.constructs.level0.test_resource_group",
    "tests.constructs.level0.test_storage_account",
    "tests.constructs.level0.test_storage_container",
]
