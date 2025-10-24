import os
import griffe
from griffe import load, GoogleOptions


def get_object_by_path(package, path):
    """
    Traverse a dot-separated path and return the object from a Griffe package.

    Args:
        package: The root Griffe package object.
        path: Dot-separated path (e.g., "ibis.expr.types.relations.Table").

    Returns:
        The object at the end of the path, or None if not found.
    """
    parts = path.split(".")
    obj = package
    try:
        for part in parts[1:]:  # Skip the root package name (e.g., "ibis")
            obj = obj[part]
        return obj
    except KeyError as e:
        print(f"Error: Could not find '{part}' in path '{path}'")
        return None
    except Exception as e:
        print(f"Error traversing path '{path}': {e}")
        return None


def generate_markdown_for_object(package_name, object_paths, output_file="api_reference.md"):
    """Generate a Markdown file with docstrings for classes and their methods."""
    package = load("ibis")
    with open(output_file, "w") as f:
        f.write(f"# {package_name} API Reference\n\n")
        for path in object_paths:
            obj = get_object_by_path(package, path)
            if obj:
                class_name = path.split('.')[-1]
                f.write(f"## `{class_name}`\n")
                # docstring = obj.docstring.value if obj.docstring else "No docstring available."
                # f.write(f"{docstring}\n\n")

                # List and document methods
                f.write("### Methods\n\n")
                for name, member in sorted(obj.members.items()):
                    if name.startswith("_"):
                        continue  # Skip private/non-callable members
                    if not isinstance(member, griffe.Function):
                        continue

                    f.write(f"#### `{name}`\n\n")
                    f.write(f"`{member.signature()}`\n\n")
                    if member.docstring:
                        docstring = member.docstring.value 
                        f.write(f"{docstring}\n\n")
                f.write("---\n\n")
            else:
                f.write(f"## `{path.split('.')[-1]}`\n")
                f.write(f"Error: Could not find object at path `{path}`\n\n")
                f.write("---\n\n")



def main():
    # options = GoogleOptions(
    #     {
    #         "receives_named_value": False,
    #         "returns_type_in_property_summary": True
    #     }
    # )

    object_paths = [
        "ibis.expr.types.relations.Table",
        "ibis.expr.types.groupby.GroupedTable",
        # "ibis.expr.types.strings.StringValue",
        # "ibis.expr.types.numeric.NumericValue",
        # "ibis.and_",
        # "ibis.array",
        # "ibis.where"
        # Add more paths as needed
    ]
    generate_markdown_for_object("ibis", object_paths)
    # expressions_path = "docs/api/expressions/"
    # with os.scandir(expressions_path) as entries:
    #     expression_files = [entry.name for entry in entries]

    # for expression_file in expression_files:
    #     with open(os.path.join(expressions_path, expression_file), "r") as f:
    #         print(f.read())


if __name__ == "__main__":
    main()