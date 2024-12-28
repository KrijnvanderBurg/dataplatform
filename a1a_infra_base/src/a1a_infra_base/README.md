# a1a_infra_base

### Config as separate classes
Each stack and construct has a separate config class instead of embedding config within the stack or construct. This avoids an issue where classmethods `from_config` calling another `from_config` cause initialization to happen bottom-up (e.g., level 0 → level 1 → level 2 → stack) instead of the required top-down order (stack → level 2 → level 1 → level 0). This misordering causes CDKTF to crash because the scope becomes incorrect after the first construct is created. Separating config from constructs was the only solution after days of trial and error.
