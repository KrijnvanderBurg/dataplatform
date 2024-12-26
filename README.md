dataplatform © 2024 by Krijn van der Burg is licensed under [CC BY 4.0](./LICENSE).

# dataplatform
This repository organizes the key components of the Data Platform into three main bodies.

- **Infrastructure**: Deploying the required infrastructure.
- **Workloads**: Deploying and managing operational workloads.
- **Work in Progress**: Synchronizing ongoing work, ensuring it's available for continued use.

## Repo Structure
### a0a_library
A placeholder for library or framework that other parts of the platform depend on. This could include custom-built libraries or reusable components necessary for the entire stack.

### a1b_infra_base
Handles the deployment of infrastructure using CDKTF (Cloud Development Kit for Terraform) to generate the Terraform plan. This sets up the foundational environment, including compute, storage, and networking components.

Intentionally left room for 01a, in case there needs to be subscription deployment.

### a2a_databricks_jobs
Manages the deployment of all operational Databricks jobs. This product contains and manages the scheduling, execution, and monitoring of Databricks tasks, ensuring that jobs are correctly deployed and run in the environment.

<!-- ### a2b_polars_jobs
Handles the deployment and execution of Polars jobs. This includes all related tasks for processing data using the Polars library, ensuring that workloads relying on this framework are deployed and operational. -->

### a3a_syncwork
Ensures that work in progress (WIP) by users is synchronized, making their ongoing tasks available for continuation. This may include syncing repositories, Databricks environments, or other active projects that need to be resumed.
