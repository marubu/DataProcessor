def tagFilter(run_list, tag):
    """
    >>> run_list = [{"path":"hoge", "meta":{"tags":["tag1", "tag2"]}},
    ...     {"path":"hoge2", "meta":{"tags":["tag1", "tag4"]}},
    ...     {"path":"hoge3", "meta":{"tags":["tag2", "tag2"]}},
    ...     {"path":"hoge4", "meta":{"tags":["tag12", "tag3"]}},
    ...     {"path":"hoge5", "meta":{"tags":["tag1", "tag2"]}}]
    >>> tagFilter(run_list, "tag1") == [
    ...     {'path':'hoge', 'meta':{'tags':['tag1', 'tag2']}},
    ...     {'path':'hoge2', 'meta':{'tags':['tag1', 'tag4']}},
    ...     {'path':'hoge5', 'meta':{'tags':['tag1', 'tag2']}}]
    True
    >>>
    """
    return [run for run in run_list if tag in run["meta"]["tags"]]



def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
