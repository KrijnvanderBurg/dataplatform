"""
Main module for the a1a_infra_base application.

This module initializes the CDKTF application and synthesizes the Terraform backend stack.
"""

from cdktf import App

from a1a_infra_base.stacks.terraform_backend import TerraformBackendStack

if __name__ == "__main__":
    app = App()
    TerraformBackendStack(app, "terraform-backend")
    app.synth()
