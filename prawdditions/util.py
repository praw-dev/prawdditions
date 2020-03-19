"""Constant values and utility function."""
from typing import Any, Union

###############################################################################
#                              Time Manipulation                              #
###############################################################################

# Units

seconds_values = ["s", "sec", "secs", "second", "seconds"]
minutes_values = ["min", "mins", "minute", "minutes"]
hours_values = ["h", "hr", "hrs", "hour", "hours"]
days_values = ["d", "day", "days"]
weeks_values = ["w", "wk", "wks", "week", "weeks"]
months_values = ["mon", "month", "months"]
years_values = ["y", "yr", "yrs", "year", "years"]
all_time_values = (
    seconds_values
    + minutes_values
    + hours_values
    + days_values
    + weeks_values
    + months_values
    + years_values
)

# Time units in seconds

second = 1
minute = second * 60
hour = minute * 60
day = hour * 24
week = day * 7
month = day * 30
year = day * 365


# Time functions


def get_seconds(amount: Union[int, float], unit: str) -> Union[int, float]:
    """Get the representation of the given time value in seconds.

    :param amount: The amount of time to compare by.
    :param unit: The unit of time the amount represents.
    :raises: A :class:`ValueError` if the unit given is invalid.
    :returns: The time converted to seconds.
    """
    unit = unit.lower()
    if unit not in all_time_values:
        raise ValueError(
            "The given unit ({!r}) is invalid. The unit has to be one of "
            "the following: {}".format(
                unit, ", ".join(["{!r}".format(u) for u in all_time_values])
            )
        )
    if unit in seconds_values:
        return amount
    elif unit in minutes_values:
        return amount * minute
    elif unit in hours_values:
        return amount * hour
    elif unit in days_values:
        return amount * day
    elif unit in weeks_values:
        return amount * week
    elif unit in months_values:
        return amount * month
    elif unit in years_values:
        return amount * year


###############################################################################
#                     Miscellaneous Functions and Classes                     #
###############################################################################


def symbol_action(
    symbol: str,
    return_symbol_1: Any,
    return_symbol_2: Any,
    return_symbol_3: Any,
    return_symbol_4: Any,
    return_symbol_5: Any,
    return_symbol_6: Any,
) -> Any:
    """Return 6 different values based on the given symbol.

    Valid symbols:

    :param symbol: The symbol to check for. Currently supported symbols are
        the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
        and ``!=``.
    :param return_symbol_1: The item to return if the symbol is ``<``.
    :param return_symbol_2: The item to return if the symbol is ``>``.
    :param return_symbol_3: The item to return if the symbol is ``<=``.
    :param return_symbol_4: The item to return if the symbol is ``>=``.
    :param return_symbol_5: The item to return if the symbol is ``==``.
    :param return_symbol_6: The item to return if the symbol is ``!=``.
    :raises: :class:`ValueError` if the given symbol is not one of the 6
        supported symbols.
    :returns: Any one of the 6 ``return_symbol`` parameters.
    """
    if symbol not in ["<", ">", "<=", ">=", "==", "!="]:
        raise ValueError(
            "The symbol {!r} is not one of the Python "
            "comaprison symbols: ``<``, ``>``, ``<=``, ``>=``, "
            "``==``, and ``!=``. ".format(symbol)
        )
    elif symbol == "<":
        return return_symbol_1
    elif symbol == ">":
        return return_symbol_2
    elif symbol == "<=":
        return return_symbol_3
    elif symbol == ">=":
        return return_symbol_4
    elif symbol == "==":
        return return_symbol_5
    elif symbol == "!=":
        return return_symbol_6
