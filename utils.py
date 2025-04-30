def verify_email(email_id: str) -> bool:
    if "@" not in email_id or "." not in email_id:
        return False
    
    if email_id.split(".")[-1] == "com":
        return True
    
    return False

def email_data_validation(email: dict) -> bool:
    if "id" not in email:
        raise KeyError("The data does not contain an id")
    
    if "from" not in email:
        raise KeyError("The data does not contain an email id")
    
    if not verify_email(email["from"]):
        raise ValueError(f"Given email id is wrong: {email['from']}")
    
    if "subject" not in email:
        raise KeyError("The data does not contain a subject")
    
    if "body" not in email:
        raise KeyError("The data does not contain a body")
    
    if "timestamp" not in email:
        raise KeyError("The data does not contain a timestamp")
    
    return True