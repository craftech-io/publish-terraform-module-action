# Publish Terraform module on your private registry
Github Action for publishing your modules on your own registry.

## Customizing
### Inputs

| Name          | Type   | Description                                                                                                                  |
|-------------- |--------|------------------------------------------------------------------------------------------------------------------------------|
| `api-key`     | String | API Key used to authenticate to the registry.                                                                                |
| `hostname`    | String | URL of your registry.                                                                                                        |
| `namespace`   | String | Is the name of a namespace, unique on a particular hostname, that can contain one or more modules that are somehow related.  |
| `module-name` | String | Name of the module.                                                                                                          |
| `system`      | String |Name of a remote system that the module is primarily written to target.                                                       |
| `version`     | String | Version of the module.                                                                                                       |
| `path`        | String | ath where the code is.                                                                                                       |

## Example usage
```yaml
uses: craftech-io/publish-terraform-module-action@v1
with:
  api-key: ${{ secrets.API_KEY }}
  hostname: https://registry.acme.com
  namespace: example
  module-name: ecr
  system: aws
  version: v1.0.0
  path: modules/
```

The example above will upload your code to `https://registry.acme.com/example/ecr/aws/v1.0.0`