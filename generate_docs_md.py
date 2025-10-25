import os
import re
import griffe
from griffe import load, GoogleOptions


def get_object_by_path(package, path):
    """
    Traverse a dot-separated path and return the object from a Griffe package.
    Args:
        package: The root Griffe package object.
        path: Dot-separated path (e.g., "ibis.expr.types.arrays.ArrayValue").
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


def generate_markdown_for_fn(name, obj):
    assert isinstance(obj, griffe.Function)
    markdown_str = ""
    markdown_str += f"#### `{name}`\n\n"
    markdown_str += f"`{obj.signature()}`\n\n"
    if obj.docstring:
        markdown_str += f"{obj.docstring.value}\n\n"
    return markdown_str


def generate_markdown_for_object(package, obj):
    """
    Generate a Markdown string for a single object.

    For Alias, resolve to Function and generate markdown.
    FOr Class, list Functions and generate markdown.
    """
    assert obj

    markdown_str = ""
    obj_name = obj.path.split('.')[-1]
    markdown_str += f"## `{obj_name}`\n\n"

    # Resolve Alias to Function
    if isinstance(obj, griffe.Alias):
        resolved_obj_name = obj.resolve(obj_name)
        resolved_obj = get_object_by_path(package, resolved_obj_name)
        if isinstance(resolved_obj, griffe.Function):
            markdown_str += generate_markdown_for_fn(obj_name, resolved_obj)
            return markdown_str

    # Class Functions
    markdown_str += "### Methods\n\n"
    for name, member in sorted(obj.members.items()):
        if name.startswith("_"):
            continue  # Skip private/non-callable members
        if not isinstance(member, griffe.Function):
            continue
        markdown_str += generate_markdown_for_fn(name, member)
    markdown_str += "---\n\n"
    return markdown_str

def process_markdown_files(expressions_path, package, output_file="api_reference.md"):
    """Process all markdown files in the directory and write to a single output file."""
    with open(output_file, "w") as f_out:
        # Iterate over all markdown files in the directory
        with os.scandir(expressions_path) as entries:
            for entry in entries:
                if not entry.name.endswith(".md"):
                    continue

                file_path = os.path.join(expressions_path, entry.name)
                with open(file_path, "r") as f_in:
                    content = f_in.read()

                # Write the original content (except ::: lines) to the output
                lines = content.split('\n')
                for line in lines:
                    if line.startswith(":::"):
                        path = line[3:].strip()
                        obj = get_object_by_path(package, path)
                        if obj:
                            f_out.write(generate_markdown_for_object(package, obj))
                        else:
                            f_out.write(f"Error: Could not find object at path `{path}`\n\n---\n\n")
                    else:
                        f_out.write(line + '\n')
                f_out.write("\n")  # Add a newline between files

def main():
    package = load("ibis")
    expressions_path = "docs/api/expressions/"
    output_file = "api_reference.md"
    process_markdown_files(expressions_path, package, output_file)
    print(f"Generated API reference: {output_file}")

if __name__ == "__main__":
    main()
