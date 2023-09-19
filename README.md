# Publish Terraform module on your private registry
Github Action for publishing your modules on your own registry.

## Customizing
### Inputs

name: `api-key`
type: String
description: API Key used to authenticate to the registry.

| Name          | Type   | Description                                                                  |
|-------------- |--------|----------------------------------------------------------------------------- |
| `api-key`     | String | API Key used to authenticate to the registry.                                |
| `hostname`    | String | AWS access key id part of the aws credentials. This is used to login to EKS. |
| `namespace`   | String | AWS region to use. This must match the region your desired cluster lies in.  |
| `module-name` | String | The name of the desired cluster.                                             |
| `system`      | String | If you wish to assume an admin role, provide the role arn here to login as.  |
| `version`     | String | Comma separated list of helm values files.                                   |
| `path`        | String | Kubernetes namespace to use.                                                 |
