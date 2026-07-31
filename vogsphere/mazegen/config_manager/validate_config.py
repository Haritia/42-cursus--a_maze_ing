"""This module provides a pydantic class for config data validation.

It ultimately will provide the starting argument to create the maze
object.
"""

from .extract_config import fetch_var
from pydantic import BaseModel, Field, model_validator
import random
from typing import Any


class CheckConfig(BaseModel):
    """Data validation for the content fetched from config file.

    This makes sure the parameters passed
    through the config file are legit and respect some
    constraints. This will also add default value to the
    missing or omitted parameters.
    """
    WIDTH: int = Field(..., gt=2, le=200)
    HEIGHT: int = Field(..., gt=2, le=200)
    ENTRY: tuple[int, int] = Field(..., max_length=2)
    EXIT: tuple[int, int] = Field(..., max_length=2)

    # add default value for the following
    OUTPUT_FILE: str = Field(default="default.txt")
    PERFECT: bool = True
    DISPLAY: bool = True
    SEED: int = random.randint(0, 1000)

    @model_validator(mode="before")
    def pre_validation(param: dict[str, Any]) -> dict[str, Any]:
        """Make sure the SEED parameter is defined.

        This sets some valid value if SEED in config
        file is set to None.
        """
        if param.get("SEED") in ["None", "none"]:
            param["SEED"] = 42
        return param

    @model_validator(mode="after")
    def post_validation(self) -> "CheckConfig":
        """Run the validated data through further checks.

        Make sure entry and exit are different cells
        and within bound and that output file name
        is correctly formatted.
        """
        # ENTRY and EXIT must be within WIDTH and HEIGHT
        for point in (self.ENTRY, self.EXIT):
            if point[0] >= self.WIDTH or point[1] >= self.HEIGHT:
                raise ValueError(f"Coordinates {point} out of bound.")

        # make sure output file format is acceptable
        if (
            "." not in self.OUTPUT_FILE or
            "txt" not in self.OUTPUT_FILE.split(".")
        ):
            raise ValueError("Invalid output file name.")

        # ENTRY and EXIT shall be different
        if self.ENTRY == self.EXIT:
            raise ValueError("Entry and exit can't be the same.")
        return self


def full_check(file_name: str) -> CheckConfig:
    """Complete check of the config file's content.

    This first extract the key-value pairs,
    store them in a dict, then pass that dict
    throught the data validation class.
    """
    valid_input = CheckConfig.model_validate(fetch_var(file_name))
    # result = valid_input.model_dump()
    return valid_input


if __name__ == "__main__":
    try:
        full_check("config.txt")
    except ValueError as e:
        print(e)
