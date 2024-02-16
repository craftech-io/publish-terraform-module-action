import hcl2
import semantic_version
import re
import sys
import os

MODULES_PATH = os.environ.get("MODULES_PATH")
HIGHER_VERSION_ALLOWED = os.environ.get("HIGHER_TERRAFORM_VERSION")
LOWEST_VERSION_ALLOWED = os.environ.get("LOWER_TERRAFORM_VERSION")
FILE_EXTENSION_SEARCHED = ".tf"

def look_for_required_versions(modules_path, file_extension_searched):
    """
    This function looks for all the files in the MODULES_PATH path that ends
    with the FILE_EXTENSION_SEARCHED extension, parses these files, extracts
    the required_version from terraform if exists, and
    appends it to the required_versions variable.
    """
    required_versions = []
    for root, _, files in os.walk(modules_path):
        for file in files:
            if file.endswith(file_extension_searched):
                path_to_file = os.path.join(root, file)
                try:
                    with open(path_to_file, "r") as file:
                        parsed_file = hcl2.load(file)
                        # Extract 'required_version' from 'terraform' blocks.
                        if "terraform" in parsed_file:
                            for bloque in parsed_file["terraform"]:
                                if "required_version" in bloque:
                                    required_version = bloque["required_version"]
                                    required_versions.append(required_version)

                except Exception as e:
                    print(f"Error trying to parse the file {path_to_file}: {e}")

    # Duplicated versions are eliminated.
    required_versions = list(set(required_versions))
    # Space between operators and versions is eliminated.
    required_versions = [element.replace(" ", "") for element in required_versions]
    print("The required versions are:", required_versions)
    return required_versions

def analize_versions(
    higher_version_allowed,
    lowest_version_allowed,
    modules_path,
    file_extension_searched,
):
    """
    This function invokes the look_for_required_versions function, for
    each version in the required_versions variable calculates the max and
    min terraform versions, and compares them with the version limits
    configured through HIGHER_VERSION_ALLOWED and LOWEST_VERSION_ALLOWED.
    If some version is outside the limits, the function sends a sys exit = 1
    """
    # The required versions are obtained.
    required_versions = look_for_required_versions(
        modules_path, file_extension_searched
    )

    # The limited range version is configured.
    if higher_version_allowed:
        high_version_allowed = semantic_version.Version.coerce(higher_version_allowed)
        print(f"Higher version allowed: {high_version_allowed}")

    if lowest_version_allowed:
        low_version_allowed = semantic_version.Version.coerce(lowest_version_allowed)
        print(f"Lowest version allowed: {low_version_allowed}")

    # The operators are extracted from the values in the required_versions list.
    pattern = re.compile(r"^[^0-9]{1,2}")

    for version in required_versions:
        not_comprended_higher = f"The version range {version} is not comprended by the higher limit: <{higher_version_allowed}."
        comprended_higher = f"The version range {version} is comprended by the higher limit: <{higher_version_allowed}."
        not_comprended_lower = f"The version range {version} is not comprended by the lower limit: >{lowest_version_allowed}."
        comprended_lower = f"The version range {version} is comprended by the lower limit: >{lowest_version_allowed}."

        match = pattern.match(version)
        operator = match.group()

        # The ~ operator is not comprended by the semantic_version library, so the
        # max and min versions are calculated manually.
        if operator == "~>":
            base_version = version.split("~>")[1].strip()
            segments = base_version.split(".")
            base_version_obj = semantic_version.Version.coerce(base_version)

            min_version = semantic_version.SimpleSpec(f">={base_version}")

            if len(segments) == 2:
                next_major = base_version_obj.next_major()
                max_version = semantic_version.SimpleSpec(f"<{next_major}")
            elif len(segments) == 3:
                next_minor = base_version_obj.next_minor()
                max_version = semantic_version.SimpleSpec(f"<{next_minor}")
            else:
                print(f"The version '{version}' has not a known format.")
                sys.exit(1)

        # The other terraform allowed operators are calculated.
        # https://developer.hashicorp.com/terraform/language/expressions/version-constraints#version-constraint-syntax
        elif (
            operator == "="
            or operator == ">"
            or operator == "<"
            or operator == ">="
            or operator == "<="
            or operator == "!="
        ):
            max_version = semantic_version.SimpleSpec(version)
            min_version = semantic_version.SimpleSpec(version)

        else:
            print(f"The version {version} is not a valid terraform operator.")
            sys.exit(1)

        # The max and min terraform versions calculated are compared with the limits.
        if higher_version_allowed:
            check_higher_compatibility = max_version.match(high_version_allowed)
            if check_higher_compatibility:
                print(not_comprended_higher)
                sys.exit(1)
            else:
                print(comprended_higher)

        if lowest_version_allowed:
            check_base_version_compatibility = min_version.match(low_version_allowed)
            if check_base_version_compatibility:
                print(not_comprended_lower)
                sys.exit(1)
            else:
                print(comprended_lower)


analize_versions(
    HIGHER_VERSION_ALLOWED,
    LOWEST_VERSION_ALLOWED,
    MODULES_PATH,
    FILE_EXTENSION_SEARCHED,
)
