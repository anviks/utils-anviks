import linecache
import os
import tracemalloc

BYTES_IN_MEBIBYTE = 1024 ** 2


class CaptureMalloc:
    """
    Context manager to capture memory allocations using ``tracemalloc``.
    
    Upon exiting the context manager, the snapshot is taken and stored in the ``snapshot`` attribute.
    The snapshot is also formatted into a string and stored in the ``snapshot_string`` attribute.
    """

    def __init__(self, max_lines: int = 3):
        """
        Initialize the context manager with the given maximum amount of code lines to include in the snapshot string (sorted by memory usage).
        
        :param max_lines: The maximum amount of code lines to include in the snapshot string. 
        """
        self._max_lines = max_lines
        self.snapshot = None
        self.snapshot_string = ''

    def __enter__(self):
        tracemalloc.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        self.snapshot_string = tm_snapshot_to_string(self.snapshot, limit=self._max_lines)


def tm_snapshot_to_string(snapshot: tracemalloc.Snapshot, key_type='lineno', limit: int = 3) -> str:
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
        report.append("#%s: %s:%s: %.1f MiB"
                      % (index, filename, frame.lineno, stat.size / BYTES_IN_MEBIBYTE))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            report.append('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        report.append("%s other: %.1f MiB" % (len(other), size / BYTES_IN_MEBIBYTE))
    total = sum(stat.size for stat in top_stats)
    report.append("Total allocated size: %.1f MiB" % (total / BYTES_IN_MEBIBYTE))

    return '\n'.join(report)
