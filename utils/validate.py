import re


def validate_email(value):
  email_regex = re.compile(r"^^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$")

  if not re.search(email_regex, value):
    raise ValueError("Invalid email")

  return value

def validate_url(value):
  url_regex = re.compile(
      r'^(?:http|ftp)s?://'  # http:// or https://
      # domain...
      r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
      r'localhost|'  # localhost...
      r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
      r'(?::\d+)?'  # optional port
      r'(?:/?|[/?]\S+)$', re.IGNORECASE)

  if not re.search(url_regex, value):
    raise ValueError("Invalid URL")

  return value
