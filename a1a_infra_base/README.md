# Terraform CDK trial Documentation

## What is Terraform CDK?

Terraform CDK (Cloud Development Kit for Terraform) allows developers to define infrastructure using familiar programming languages instead of traditional HCL (HashiCorp Configuration Language). This project specifically utilizes the Python binding of Terraform CDK (CDKTF Python) to define and manage infrastructure as code.

## Project overview
This project serves as my trial for using Terraform CDK with Python, focusing on initializing variables via a custom YAML structure.

## Key Areas of Interest
- YAML Structure: Review the YAML structure to understand variable definitions and usage.
- Configuration Parsing: Focus on how the from_dict methods transform YAML data into configuration objects.

## Challenges with Terraform CDK in Python

Using CDKTF with Python adds complexity compared to native Terraform, as it requires managing a full Python application. My primary concerns include:

1. Maintainability: Future colleagues may struggle to manage a Python-based infrastructure project compared to traditional Terraform.

2. Technical Limitations:
    - The Level 2 data_lake construct (as an example): My goal is to create a default Level 1 (storage) construct and override its attributes using values loaded from YAML. However, this represents a broader challenge: 
    
        I want to build a structure where I can define hardcoded objects while still allowing YAML-based configuration to override any values. The difficulty arises in merging these sources correctly. If an object has required default attributes (e.g., name) that are always set, conflicts occur when both the hardcoded instance and the YAML-derived instance contain them. The primary challenge is determining which values should take precedence.

## Configuration Management

### Separate Configuration Classes
Each stack and construct has a dedicated configuration class rather than embedding configuration directly within the stack or construct. This approach avoids an issue in which:

Calling from_dict recursively within class methods can cause initialization to happen in the wrong order (e.g., Level 0 → Level 1 → Level 2 → Stack instead of Stack → Level 2 → Level 1 → Level 0).

Incorrect initialization order leads to CDKTF crashes due to invalid scope assignments.

Through extensive trial and error, I found that decoupling configuration from constructs was the most reliable way to ensure proper initialization and avoid scope-related issues.