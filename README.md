# Publish Terraform module on your private registry
Github Action for publishing your modules on your own registry.

## Customizing
### Inputs

| Name                      | Type   | Description                                                                                                                  |
|---------------------------|--------|------------------------------------------------------------------------------------------------------------------------------|
| `api-key`                 | String | API Key used to authenticate to the registry.                                                                                |
| `hostname`                | String | URL of your registry.                                                                                                        |
| `namespace`               | String | Is the name of a namespace, unique on a particular hostname, that can contain one or more modules that are somehow related.  |
| `module-name`             | String | Name of the module.                                                                                                          |
| `system`                  | String | Name of a remote system that the module is primarily written to target.                                                       |
| `version`                 | String | Version of the module.                                                                                                       |
| `modules-path`            | String | ath where the code is.                                                                                                       |
| `lower-terraform-version` | Number | Lower allowed terraform version.                                                                                                      |
| `higher-terraform-version`| Number | Higher allowed terraform version.                                                                                                      |

## Example usage
```yaml
uses: craftech-io/publish-terraform-module-action@v1.1.1
with:
  api-key: ${{ secrets.API_KEY }}
  hostname: https://registry.acme.com
  namespace: example
  module-name: ecr
  system: aws
  version: v1.0.0
  modules-path: modules/
```
The example above will upload your code to `https://registry.acme.com/example/ecr/aws/1.0.0`

## Optional arguments

### Higher and lower terraform required version
The Action lets you configure a higher, lower or both terraform required version limits. The Action will check if the terraform modules comply with it before zipping and uploading the modules to the registry.

Example: 
```yaml
with:
  ... 
  ...
  lower-terraform-version: 0.99.99
  higher-terraform-version: 1.6.0
```
The values of these variables are not included in the allowed range. With those values, the allowed range will be >1.0.0 and <1.6.0.

### Paths and files to exclude

The Action lets you exclude some folders and files from the package. For example, you want to exclude the test or a random folder that is in your repository.

The paths-files-to-exclude variable value could be a list of folders and files as:

```yaml
with:
  ... 
  ...
  paths-files-to-exclude: "/asd/* test.tf"

```
In the above example, the "asd" folder and subfolders and subfiles will be excluded from the package. Also, the test.tf file from the root directory will be excluded.

# :warning: Public Repository Warning

Please be aware that this is a public repository on GitHub.

## :bulb: Caution:

- Any data you upload or changes you make will be publicly visible.
- Avoid uploading sensitive, personal, or confidential information.
- Review your contributions to ensure they do not reveal anything you wouldn't want to be public.

Remember, your data and contributions can be accessed, used, and shared by anyone around the world.
