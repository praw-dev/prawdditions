"""Filter items from a PRAW listing or stream."""
from typing import List, Union, Any, Iterator, Callable, TypeVar, Dict
from praw.models import Comment, Redditor, Submission, Subreddit
from .capsule import FilterCapsule
from .redditor import RedditorFilters
from .subreddit import SubredditFilters

# from .user_content import

_Filterable = TypeVar("_Filterable")


class Filterable(RedditorFilters, SubredditFilters):
    """Create a filterable generator/iterator.

    Filterable iterators can be filtered with :meth:`.filter`.
    There are two types of filters, ``AND filters``, and ``OR filters``. In
    order for an object to be yielded, every filter in the list of
    ``AND filters`` and any one filter in the ``OR filters`` list has to
    return True.

    For example, in order to filter all posts to either ``r/AskReddit`` or
    ``r/programming``, but must be by a user who has a karma score >500

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

    @property
    def capsule(self) -> FilterCapsule:
        """Obtain a filter capsule to work with."""
        return FilterCapsule()

    def __init__(
        self,
        generator: Union[
            Iterator[Union[Any, Comment, Redditor, Submission, Subreddit]]
        ],
        cache_items: int = 1000,
    ):
        """Initialize the class.

        :param generator: A generator or iterator that yields
            :class:`praw.models.Comment`\ s, :class:`praw.models.Redditor`\ s,
            :class:`praw.models.Submission`\ s, and/or
            :class:`praw.models.Subreddit`\ s.
        :param cache_items: The amount of items to maintain in the caches (
            Default=1000).

        """
        self.generator = generator
        self._iter = iter(generator)
        self._and_list = []
        self._or_list = []
        self._cache_count = 0
        self._set_up_redditor_cache(keep=cache_items)
        self._set_up_subreddit_cache(keep=cache_items)

    def __iter__(self) -> _Filterable:
        """Return the iterator, also this class.

        :returns: This class
        :meta private:
        """
        return self

    def __len__(self) -> int:
        """Get the length of both filter lists.

        :returns: The combined length of :meth:`.and_filters` and
            :meth:`.or_filters`.
        :meta private:
        """
        return len(self.and_filters + self.or_filters)

    def __next__(self) -> Any:
        """Return the next item in the wrapper iterator after filtering.

        :returns: An object from the wrapped iterator.
        :meta private:
        """
        if self._cache_count >= 2000:
            self.clean_cache()
            self._cache_count = 0
        status = False
        while not status:
            item = next(self._iter)
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
            status = and_status and or_status
        self._cache_count += 1
        return item

    def __repr__(self) -> str:
        """Return the REPR of the instance.

        :returns: The REPR as a string
        :meta private:
        """
        return "<{} {!r} with {} AND filters & {} OR filters>".format(
            self.__class__.__name__,
            self.generator.__class__.__name__,
            len(self.and_filters),
            len(self.or_filters),
        )

    def clean_cache(self):
        """Clean the cache to reduce resource usage.

        .. note:: It is run once every 2000 yields.
        """
        self._redditor_cache["muted"] = dict(
            sorted(
                self._redditor_cache.get("muted", {}),
                key=lambda entry: entry["timestamp"],
            )[0 : self._redditor_cache_keep]
        )
        self._redditor_cache["approved_submitter"] = dict(
            sorted(
                self._redditor_cache.get("approved_submitter", {}),
                key=lambda entry: entry["timestamp"],
            )[0 : self._redditor_cache_keep]
        )
        self._subreddit_cache = dict(
            sorted(
                self._subreddit_cache.items(),
                key=lambda entry: entry["timestamp"],
            )[0 : self._subreddit_cache_keep]
        )

    def filter(
        self,
        filter_type: str,
        filter_func: Callable[
            [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
        ],
    ) -> _Filterable:
        """Add a filter of type ``filter_type`` to the corresponding list.

        The function returns the class, so it is possible to chain filters,
        like this:

        .. code-block:: python

            from prawdditions.filters import (Filterable, filter_author,
            filter_subreddit)
            subreddit = reddit.subreddit("all")
            filtered_stream = Filterable(subreddit.stream.submissions)
            for submission in filtered_stream.filter("and",
            filter_subreddit(reddit.subreddit("test"))).filter("and",
            filter_author(reddit.redditor("spez"))):
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

    def filter_and(
        self,
        filter_func: Callable[
            [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
        ],
    ) -> _Filterable:
        """Convenience function to add to the ``AND filters`` list."""
        return self.filter("and", filter_func)

    def filter_or(
        self,
        filter_func: Callable[
            [Union[Any, Comment, Redditor, Submission, Subreddit]], bool
        ],
    ) -> _Filterable:
        """Convenience function to add to the ``OR filters`` list."""
        return self.filter("or", filter_func)
