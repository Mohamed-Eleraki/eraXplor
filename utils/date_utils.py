from datetime import datetime, timedelta

def get_start_date_from_user():
    """Prompts the user to enter a start date and validates the input format.

    Continuously prompts the user until a valid date is provided in the specified
    format or until the user interrupts with keyboard input. Handles both format
    validation and user interruption gracefully.

    Returns:
        datetime.date or None: Returns a date object if valid input is provided,
            returns None if the user interrupts the input (Ctrl+C).

    Raises:
        KeyboardInterrupt: If the user interrupts the input prompt (though this is
            caught and handled within the function).

    Example:
        >>> get_end_date_from_user()  # doctest: +SKIP
        Enter an end date value with YYYY-MM-DD format: 2023-05-15
        2023-05-15

        >>> get_end_date_from_user()  # doctest: +SKIP
        Enter an end date value with YYYY-MM-DD format: invalid
        Invalid date format, Please use YYYY-MM-DD
        Enter an end date value with YYYY-MM-DD format: ^C
        User interrupted. Exiting
        None
    """
    while True:
        try:
            date_string = input("Enter a start date value with YYYY-MM-DD format: ")
            date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
            return date_object
        except ValueError:
            print("Invalid date format, Please use YYYY-MM-DD")
        except KeyboardInterrupt:
            print("\nUser interrupted. Exiting")
            break
        
    return None

def get_end_date_from_user():
    """Prompts the user to enter an end date and validates the input format.

    Continuously prompts the user until a valid date is provided in the specified
    format or until the user interrupts with keyboard input. Handles both format
    validation and user interruption gracefully.

    Returns:
        datetime.date or None: Returns a date object if valid input is provided,
            returns None if the user interrupts the input (Ctrl+C).

    Raises:
        KeyboardInterrupt: If the user interrupts the input prompt (though this is
            caught and handled within the function).

    Example:
        >>> date = get_end_date_from_user()
        >>> Enter a start date value with YYYY-MM-DD format: 2023-05-15
        >>> print(date)
        2023-05-15

        >>> date = get_start_date_from_user()
        >>> Enter an end date value with YYYY-MM-DD format: invalid
        >>> Invalid date format, Please use YYYY-MM-DD
        >>> Enter an end date value with YYYY-MM-DD format: ^C
        >>> User interrupted. Exiting
        >>> print(date)
        None
    """
    while True:
        try:
            date_string = input("Enter an end date value with YYYY-MM-DD format: ")
            date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
            return date_object
        except ValueError:
            print("Invalid date format, Please use YYYY-MM-DD")
        except KeyboardInterrupt:
            print("\nUser interrupted. Exiting")
            break
    return None