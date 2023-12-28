import hcl2
import semantic_version
import re
import sys
import os

modules_path = os.environ.get('MODULES_PATH')
higher_version_allowed = os.environ.get('HIGHER_TERRAFORM_VERSION')
lowest_version_allowed = os.environ.get('LOWER_TERRAFORM_VERSION')
file_extention_searched = ".tf"

def look_for_required_versions(modules_path, file_extention_searched):
    required_versions = []
    for raiz, dirs, files in os.walk(modules_path):
        for file in files:
            if file.endswith(file_extention_searched):
                path_to_file = os.path.join(raiz, file)
                with open(path_to_file, "r") as file:
                    try:
                        content = file.read()
                        parsed_file = hcl2.loads(content)
                        # Extract 'required_version' from 'terraform' block
                        if "terraform" in parsed_file and isinstance(
                            parsed_file["terraform"], list
                        ):
                            for bloque in parsed_file["terraform"]:
                                if "required_version" in bloque:
                                    required_version = bloque["required_version"]
                                    required_versions.append(required_version)

                    except Exception as e:
                        print(f"Error trying to parse the file {path_to_file}: {e}")

    # Duplicated versions are eliminated
    required_versions = list(set(required_versions))
    required_versions = [element.replace(" ", "") for element in required_versions]
    print("The required versions are:", required_versions)

    return required_versions


def analize_versions(
    higher_version_allowed,
    lowest_version_allowed,
    modules_path,
    file_extention_searched,
):
    # The required versions are obtained.
    required_versions = look_for_required_versions(
        modules_path, file_extention_searched
    )

    # The limited range version is configured.
    higher_version_allowed = semantic_version.Version.coerce(higher_version_allowed)
    print(f"Higher version allowed: {higher_version_allowed}")
    lowest_version_allowed = semantic_version.Version.coerce(lowest_version_allowed)
    print(f"Lowest version allowed: {lowest_version_allowed}")

    patron = re.compile(r"^[^0-9]{1,2}")
    for version in required_versions:
        match = patron.match(version)
        operator = match.group()
        if operator == "~>":
            base_version = version.split("~>")[1].strip()
            segments = base_version.split(".")
            base_version_obj = semantic_version.Version.coerce(base_version)

            if len(segments) == 2:
                next_major = base_version_obj.next_major()
                max_version = semantic_version.SimpleSpec(f"<{next_major}")
                min_version = semantic_version.SimpleSpec(f">={base_version}")

            elif len(segments) == 3:
                next_minor = base_version_obj.next_minor()
                max_version = semantic_version.SimpleSpec(f"<{next_minor}")
                min_version = semantic_version.SimpleSpec(f">={base_version}")
            else:
                print(f"La versión '{version}' no tiene un formato reconocido.")
                sys.exit(1)

            check_higher_compatibility = max_version.match(higher_version_allowed)
            check_base_version_compatibility = min_version.match(lowest_version_allowed)

            if check_higher_compatibility or check_base_version_compatibility:
                print(
                    f"The version range {version} is not comprended by the limits: >{lowest_version_allowed} and <{higher_version_allowed}."
                )
                sys.exit(1)
            else:
                print(
                    f"The version range {version} is comprended by the limits: >{lowest_version_allowed} and <{higher_version_allowed}."
                )

        elif operator == "=":
            base_version = semantic_version.SimpleSpec(version)
            check_higher_compatibility = base_version.match(lowest_version_allowed)
            check_lower_compatibility = base_version.match(higher_version_allowed)
            if check_higher_compatibility or check_lower_compatibility:
                print(
                    f"The version {version} is not comprended by the version range: >{lowest_version_allowed} and <{higher_version_allowed}."
                )
                sys.exit(1)
            print(
                f"The version {version} is comprended by the version range:  >{lowest_version_allowed} and <{higher_version_allowed}."
            )

        elif operator == ">" or operator == "<" or operator == ">=" or operator == "<=":
            print(
                f"The version {version} could be higher than {higher_version_allowed} or lower than {lowest_version_allowed}"
            )
            sys.exit(1)

        else:
            print(
                f"The version {version} is not comprended by the version range: >{lowest_version_allowed} and <{higher_version_allowed}."
            )
            sys.exit(1)

required_terraform_versions = analize_versions(
    higher_version_allowed,
    lowest_version_allowed,
    modules_path,
    file_extention_searched,
)
