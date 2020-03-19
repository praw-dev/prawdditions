"""Holds filters for comparing subreddits."""
from datetime import datetime
from time import time
from typing import Union, Any, Callable
from praw.models import Comment, Redditor, Submission, Subreddit
from .base import BaseFilter
from prawdditions.util import get_seconds, symbol_action


class SubredditFilters(BaseFilter):
    """Filter functions that apply to Subreddits.

    .. note:: Since these filters will most likely be used in high-traffic
        streams such as ``r/all``, to prevent the delay of a stream, results
        will be cached. The cache time can be configured by
        :meth:`.set_subreddit_cache`.
    """

    def _set_up_subreddit_cache(self, keep=1000):
        self._subreddit_cache = {}
        self._subreddit_cache_time = 3600
        self._subreddit_cache_keep = keep

    @staticmethod
    def filter_subreddit(
        subreddit: Subreddit,
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Generate a filter function for the given subreddit.

        :param subreddit: An instance of :class:`Subreddit`.
        :return: A filter function for use in :meth:`.Filterable.filter`.
        """

        def filter_func(
            item: [Union[Any, Comment, Redditor, Submission, Subreddit]]
        ) -> bool:
            """Filter an item.

            :param item: The item to check for equality
            """
            return (
                item if isinstance(item, Subreddit) else item.subreddit
            ) == subreddit

        return filter_func

    def filter_subreddit_attribute(
        self,
        attribute: str,
        value: [Union[Any, Comment, Redditor, Submission, Subreddit]],
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter by a specific attribute of :class:`praw.models.Subreddit`.

        .. note:: Results will be cached.

        :param attribute: The attribute to check for.
        :param value: The value that the attribute should equal.
        :returns: A filter function for use in :meth:`.Filterable.filter`.

        .. note:: This function is for equality. If you want to do numerical
            comparisons, such as karma, use :meth:`.filter_subreddit_number`.
        """

        def filter_func(
            item: [Union[Any, Comment, Redditor, Submission, Subreddit]]
        ) -> bool:
            """Filter an item.

            :param item: The item to check for equality
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                getattr(self._subreddit_cache[subreddit]["value"], attribute)
                == value
            )

        return filter_func

    def filter_subreddit_number(
        self, attribute: str, symbol: str, value: Union[Any, int]
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter by a numerical attribute of :class:`praw.models.Subreddit`.

        :param attribute: The attribute to check for.
        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param value: The value that the attribute should compare to.
        :raises: A :class:`ValueError` if the symbol given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """

        def return_function_1(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                len(
                    getattr(
                        self._subreddit_cache[subreddit]["value"], attribute
                    )
                )
                < value
            )

        def return_function_2(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                len(
                    getattr(
                        self._subreddit_cache[subreddit]["value"], attribute
                    )
                )
                > value
            )

        def return_function_3(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                len(
                    getattr(
                        self._subreddit_cache[subreddit]["value"], attribute
                    )
                )
                <= value
            )

        def return_function_4(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                len(
                    getattr(
                        self._subreddit_cache[subreddit]["value"], attribute
                    )
                )
                >= value
            )

        def return_function_5(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                len(
                    getattr(
                        self._subreddit_cache[subreddit]["value"], attribute
                    )
                )
                == value
            )

        def return_function_6(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                len(
                    getattr(
                        self._subreddit_cache[subreddit]["value"], attribute
                    )
                )
                != value
            )

        return symbol_action(
            symbol,
            return_function_1,
            return_function_2,
            return_function_3,
            return_function_4,
            return_function_5,
            return_function_6,
        )

    def filter_subreddit_length(
        self, attribute: str, symbol: str, value: Union[Any, int]
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter by the length of an attribute of a subreddit.

        :param attribute: The attribute to check for.
        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param value: The value that the attribute should compare to.
        :raises: A :class:`ValueError` if the symbol given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """

        def return_function_1(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                getattr(self._subreddit_cache[subreddit]["value"], attribute)
                < value
            )

        def return_function_2(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                getattr(self._subreddit_cache[subreddit]["value"], attribute)
                > value
            )

        def return_function_3(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                getattr(self._subreddit_cache[subreddit]["value"], attribute)
                <= value
            )

        def return_function_4(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                getattr(self._subreddit_cache[subreddit]["value"], attribute)
                >= value
            )

        def return_function_5(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                getattr(self._subreddit_cache[subreddit]["value"], attribute)
                == value
            )

        def return_function_6(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                getattr(self._subreddit_cache[subreddit]["value"], attribute)
                != value
            )

        return symbol_action(
            symbol,
            return_function_1,
            return_function_2,
            return_function_3,
            return_function_4,
            return_function_5,
            return_function_6,
        )

    def filter_subreddit_true(
        self, attribute: str, opposite: bool = False
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter by the boolean value of :class:`praw.models.Subreddit`.

        :param attribute: The attribute to check for.
        :param opposite: Whether to return items that matched False (
            Default: False)
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """

        def filter_func(
            item: [Union[Any, Comment, Redditor, Submission, Subreddit]]
        ) -> bool:
            """Filter an item.

            :param item: The item to check for equality
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            result = bool(
                getattr(self._subreddit_cache[subreddit]["value"], attribute)
            )
            return (not result) if opposite else result

        return filter_func

    def filter_subreddit_age(
        self, symbol: str, amount: int, unit="days"
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter items by subreddit age.

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param amount: The amount of time to compare by.
        :param unit: The unit of time the amount represents. Defaults to 
            ``days``.
        :raises: A :class:`ValueError` if the unit given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.

        Units of time usable by the function:

        * Seconds: ``s``, ``sec``, ``secs``, ``second``, ``seconds``
        * Minutes: ``min``, ``mins``, ``minute``, ``minutes``
        * Hours: ``h``, ``hr``, ``hrs``, ``hour``, ``hours``
        * Days: ``d``, ``day``, ``days``
        * Weeks: ``w``, ``wk``, ``wks``, ``week``, ``weeks``
        * Months: ``mon``, ``month``, ``months``
        * Years: ``y``, ``yr``, ``yrs``, ``year``, ``years``

        .. note:: A month is regarded as 30 days. If finer control is needed on
            the exact amount of days to check for, use a unit of days.

        .. note:: A year is regarded as 365 days. If finer control is needed on
            the exact amount of days to check for, use a unit of days.
        """
        comparison_time = get_seconds(amount, unit)
        if "age" not in self._subreddit_cache:
            self._subreddit_cache["age"] = {}

        def return_function_1(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }
            return (
                datetime.utcnow().timestamp()
                - self._subreddit_cache[subreddit]["value"].created_utc
                < comparison_time
            )

        def return_function_2(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }

            return (
                datetime.utcnow().timestamp()
                - self._subreddit_cache[subreddit]["value"].created_utc
                > comparison_time
            )

        def return_function_3(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }

            return (
                datetime.utcnow().timestamp()
                - self._subreddit_cache[subreddit]["value"].created_utc
                <= comparison_time
            )

        def return_function_4(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }

            return (
                datetime.utcnow().timestamp()
                - self._subreddit_cache[subreddit]["value"].created_utc
                >= comparison_time
            )

        def return_function_5(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }

            return (
                datetime.utcnow().timestamp()
                - self._subreddit_cache[subreddit]["value"].created_utc
                == comparison_time
            )

        def return_function_6(item) -> bool:
            """A return function used by :func:`.symbol_action`.

            :param item: The item to compare with
            :returns: The result of the comparison
            """
            subreddit = str(
                item if isinstance(item, Subreddit) else item.subreddit
            )
            if subreddit not in self._subreddit_cache:
                self._subreddit_cache[subreddit] = {
                    "timestamp": time(),
                    "value": item._reddit.subreddit(subreddit),
                }
            else:
                if (
                    time() - self._subreddit_cache[subreddit]["timestamp"]
                    > self._subreddit_cache_time
                ):
                    self._subreddit_cache[subreddit] = {
                        "timestamp": time(),
                        "value": item._reddit.subreddit(subreddit),
                    }

            return (
                datetime.utcnow().timestamp()
                - self._subreddit_cache[subreddit]["value"].created_utc
                != comparison_time
            )

        return symbol_action(
            symbol,
            return_function_1,
            return_function_2,
            return_function_3,
            return_function_4,
            return_function_5,
            return_function_6,
        )

    def filter_subreddit_subscribers(
        self, symbol: str, amount: int
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filters a subreddit based on the amount of subscribers it has.

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param amount: The amount of subscribers to check for
        :raises: A :class:`ValueError` if the symbol given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_subreddit_number("subscribers", symbol, amount)

    def filter_subreddit_nsfw(
        self, negate=False
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter upon the NSFW status of the subreddit.

        :param negate: Negates the NSFW check, so only non-nsfw subreddits
            are returned.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_subreddit_true("over18", opposite=negate)

    def filter_subreddit_name(self, symbol: str, value: int):
        """Filter by the amount of characters in a subreddit name.

        .. note:: Reddit has a 21-character limit for subreddit names,
            so any values over 21 will not yield anything.

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param value: The amount of characters in a subreddit name.
        :raises: A :class:`ValueError` if the unit given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_subreddit_length("display_name", symbol, value)

    def set_subreddit_cache(self, time: int):
        """Set the subreddit cache time.

        :param time: The amount of time, in seconds, to cache results
        """
        self._subreddit_cache_time = time
