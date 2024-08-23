import os
import re
from collections import defaultdict

# This function will search for Android.bp files and find conflicting module definitions
def find_conflicting_modules(base_dir, output_file):
    # Dictionary to store module names and their file paths
    module_definitions = defaultdict(list)

    # Regular expression to match module definitions in Android.bp files
    module_pattern = re.compile(r'name\s*:\s*"(\w+)"')

    # Traverse the directory tree to find Android.bp files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "Android.bp":
                bp_file_path = os.path.join(root, file)

                # Open and read the Android.bp file
                with open(bp_file_path, 'r') as bp_file:
                    for line in bp_file:
                        # Search for module name definitions
                        match = module_pattern.search(line)
                        if match:
                            module_name = match.group(1)
                            # Store the module name and the file path it was found in
                            module_definitions[module_name].append(bp_file_path)

    # Open the output file to write the results
    with open(output_file, 'w') as output:
        conflicts_found = False
        for module_name, locations in module_definitions.items():
            if len(locations) > 1:
                conflicts_found = True
                output.write(f"Conflict found for module '{module_name}':\n")
                for location in locations:
                    output.write(f"  Defined in: {location}\n")
                output.write("\n")

        if not conflicts_found:
            output.write("No conflicts found.\n")

    # Print confirmation message
    if conflicts_found:
        print(f"Conflicts found and written to {output_file}.")
    else:
        print(f"No conflicts found. Results written to {output_file}.")

# Run the script
if __name__ == "__main__":
    # Replace '.' with the base directory you want to search in
    base_dir = '.'
    output_file = 'conflicting_modules.txt'
    find_conflicting_modules(base_dir, output_file)
