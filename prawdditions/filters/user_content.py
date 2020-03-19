from datetime import datetime
from typing import Union, Callable
from praw.models import Comment, Submission
from prawdditions.util import get_seconds, symbol_action


class UserContentFilters:
    """Filter functions that apply to user content (Comments/Submissions)."""

    @staticmethod
    def filter_parent_submission(
        submission: Submission,
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter a stream for comments that are part of the submission.

        :param submission: The parent submission that comments need to be
            part of.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """

        def filter_func(item: [Union[Comment, Submission]]) -> bool:
            """Filter an item.

            :param item: The item to check for equality
            :returns: The status of the check.
            """
            return (
                item if isinstance(item, Submission) else item.submission
            ) == submission

        return filter_func

    @staticmethod
    def filter_parent_comment(comment: Comment) -> Callable[[Comment], bool]:
        """Filter a stream for comments that are part of the comment.

        :param comment: The parent comment that comments need to be part of.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """

        def filter_func(item: Comment) -> bool:
            """Filter an item.

            :param item: The item to check for equality
            """
            return item.parent == comment

        return filter_func

    @staticmethod
    def filter_content_attribute(
        attribute: str, value: str, submission_only: bool = False
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter by the attribute of comments and submissions.

        :param attribute: The attribute to check for.
        :param value: The value that the attribute should equal.
        :param submission_only: Only submissions should be checked for. If
            this parameter is set to True, and a comment is returned,
            it will act on the comment's submission.
        :returns: A filter function for use in :meth:`.Filterable.filter`.

        .. note:: This function is for equality. If you want to do numerical
            comparisons, such as karma, use :meth:`.filter_content_number`.
        """

        def filter_func(item: Union[Comment, Submission]) -> bool:
            """Filter an item.

            :param item: The item to check for equality
            """
            return (
                getattr(
                    item.submission
                    if (isinstance(item, Comment) and submission_only)
                    else item,
                    attribute,
                )
                == value
            )

        return filter_func

    @staticmethod
    def filter_content_number(
        attribute: str, symbol: str, value: int, submission_only: bool = False
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter by a numerical attribute of a Comment or Submission.

        :param attribute: The attribute to check for.
        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param value: The value that the attribute should compare to.
        :param submission_only: Only submissions should be checked for. If
            this parameter is set to True, and a comment is returned,
            it will act on the comment's submission.
        :raises: A :class:`ValueError` if the symbol given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return symbol_action(
            symbol,
            lambda item: getattr(
                item.submission
                if (isinstance(item, Comment) and submission_only)
                else item,
                attribute,
            )
            < value,
            lambda item: getattr(
                item.submission
                if (isinstance(item, Comment) and submission_only)
                else item,
                attribute,
            )
            > value,
            lambda item: getattr(
                item.submission
                if (isinstance(item, Comment) and submission_only)
                else item,
                attribute,
            )
            <= value,
            lambda item: getattr(
                item.submission
                if (isinstance(item, Comment) and submission_only)
                else item,
                attribute,
            )
            >= value,
            lambda item: getattr(
                item.submission
                if (isinstance(item, Comment) and submission_only)
                else item,
                attribute,
            )
            == value,
            lambda item: getattr(
                item.submission
                if (isinstance(item, Comment) and submission_only)
                else item,
                attribute,
            )
            != value,
        )

    @staticmethod
    def filter_content_length(
        attribute: str, symbol: str, value: int, submission_only: bool = False
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter by a numerical attribute of a Comment or Submission.

        :param attribute: The attribute to check for.
        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param value: The value that the attribute should compare to.
        :param submission_only: Only submissions should be checked for. If
            this parameter is set to True, and a comment is returned,
            it will act on the comment's submission.
        :raises: A :class:`ValueError` if the symbol given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return symbol_action(
            symbol,
            lambda item: len(
                getattr(
                    item.submission
                    if (isinstance(item, Comment) and submission_only)
                    else item,
                    attribute,
                )
            )
            < value,
            lambda item: len(
                getattr(
                    item.submission
                    if (isinstance(item, Comment) and submission_only)
                    else item,
                    attribute,
                )
            )
            > value,
            lambda item: len(
                getattr(
                    item.submission
                    if (isinstance(item, Comment) and submission_only)
                    else item,
                    attribute,
                )
            )
            <= value,
            lambda item: len(
                getattr(
                    item.submission
                    if (isinstance(item, Comment) and submission_only)
                    else item,
                    attribute,
                )
            )
            >= value,
            lambda item: len(
                getattr(
                    item.submission
                    if (isinstance(item, Comment) and submission_only)
                    else item,
                    attribute,
                )
            )
            == value,
            lambda item: len(
                getattr(
                    item.submission
                    if (isinstance(item, Comment) and submission_only)
                    else item,
                    attribute,
                )
            )
            != value,
        )

    @staticmethod
    def filter_content_true(
        attribute: str, opposite: bool = False, submission_only: bool = False
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter by the boolean attribute of comments and submissions.

        :param attribute: The attribute to check for.
        :param opposite: Whether to return items that matched False (
            Default: False)
        :param submission_only: Only submissions should be checked for. If
            this parameter is set to True, and a comment is returned,
            it will act on the comment's submission.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """

        def filter_func(item: Union[Comment, Submission]) -> bool:
            """Filter an item.

            :param item: The item to check for equality
            """
            result = bool(
                getattr(
                    item.submission
                    if (isinstance(item, Comment) and submission_only)
                    else item,
                    attribute,
                )
            )
            return (not result) if opposite else result

        return filter_func

    @staticmethod
    def filter_content_age(
        symbol: str, amount: int, unit="days"
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter items by content age.

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
            - item.created_utc
            > comparison_time,
            return_symbol_2=lambda item: datetime.utcnow().timestamp()
            - item.created_utc
            < comparison_time,
            return_symbol_3=lambda item: datetime.utcnow().timestamp()
            - item.created_utc
            >= comparison_time,
            return_symbol_4=lambda item: datetime.utcnow().timestamp()
            - item.created_utc
            <= comparison_time,
            return_symbol_5=lambda item: datetime.utcnow().timestamp()
            - item.created_utc
            == comparison_time,
            return_symbol_6=lambda item: datetime.utcnow().timestamp()
            - item.created_utc
            != comparison_time,
        )

    @staticmethod
    def filter_content_karma(
        symbol: str, karma: int
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter items based on the content's karma (score).

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param karma: The amount of karma to compare with.
        :raises: A :class:`ValueError` if the symbol given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return symbol_action(
            symbol,
            lambda item: item.score < karma,
            lambda item: item.score > karma,
            lambda item: item.score <= karma,
            lambda item: item.score >= karma,
            lambda item: item.score == karma,
            lambda item: item.score != karma,
        )

    def filter_content_gilded(
        self,
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter items based on their gilded status.

        .. note:: Reddit considers an item as gilded if it has been awarded
            either Reddit Gold or Reddit Platinum. If you are looking for
            filters for any awardings, including Reddit Silver,
            use :meth:`.filter_content_awarded`.

        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_content_true("gilded")

    def filter_content_awarded(
        self,
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter items based on their awarding status.

        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_content_true("all_awardings")

    @staticmethod
    def filter_content_awards(
        symbol: str,
        amount_silver=None,
        amount_gold=None,
        amount_platinum=None,
        total_awards=None,
    ):
        """Filter by the amount of awards in a comment/submission.

        .. note:: As Reddit is constantly changing their award catalog,
        only parameters for silver, gold, platinum, and total awards are
        included. In order to filter a specific award,
        use :meth:`.filter_content_award`.

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param amount_silver: The amount of silver awards the content needs to
            contain (Default: 0)
        :param amount_gold: The amount of gold awards the content needs to
            contain (Default: 0)
        :param amount_platinum: The amount of platinum awards the content needs
            to contain (Default: 0)
        :param total_awards: The total amount of awards (including all other
            awards, such as subreddit awards.
        :raises: A :class:`ValueError` if the unit given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """

        def return_function_1(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            silver = item.gildings.get("gid_1", 0)
            gold = item.gildings.get("gid_2", 0)
            platinum = item.gildings.get("gid_3", 0)
            total = item.total_awards_received
            return (
                (
                    (silver < amount_silver)
                    if amount_silver is not None
                    else True
                )
                and ((gold < amount_gold) if amount_gold is not None else True)
                and (
                    (platinum < amount_platinum)
                    if amount_platinum is not None
                    else True
                )
                and (
                    (total < total_awards)
                    if total_awards is not None
                    else True
                )
            )

        def return_function_2(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            silver = item.gildings.get("gid_1", 0)
            gold = item.gildings.get("gid_2", 0)
            platinum = item.gildings.get("gid_3", 0)
            total = item.total_awards_received
            return (
                (
                    (silver > amount_silver)
                    if amount_silver is not None
                    else True
                )
                and ((gold > amount_gold) if amount_gold is not None else True)
                and (
                    (platinum > amount_platinum)
                    if amount_platinum is not None
                    else True
                )
                and (
                    (total > total_awards)
                    if total_awards is not None
                    else True
                )
            )

        def return_function_3(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            silver = item.gildings.get("gid_1", 0)
            gold = item.gildings.get("gid_2", 0)
            platinum = item.gildings.get("gid_3", 0)
            total = item.total_awards_received
            return (
                (
                    (silver <= amount_silver)
                    if amount_silver is not None
                    else True
                )
                and (
                    (gold <= amount_gold) if amount_gold is not None else True
                )
                and (
                    (platinum <= amount_platinum)
                    if amount_platinum is not None
                    else True
                )
                and (
                    (total <= total_awards)
                    if total_awards is not None
                    else True
                )
            )

        def return_function_4(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            silver = item.gildings.get("gid_1", 0)
            gold = item.gildings.get("gid_2", 0)
            platinum = item.gildings.get("gid_3", 0)
            total = item.total_awards_received
            return (
                (
                    (silver >= amount_silver)
                    if amount_silver is not None
                    else True
                )
                and (
                    (gold >= amount_gold) if amount_gold is not None else True
                )
                and (
                    (platinum >= amount_platinum)
                    if amount_platinum is not None
                    else True
                )
                and (
                    (total >= total_awards)
                    if total_awards is not None
                    else True
                )
            )

        def return_function_5(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            silver = item.gildings.get("gid_1", 0)
            gold = item.gildings.get("gid_2", 0)
            platinum = item.gildings.get("gid_3", 0)
            total = item.total_awards_received
            return (
                (
                    (silver == amount_silver)
                    if amount_silver is not None
                    else True
                )
                and (
                    (gold == amount_gold) if amount_gold is not None else True
                )
                and (
                    (platinum == amount_platinum)
                    if amount_platinum is not None
                    else True
                )
                and (
                    (total == total_awards)
                    if total_awards is not None
                    else True
                )
            )

        def return_function_6(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            silver = item.gildings.get("gid_1", 0)
            gold = item.gildings.get("gid_2", 0)
            platinum = item.gildings.get("gid_3", 0)
            total = item.total_awards_received
            return (
                (
                    (silver != amount_silver)
                    if amount_silver is not None
                    else True
                )
                and (
                    (gold != amount_gold) if amount_gold is not None else True
                )
                and (
                    (platinum != amount_platinum)
                    if amount_platinum is not None
                    else True
                )
                and (
                    (total != total_awards)
                    if total_awards is not None
                    else True
                )
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

    @staticmethod
    def filter_content_award(symbol: str, award_name: str, amount: int):
        """Filter based on the amount of a certain award name.

        .. note:: If you want to check if a specific award exists, invoke
            the method as following:

            .. code-block:: python

                filter.filter(filter.filter_content_award(">=", "AWARDNAME", 1)

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param award_name: The name of the award to check for.
        :param amount: The amount of awards to check for.
        :raises: A :class:`ValueError` if the unit given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """

        def return_function_1(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            award_names = [award["name"] for award in item.all_awardings]
            try:
                index = award_names.index(award_name)
                count = item.all_awardings[index]["count"]
            except ValueError:
                count = 0
            return count < amount

        def return_function_2(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            award_names = [award["name"] for award in item.all_awardings]
            try:
                index = award_names.index(award_name)
                count = item.all_awardings[index]["count"]
            except ValueError:
                count = 0
            return count > amount

        def return_function_3(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            award_names = [award["name"] for award in item.all_awardings]
            try:
                index = award_names.index(award_name)
                count = item.all_awardings[index]["count"]
            except ValueError:
                count = 0
            return count <= amount

        def return_function_4(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            award_names = [award["name"] for award in item.all_awardings]
            try:
                index = award_names.index(award_name)
                count = item.all_awardings[index]["count"]
            except ValueError:
                count = 0
            return count >= amount

        def return_function_5(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            award_names = [award["name"] for award in item.all_awardings]
            try:
                index = award_names.index(award_name)
                count = item.all_awardings[index]["count"]
            except ValueError:
                count = 0
            return count == amount

        def return_function_6(item: Union[Submission, Comment]) -> bool:
            """Return function for comparison."""
            award_names = [award["name"] for award in item.all_awardings]
            try:
                index = award_names.index(award_name)
                count = item.all_awardings[index]["count"]
            except ValueError:
                count = 0
            return count != amount

        return symbol_action(
            symbol,
            return_function_1,
            return_function_2,
            return_function_3,
            return_function_4,
            return_function_5,
            return_function_6,
        )

    @staticmethod
    def filter_content_reply_count(symbol: str, amount: int):
        """Filter by the amount of replies that a comment/submission has.

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param amount: The amount of replies to check for.
        :raises: A :class:`ValueError` if the unit given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return symbol_action(
            symbol,
            lambda item: (
                len(item.comments)
                if isinstance(item, Submission)
                else len(item.replies)
            )
            < amount,
            lambda item: (
                len(item.comments)
                if isinstance(item, Submission)
                else len(item.replies)
            )
            > amount,
            lambda item: (
                len(item.comments)
                if isinstance(item, Submission)
                else len(item.replies)
            )
            <= amount,
            lambda item: (
                len(item.comments)
                if isinstance(item, Submission)
                else len(item.replies)
            )
            >= amount,
            lambda item: (
                len(item.comments)
                if isinstance(item, Submission)
                else len(item.replies)
            )
            == amount,
            lambda item: (
                len(item.comments)
                if isinstance(item, Submission)
                else len(item.replies)
            )
            != amount,
        )

    def filter_submission_selftext(
        self,
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter submissions based on whether or not they are selftexts.

        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_content_true("is_self", submission_only=True)

    def filter_submission_selftext_length(
        self, symbol: str, value: int
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter by the length of a submission selftext.

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param value: The value that the attribute should compare to.
        :raises: A :class:`ValueError` if the symbol given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_content_length(
            "selftext", symbol, value, submission_only=True
        )

    def filter_submission_title_length(
        self, symbol: str, value: int
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter by the length of a submission title.

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param value: The value that the title should compare to.
        :raises: A :class:`ValueError` if the symbol given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_content_length(
            "title", symbol, value, submission_only=True
        )

    def filter_submission_url(
        self,
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter submissions based on whether or not they are URL posts.

        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_content_true("is_self", opposite=True)

    def filter_submission_nsfw(self, negate=False):
        """Filter upon the NSFW status of the submission.

        :param negate: Negates the NSFW check, so only non-nsfw submissions
            are returned.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_content_true(
            "over_18", opposite=negate, submission_only=True
        )

    def filter_submission_reddit_image(
        self, negate=False
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter submissions made to ``i.redd.it``.

        :param negate: Return items that are not from ``i.redd.it``.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        redditmedia = self.filter_content_true(
            "is_reddit_media_domain", submission_only=True
        )
        video = self.filter_content_true("is_video", submission_only=True)

        def filter_func(item: [Union[Comment, Submission]]) -> bool:
            """Filter an item.

            :param item: The item to check.
            :returns: The status of the check.
            """
            result = redditmedia(item) and not (video(item))
            return (not result) if negate else result

        return filter_func

    def filter_submission_reddit_video(
        self, negate=False
    ) -> Callable[[Union[Submission, Comment]], bool]:
        """Filter submissions made to ``v.redd.it``.

        :param negate: Return items that are not from ``i.redd.it``.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        redditmedia = self.filter_content_true(
            "is_reddit_media_domain", submission_only=True
        )
        video = self.filter_content_true("is_video", submission_only=True)

        def filter_func(item: [Union[Comment, Submission]]) -> bool:
            """Filter an item.

            :param item: The item to check.
            :returns: The status of the check.
            """
            result = redditmedia(item) and (video(item))
            return (not result) if negate else result

        return filter_func

    def filter_comment_body(
        self, symbol: str, value: int
    ) -> Callable[[Comment], bool]:
        """Filter based on the length of the comment's body.

        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param value: The value that the body should compare to.
        :raises: A :class:`ValueError` if the symbol given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return self.filter_content_length("body", symbol, value)
