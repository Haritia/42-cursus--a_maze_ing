"""This module provides parsing functions for the config file."""

from typing import Any
import sys


def fetch_var(file_name: str) -> dict[str, Any]:
    """Access the defined config file and check each line.

    This captures the required key-value pair for maze
    generation. Some required parameters can be omitted
    from the file and will later get a default value.
    Otherwise, missing parameters will be flagged as
    absent and required.

    Argument:
        - the .txt file containing the required parameters.
    """
    # list the expected parameters to single out unknown ones
    required = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
        "DISPLAY",
        "SEED"
    ]

    # dict to store the key-value pairs extracted
    param: dict[str, Any] = {}

    # trying to access file first before going further
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print(
            f"Oops, that config file ({file_name}) doesn't exist.",
            file=sys.stderr)
        sys.exit()
    except PermissionError:
        print(
            "You don't have the right to access that file.",
            file=sys.stderr)
        sys.exit()

    # file exists/is accessible, proceed to next step
    with open(file_name, "r") as file:
        configs = file.read().splitlines()
        for item in configs:

            # ignore commented lines in the file
            if item.startswith("#"):
                continue

            # only consider key=value lines
            if "=" not in item:
                continue
            key, value = item.split("=", 1)
            key = key.strip()  # rids of trailing space
            value = value.strip()

            # check if a key-pair value has already been stored
            if key in param.keys():
                raise ValueError(f"Duplicate not accepted: {key}")

            # reject unknown parameters
            if key not in required:
                raise ValueError(f"Unknown key: {key}")

            # make sure ENTRY and EXIT are two int separated by a comma
            if key in ["ENTRY", "EXIT"]:
                if "," not in value:
                    raise ValueError(
                        "please provide acceptable"
                        f" coordinates for {key}.")
                x, y = value.split(",", 1)
                param.update({key: (x, y)})
            else:
                param.update({key: value})

            # remove key from required because it's been stored
            required.remove(key)

    # whatever's left will be flagged as missing
    if required:

        # these can be omitted, no need to report them
        if "PERFECT" in required:
            required.remove("PERFECT")
        if "OUTPUT_FILE" in required:
            required.remove("OUTPUT_FILE")
        if "DISPLAY" in required:
            required.remove("DISPLAY")
        if "SEED" in required:
            required.remove("SEED")

        # report whatever's left
        if required:
            raise ValueError(f"Missing config: {required}")

    # output file name must be different from config file name
    if param.get("OUTPUT_FILE") == file_name:
        raise ValueError("use a different file name for output.")

    return (param)


if __name__ == "__main__":
    print(fetch_var("config.txt"))
