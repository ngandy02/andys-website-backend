import re
import json # used for JSON serialization and deserialization into and from Python Data Structures 
from pathlib import Path

NAME = "name"
EMAIL = "email"
SUBMISSIONS_COLLECTION = "submissions"
EMAIL_FORMAT = (
            r'^[A-Za-z0-9]+'            # Start with alnum characters
            r'([_.+-][a-zA-Z0-9]+)*'    # Allow ., +, - followed by alnum char
            r'@[a-zA-Z0-9]+'            # "@" symbol followed by domain name
            r'([.-][a-zA-Z0-9]+)*'      # Allow for subdomains
            r'\.[a-zA-Z]{2,}$'          # End with TLD (min length of 2)
        )

# Local storage: JSON file next to this module (email -> {name, email})
STORAGE_PATH = Path(__file__).resolve().parent / "submissions.json"


def read_submissions() -> dict:
    """
    Read.
    Load submissions from disk. Returns dict mapping email -> {name, email}.
    """
    if not STORAGE_PATH.exists():
        return {}
    with open(STORAGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_submission(email: str) -> dict:
    """
    Delete an submission given an email.
    Returns the value that was associated with the email key 
    which is the specific deleted submission dict
    """
    submissions = read_submissions()
    deleted_acc = submissions.pop(email)
    save_submissions(submissions)
    return deleted_acc


def save_submissions(submissions: dict) -> None:
    """
    Uploads new submission to the database or storage 
    """
    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(submissions, f, indent=2)


def submission_exists(email: str) -> bool:
    """
    Checks if an submission with the email already exists
    """
    submissions = read_submissions()
    if email in submissions:
            return True
    return False


def get_submission(email: str) -> dict | None:
    """
    Return single submission dict if exists, else None.
    """
    return read_submissions().get(email)


def list_submissions() -> list[dict]:
    """Return all submissions as list of {name, email}."""
    return list(read_submissions().values())


def is_valid_email(email: str) -> bool:
    """
    Check if email is a valid email
    """
    if not isinstance(email, str):
        raise ValueError(f"Your email is not a string")
    if re.fullmatch(EMAIL_FORMAT, email):
        return True
    raise ValueError(f"Your email: {email} does not follow correct email format")


def is_valid_name(name: str) -> bool:
    """
    Check if name is valid
    """
    if not isinstance(name, str):
        raise ValueError(f"Name is not a string: {name}")
    
    return True
    

def register(name: str, email: str) -> str:
    """
    Create.
    Register a new submission. Stores in local JSON file. Returns email on success.
    Raises ValueError for invalid input or if email already registered.
    """
    if not is_valid_name(name):
        raise ValueError(f"Name is not a valid name {name}")

    if not is_valid_email(email):
        raise ValueError(f"Email does not follow correct format {email}")

    submissions = read_submissions()
    if submission_exists(email):
        raise ValueError(f"Email already registered: {email}")

    submissions[email] = {NAME: name, EMAIL: email}
    save_submissions(submissions)
    return email 
    
    
