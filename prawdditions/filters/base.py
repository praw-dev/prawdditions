"""Base functions shared by all other filter modules."""
from typing import Union, Any, Callable, Type, Tuple
from praw.models import Comment, Redditor, Submission, Subreddit
from prawdditions.util import symbol_action


class BaseFilter:
    """Base Filters.

    .. note:: This class should never be initialized directly. Instead,
        call them from :class:`.Filterable`.
    """

    @staticmethod
    def filter_attribute(
        check_class: Union[
            Type[Union[Any, Comment, Redditor, Submission, Subreddit]],
            Tuple[Type[Union[Any, Comment, Redditor, Submission, Subreddit]]],
        ],
        classattr: str,
        attribute: str,
        value: [Union[Any, Comment, Redditor, Submission, Subreddit]],
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter by a specific attribute of a class.

        :param check_class: The class to check for, such as
            :class:`praw.models.Redditor` or :class`praw.models.Subreddit`.
        :param classattr: The attribute to implement the base function for,
            such as ``author`` for Redditor, ``subreddit`` for Subreddits, etc.
        :param attribute: The attribute to check for.
        :param value: The value that the attribute should equal.
        :returns: A filter function for use in :meth:`.Filterable.filter`.

        .. note:: This function is for equality. If you want to do numerical
            comparisons, such as karma, use :meth:`.BaseFilter.filter_number`.
        """

        def filter_func(
            item: [Union[Any, Comment, Redditor, Submission, Subreddit]]
        ) -> bool:
            """Filter an item.

            :param item: The item to check for equality
            """
            return (
                getattr(
                    (
                        item
                        if isinstance(item, check_class)
                        else getattr(item, classattr)
                    ),
                    attribute,
                )
                == value
            )

        return filter_func

    @classmethod
    def filter_number(
        cls,
        check_class: Union[
            Type[Union[Any, Comment, Redditor, Submission, Subreddit]],
            Tuple[Type[Union[Any, Comment, Redditor, Submission, Subreddit]]],
        ],
        classattr: str,
        attribute: str,
        symbol: str,
        value: Union[Any, int],
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter by a numerical attribute of a class.

        :param check_class: The class to check for, such as
            :class:`praw.models.Redditor` or :class`praw.models.Subreddit`.
        :param classattr: The attribute to implement the base function for,
            such as ``author`` for Redditor, ``subreddit`` for Subreddits, etc.
        :param attribute: The attribute to check for.
        :param symbol: The comparison symbol. Currently supported symbols are
            the Python comparison symbols ``<``, ``>``, ``<=``, ``>=``, ``==``,
            and ``!=``.
        :param value: The value that the attribute should compare to.
        :raises: A :class:`ValueError` if the symbol given is invalid.
        :returns: A filter function for use in :meth:`.Filterable.filter`.
        """
        return symbol_action(
            symbol,
            lambda item: getattr(
                item
                if isinstance(item, check_class)
                else getattr(item, classattr),
                attribute,
            )
            < value,
            lambda item: getattr(
                item
                if isinstance(item, check_class)
                else getattr(item, classattr),
                attribute,
            )
            > value,
            lambda item: getattr(
                item
                if isinstance(item, check_class)
                else getattr(item, classattr),
                attribute,
            )
            <= value,
            lambda item: getattr(
                item
                if isinstance(item, check_class)
                else getattr(item, classattr),
                attribute,
            )
            >= value,
            cls.filter_attribute(classattr, attribute, value),
            lambda item: getattr(
                item
                if isinstance(item, check_class)
                else getattr(item, classattr),
                attribute,
            )
            != value,
        )

    @staticmethod
    def filter_true(
        check_class: Union[
            Type[Union[Any, Comment, Redditor, Submission, Subreddit]],
            Tuple[Type[Union[Any, Comment, Redditor, Submission, Subreddit]]],
        ],
        classattr: str,
        attribute: str,
        opposite: bool = False,
    ) -> Callable[
        [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
    ]:
        """Filter by the boolean value of an attribute.

        :param check_class: The class to check for, such as
            :class:`praw.models.Redditor` or :class`praw.models.Subreddit`.
        :param classattr: The attribute to implement the base function for,
            such as ``author`` for Redditor, ``subreddit`` for Subreddits, etc.
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
            result = bool(
                getattr(
                    item
                    if isinstance(item, check_class)
                    else getattr(item, classattr),
                    attribute,
                )
            )
            return (not result) if opposite else result

        return filter_func
