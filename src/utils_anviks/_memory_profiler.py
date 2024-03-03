import linecache
import os
import tracemalloc


def tm_snapshot_to_string(snapshot: tracemalloc.Snapshot, key_type='lineno', limit=3) -> str:
    """
    Build a readable string from the given ``tracemalloc`` snapshot.

    :param snapshot: The snapshot to create a string from.
    :param key_type: The key type to group statistics by.
    :param limit: The amount of memory allocations to include in the string.
    :return: The formatted snapshot string.
    """
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)
    report = ["Top %s lines" % limit]

    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        report.append("#%s: %s:%s: %.1f KiB"
                      % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            report.append('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        report.append("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    report.append("Total allocated size: %.1f KiB" % (total / 1024))

    return '\n'.join(report)
