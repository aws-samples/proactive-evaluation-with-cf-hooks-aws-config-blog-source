## Proactively Evaluate Resources With AWS CloudFormation Hooks and AWS Config Rules

[Blog post]() demonstrating how to proactively evaluate AWS resources compliance with pre-defined AWS Managed Config rules and AWS CloudFormation Hooks. 

This repository contains the following files:

- AWS Config rules:
    - [rds-instance-public-config-rule.json](https://github.com/aws-samples/proactive-evaluation-with-cf-hooks-aws-config-blog-source/blob/main/config-rules/rds-instance-public-config-rule.json)
    - [rds-storage-encrypted-config-rule.json](https://github.com/aws-samples/proactive-evaluation-with-cf-hooks-aws-config-blog-source/blob/main/config-rules/rds-storage-encrypted-config-rule.json)
- AWS Cloudformation:
    - [Hook Schema](https://github.com/aws-samples/proactive-evaluation-with-cf-hooks-aws-config-blog-source/blob/main/demo-testing-configrulehook.json)
    - [Hook handler code](https://github.com/aws-samples/proactive-evaluation-with-cf-hooks-aws-config-blog-source/blob/main/src/handlers.py)
    - [Test template](https://github.com/aws-samples/proactive-evaluation-with-cf-hooks-aws-config-blog-source/blob/main/templates/rds.yaml)




## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

