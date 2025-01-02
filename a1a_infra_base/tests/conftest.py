"""
Fixtures to reuse.


==============================================================================
Copyright Krijn van der Burg. All rights reserved.

This software is proprietary and confidential. No reproduction, distribution,
or transmission is allowed without prior written permission. Unauthorized use,
disclosure, or distribution is strictly prohibited.

For inquiries and permission requests, contact Krijn van der Burg at
krijnvdburg@protonmail.com.
==============================================================================
"""

pytest_plugins: list[str] = [
    "tests.constructs.level0.test_management_lock",
    "tests.constructs.level0.test_resource_group",
    "tests.constructs.level0.test_storage_account",
    "tests.constructs.level0.test_storage_container",
    "tests.constructs.level1.test_terraform_backend",
]
