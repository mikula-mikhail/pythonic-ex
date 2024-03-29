
# pip install pydantic
'''Pydantic'''
import json
from pydantic import BaseModel, ValidationError, Field, validator, root_validator
from typing import Optional, List

class Tag(BaseModel):
    id: int
    tag: str = Field(alias='myTag')


class UserWithoutPassword(BaseModel):
    name: str
    email: str

class User(UserWithoutPassword):
    password: str


class City(BaseModel):
    city_id: int
    name: str
    population: int

    # @validator
    # def name_should_be_sbp(cls, v: str) -> str:
    #     if 'spb' not in v.lower():
    #         raise ValueError("Work with SPB!")
    #     return v



input_json = """
{
    "city_id": 123,
    "name": "Moscow",
    "population": 1000000
}
"""


try:
    city = City.parse_raw(input_json)
    print(city)
except ValidationError as e:
    print(e.json())
# print(city, name)


class ISBNMissingError(Exception):
    """Custom error that is raised when both ISBN10 and ISBN13 are missing."""

    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
        super().__init__(message)


class ISBN10FormatError(Exception):
    """Custom error that is raised when ISBN10 doesn't have the right format."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)

# Pydantic really helpfull when you want to add a validation to your data
class Book(BaseModel):
    title: str
    author: str
    publisher: str
    price: float
    isbn_10: Optional[str]
    isbn_13: Optional[str]
    subtitle: Optional[str]

    # validating a whole model
    @pydantic.root_validator(pre=True)
    @classmethod
    def check_isbn10_or_isbn13(cls, value):
        """Make sure there is either an isbn10 or isbn13 value defined."""
        if "isbn_10" not in values and "isbn_13" not in values:
            raise ISBNMissingError(
                title=values["title"],
                message="Document should have either an ISBN10 or ISBN13"
            )
        return values

    # validating a field
    @pydantic.validator("isbn_10")
    @classmethod
    def isbn_10_valid(cls, value):
        """Validator to check whether ISBN10 is valid."""
        chars = [c for c in value if c in "0123456789Xx"]
        if len(chars != 10):
            raise ISBN10FormatError(value=value, message="ISBN10 should be 10 digits.")

        def char_to_int(char: str) -> int:
            if char in "Xx":
                return 10
            return int(char)

        weighted_sum = sum((10 - i) * char_to_int(x) for i, x in enumerate(chars))
        if weighted_sum % 11 != 0:
            raise ISBN10FormatError(
                value=value, message="ISBN10 digit sum should be divisible by 11."
            )
        return value

    class Config:
        """Main function."""

        allow_mutation = False
        anystr_lower = True


def main() -> None:
    """Main function."""

    # Read data from a JSON file
    with open("data.json") as file:
        data = json.load(file)
        # Read data with Pydantic
        books: List[Book] = [Book(**item) for item in data]


if __name__ == '__main__':
    main()
