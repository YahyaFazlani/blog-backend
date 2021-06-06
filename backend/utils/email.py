import re


def validate_email(value):
  email_regex = r"^^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$"

  if not re.search(email_regex, value):
    raise ValueError("Invalid email")

  return value
