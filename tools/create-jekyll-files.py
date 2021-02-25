# %%
import glob
import os


def create_dir(dir_name: str):
    """Creates directory. Will not fail if dir_name exists."""
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass


def strip_lines_with_colons(in_file: str, out_file: str):
    """Remove all lines starting with ':::'"""
    with open(in_file, "r") as input, open(out_file, "w") as output:
        for line in input:
            if not line.startswith(":::"):
                output.write(line)


input_files = glob.glob("source/**/*.md")
output_files = [file.replace("source/", "docs/") for file in input_files]
# remove file name from path
output_dirs = {"/".join(file.split("/")[:-1]) for file in output_files}
for dir in output_dirs:
    create_dir(dir)

for (input_file, output_file) in zip(input_files, output_files):
    strip_lines_with_colons(input_file, output_file)

# %%
