from uuid import uuid4


def generate_od_uuid():
    """
    Generates a random 8-character string prefixed with 'od_'.

    Uses UUID4 to generate a random UUID, takes the first 8 characters
    of its hexadecimal representation, and prepends 'od_'.

    Returns:
        str: A string in the format 'od_xxxxxxxx' where xxxxxxxx is
             8 random hexadecimal characters.
    """
    # Generate a random UUID (version 4)
    random_uuid = uuid4()

    # Get the hexadecimal representation of the UUID and take the first 8 characters
    short_uuid = str(random_uuid).replace("-", "")[:8]

    # Prefix with 'od_'
    prefixed_uuid = f"od_{short_uuid}"

    return prefixed_uuid
