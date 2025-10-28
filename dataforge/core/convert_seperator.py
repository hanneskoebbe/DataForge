def convert_seperator(value):
    # replace comma with point
    if isinstance(value, str):
        value = value.replace(",", ".")
    # try to convert string to float
    try:
        value = float(value)
    except (ValueError, TypeError):
        pass  # record is still a string (pos. nr.)
    return value
