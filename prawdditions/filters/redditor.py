"""Holds functions for comparing redditors."""
from datetime import datetime
from time import time
from typing import Union, Any, Callable
from praw.models import Comment, Redditor, Submission, Subreddit
from .base import BaseFilter
from prawdditions.util import get_seconds, symbol_action


class RedditorFilters(BaseFilter):
    """Filter functions that apply to Redditors."""

    def _set_up_redditor_cache(self, keep=1000):
        self._redditor_cache = dict()
        self._redditor_cache_keep = keep

    @staticmethod
    def filter_redditor(
        redditor: Redditor,
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Generate a filter function for the given redditor.

        :param redditor: An instance of :class:`Redditor`.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """

        def filter_func(
            item: [Union[Any, Comment, Redditor, Submission, Subreddit]]
        ) -> bool:
            """Filter an item.

            :param item: The item to check for equality
            """
            return (
                item if isinstance(item, Redditor) else item.author == redditor
            )

        return filter_func

    def filter_redditor_attribute(
        self,
        attribute: str,
        value: [Union[Any, Comment, Redditor, Submission, Subreddit]],
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter by a specific attribute of :class:`praw.models.Redditor`.

        :param attribute: The attribute to check for.
        :param value: The value that the attribute should equal.
        :returns: A filter function for use in :meth:`.Filterable.filter`.

        .. note:: This function is for equality. If you want to do numerical
            comparisons, such as karma, use :meth:`.filter_redditor_number`.
        """

        return self.filter_attribute(Redditor, "author", attribute, value)

    def filter_redditor_number(
        self, attribute: str, symbol: str, value: Union[Any, int]
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter by a numerical attribute of :class:`praw.models.Redditor`.

        :param attribute: The attribute to check for.
        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param value: The value that the attribute should compare to.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_number(Redditor, "author", attribute, symbol, value)

    def filter_redditor_true(
        self, attribute: str, opposite: bool = False
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter by the boolean value of :class:`praw.models.Redditor`.

        :param attribute: The attribute to check for.
        :param opposite: Whether to return items that matched False (
            Default: False)
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_true(Redditor, "author", attribute)

    @staticmethod
    def filter_account_age(
        symbol: str, amount: int, unit="days"
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter items by redditor age.

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
        return symbol_action(
            symbol,
            return_symbol_1=lambda item: datetime.utcnow().timestamp()
            - (item if isinstance(item, Redditor) else item.author).created_utc
            > comparison_time,
            return_symbol_2=lambda item: datetime.utcnow().timestamp()
            - (item if isinstance(item, Redditor) else item.author).created_utc
            < comparison_time,
            return_symbol_3=lambda item: datetime.utcnow().timestamp()
            - (item if isinstance(item, Redditor) else item.author).created_utc
            >= comparison_time,
            return_symbol_4=lambda item: datetime.utcnow().timestamp()
            - (item if isinstance(item, Redditor) else item.author).created_utc
            <= comparison_time,
            return_symbol_5=lambda item: datetime.utcnow().timestamp()
            - (item if isinstance(item, Redditor) else item.author).created_utc
            == comparison_time,
            return_symbol_6=lambda item: datetime.utcnow().timestamp()
            - (item if isinstance(item, Redditor) else item.author).created_utc
            != comparison_time,
        )

    def filter_account_link_karma(
        self, symbol: str, karma: int
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter items based on the redditor's link karma.

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param karma: The amount of karma to compare with.
        :raises: A :class:`ValueError` if the unit given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_redditor_number("link_karma", symbol, karma)

    def filter_account_comment_karma(
        self, symbol: str, karma: int
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter items based on the redditor's comment karma.

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param karma: The amount of karma to compare with.
        :raises: A :class:`ValueError` if the unit given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_redditor_number("comment_karma", symbol, karma)

    @staticmethod
    def filter_account_karma(
        symbol: str, karma: int
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter items based on the redditor's total (link + comment) karma.

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param karma: The amount of karma to compare with.
        :raises: A :class:`ValueError` if the symbol given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return symbol_action(
            symbol,
            lambda item: (
                item if isinstance(item, Redditor) else item.author
            ).link_karma
            + (
                item if isinstance(item, Redditor) else item.author
            ).comment_karma
            < karma,
            lambda item: (
                item if isinstance(item, Redditor) else item.author
            ).link_karma
            + (
                item if isinstance(item, Redditor) else item.author
            ).comment_karma
            > karma,
            lambda item: (
                item if isinstance(item, Redditor) else item.author
            ).link_karma
            + (
                item if isinstance(item, Redditor) else item.author
            ).comment_karma
            <= karma,
            lambda item: (
                item if isinstance(item, Redditor) else item.author
            ).link_karma
            + (
                item if isinstance(item, Redditor) else item.author
            ).comment_karma
            >= karma,
            lambda item: (
                item if isinstance(item, Redditor) else item.author
            ).link_karma
            + (
                item if isinstance(item, Redditor) else item.author
            ).comment_karma
            >= karma,
            lambda item: (
                item if isinstance(item, Redditor) else item.author
            ).link_karma
            + (
                item if isinstance(item, Redditor) else item.author
            ).comment_karma
            != karma,
        )

    def filter_account_muted(
        self, get_mute_info=600
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter items based on the redditor's muted status.

        .. note:: The streamed type must be a type that has a ``subreddit``
            attribute, such as a Comment or Submission.

        .. note:: The authenticated account must be a moderator of any
            subreddits that are filtered with this filter.

        :param get_mute_info: The class will obtain and refresh a list of
            muted accounts every ``get_mute_info`` seconds. (Default: 600
            seconds or 10 minutes).

        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        if "muted" not in self._redditor_cache:
            self._redditor_cache["muted"] = {}

        def filter_func(
            item: [Union[Any, Comment, Redditor, Submission, Subreddit]]
        ) -> bool:
            """Filter an item.

            :param item: The item to check for equality
            """
            subreddit = str(item.subreddit)
            if subreddit not in self._redditor_cache["muted"]:
                self._redditor_cache["muted"][subreddit] = {
                    "timestamp": time(),
                    "data": list(item.subreddit.muted()),
                }
            else:
                cached = self._redditor_cache["muted"][subreddit]["timestamp"]
                if time() - cached > get_mute_info:
                    self._redditor_cache["muted"][subreddit] = {
                        "timestamp": time(),
                        "data": list(item.subreddit.muted()),
                    }
            return (
                item.author in self._redditor_cache["muted"][subreddit]["data"]
            )

        return filter_func

    def filter_account_approved_submitter(
        self, get_approved_submitter_info=600
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter items based on the redditor's approved_submitter status.

        .. note:: The streamed type must be a type that has a ``subreddit``
            attribute, such as a Comment or Submission.

        .. note:: The authenticated account must be a moderator of any
            subreddits that are filtered with this filter.

        :param get_approved_submitter_info: The class will obtain and refresh
            a list of approved submitter accounts every
            ``get_approved_submitter_info``  seconds. (Default: 600 seconds
            or 10 minutes).

        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        if "approved_submitter" not in self._redditor_cache:
            self._redditor_cache["approved_submitter"] = {}

        def filter_func(
            item: [Union[Any, Comment, Redditor, Submission, Subreddit]]
        ) -> bool:
            """Filter an item.

            :param item: The item to check for equality
            """
            subreddit = str(item.subreddit)
            if subreddit not in self._redditor_cache["approved_submitter"]:
                self._redditor_cache["approved_submitter"][subreddit] = {
                    "timestamp": time(),
                    "data": list(item.subreddit.contributor()),
                }
            else:
                cached = self._redditor_cache["approved_submitter"][subreddit][
                    "timestamp"
                ]
                if time() - cached > get_approved_submitter_info:
                    self._redditor_cache["approved_submitter"][subreddit] = {
                        "timestamp": time(),
                        "data": list(item.subreddit.contributor()),
                    }
            return (
                item.author
                in self._redditor_cache["approved_submitter"][subreddit][
                    "data"
                ]
            )

        return filter_func
