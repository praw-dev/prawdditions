"""Filter capsules are stored here."""
from typing import (
    List,
    Union,
    Any,
    Iterator,
    Callable,
    TypeVar,
)
from praw.models import Comment, Redditor, Submission, Subreddit

_FilterCapsule = TypeVar("_FilterCapsule")


class FilterCapsule:
    """A filter capsule.

    The filter capsule allows you to to have a mini-``AND filter`` or a
    mini-``OR filter`` without having to use another Filterable class.
    For example, if you wanted a filter that had several filters, but some
    are compound filters, such as:

    1. Return posts from users below 7 days that are either approved
    submitters or have over 200 karma.
    2. Return posts from users below 30 days that are either approved
    submitters or have 100 karma.
    3. Return all posts from users above 30 days.

    It would be impossible to use the ``AND filter`` list, as it would be
    impossible to fill the 100 karma requirement due to the 200 karma filter
    from the first hypothetical. A custom function would have to be added
    that does each of the checks, which defeats the whole point of the
    Filterable class being a class built up of individual parts.

    With a filter capsule, each step can become a filter capsule.

    .. code-block:: python

        from prawdditions.filters import (Filterable,
                                          FilterCapsule,
                                          filter_account_age,
                                          filter_account_karma,
                                          filter_approved_submitter)
        submission_stream = reddit.subreddit("mod").stream.submissions()
        filtered_stream =  Filterable(submission_stream)
        sub_filter_1 = FilterCapsule()
        sub_filter_1.add_and_filter(filter_account_age("<", 7, "days"))
        sub_filter_1.add_or_filter(filter_approved_submitter())
        sub_filter_1.add_or_filter(filter_account_karma(">=", 200))
        sub_filter_2 = FilterCapsule()
        sub_filter_2.add_and_filter(filter_account_age("<", 30, "days"))
        sub_filter_2.add_or_filter(filter_approved_submitter())
        sub_filter_2.add_or_filter(filter_account_karma(">=", 100))
        filtered_stream.filter_or(sub_filter_1)
        filtered_stream.filter_or(sub_filter_2)
        filtered_stream.filter_or(filter_account_age(">=", 30, "days"))
        for post in filtered_stream:
            print(post)
    """

    @property
    def and_filters(
        self,
    ) -> List[
        Callable[[Union[Any, Comment, Redditor, Submission, Subreddit]], bool]
    ]:
        """View the list of ``AND filters``."""
        return self._and_list

    @property
    def or_filters(
        self,
    ) -> List[
        Callable[[Union[Any, Comment, Redditor, Submission, Subreddit]], bool]
    ]:
        """View the list of ``OR filters``."""
        return self._or_list

    def __init__(self):
        """Initialize the class."""
        self._and_list = []
        self._or_list = []

    def __len__(self) -> int:
        """Get the length of both filter lists."""
        return len(self.and_filters + self.or_filters)

    def __repr__(self) -> str:
        """Return the REPR of the instance."""
        return "{} with {} AND filters & {} OR filters >".format(
            self.__class__.__name__,
            len(self.and_filters),
            len(self.or_filters),
        )

    def add_filter(
        self,
        filter_type: str,
        filter_func: Callable[
            [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
        ],
    ) -> _FilterCapsule:
        """Add a filter of type ``filter_type`` to the corresponding list.

        This method implements the same logic as :class:`.Filterable`.

        The function returns the class, so it is possible to chain filters,
        like this:

        .. code-block:: python

            from prawdditions.filters import (Filterable, filter_author,
            filter_subreddit)
            subreddit = reddit.subreddit("all")
            filtered_stream =  Filterable(subreddit.stream.submissions)
            sub_filter_1 = FilterCapsule().add_and_filter(
            filter_account_age("<", 7, "days")).add_or_filter(
            filter_approved_submitter()).add_or_filter(
            filter_account_karma(">=", 200))
            for submission in filtered_stream.filter(sub_filter_1):
                print(submission)

        The previous example will filter

        :param filter_type: The filter type, ``or`` & ``and``.
        :param filter_func: The filter function generated from a template or a
            custom function. Must take an item and return a boolean.
        :returns: The class
        """
        if isinstance(filter_func, FilterCapsule):
            filter_func = filter_func.filter
        if filter_type.lower() == "and":
            self.and_filters.append(filter_func)
        elif filter_type.lower() == "or":
            self.or_filters.append(filter_func)
        else:
            raise ValueError(
                "Unrecognized filter type: {!r}. Valid filter types are: "
                "'and' & 'or' filter types.".format(filter_type)
            )
        return self

    def add_and_filter(
        self,
        filter_func: Callable[
            [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
        ],
    ) -> _FilterCapsule:
        """Convenience function to add to the ``AND filters`` list."""
        return self.add_filter("and", filter_func)

    def add_or_filter(
        self,
        filter_func: Callable[
            [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
        ],
    ) -> _FilterCapsule:
        """Convenience function to add to the ``OR filters`` list."""
        return self.add_filter("or", filter_func)

    def filter(
        self, item: Union[Any, Comment, Redditor, Submission, Subreddit]
    ) -> bool:
        """Check the item against the filter rules.

        This method implements the same logic as :class:`.Filterable`.

        :param item: The item to check against the filters.
        :returns: Whether or not the item matched the filters.

        .. warning:: This function should never be directly called. Instead,
            it is provided as a function type that can be used by
            :class:`.Filterable`.
        """
        if len(self.and_filters) > 0:
            and_status = True
            for and_filter in self.and_filters:
                and_status &= and_filter(item)
        else:
            and_status = True
        if len(self.or_filters) > 0:
            or_status = False
            for or_filter in self.or_filters:
                or_status |= or_filter(item)
        else:
            or_status = True
        return and_status and or_status
