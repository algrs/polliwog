import numpy as np
import vg


def partition(v, partition_size=5):
    """

    params:
        v:
            V x N np.array of points in N-space

        partition_size:
            how many partitions intervals for each segment?

    Fill in the line segments determined by v with equally
    spaced points - the space for each segment is determined
    by the length of the segment and the supplied partition size.

    """
    src = np.arange(len(v) - 1)
    dst = src + 1

    diffs = v[dst] - v[src]

    sqdis = np.square(diffs)
    dists = np.sqrt(np.sum(sqdis, axis=1))

    unitds = diffs / dists[:, np.newaxis]
    widths = dists / partition_size

    domain = widths[:, np.newaxis] * np.arange(0, partition_size)
    domain = domain.flatten()[:, np.newaxis]

    points = np.repeat(v[:-1], partition_size, axis=0)
    unitds = np.repeat(unitds, partition_size, axis=0)

    filled = points + (unitds * domain)

    return np.vstack((filled, v[-1]))


def partition_segment(p1, p2, n_samples, endpoint=True):
    """
    For two points in n-space, return an np.ndarray of equidistant partition
    points along the segment determined by p1 & p2.

    The total number of points returned will be n_samples. When n_samples is
    2, returns the original points.

    When endpoint is True, p2 is the last point. When false, p2 is excluded.

    Partition order is oriented from p1 to p2.

    Args:
        p1, p2:
            1 x N vectors

        partition_size:
            size of partition. should be >= 2.

    """
    if not isinstance(n_samples, int):
        raise TypeError("partition_size should be an int.")
    elif n_samples < 2:
        raise ValueError("partition_size should be bigger than 1.")

    return (p2 - p1) * np.linspace(0, 1, num=n_samples, endpoint=endpoint)[
        :, np.newaxis
    ] + p1


def partition_segment_old(p1, p2, partition_size=5):
    """
    Deprecated. Please use partition_segment.

    For two points in n-space, return an np.ndarray of partition points at equal widths
    determined by 'partition_size' on the interior of the segment determined by p1 & p2.

    Accomplished by partitioning the segment into 'partition_size' sub-intervals.

    Partition order is oriented from p1 to p2.

    Args:
        p1, p2:
            1 x N vectors

        partition_size:
            size of partition. should be > 1.
    """

    if not isinstance(partition_size, int):
        raise TypeError("partition_size should be an int.")
    elif partition_size < 2:
        raise ValueError("partition_size should be bigger than 1.")

    dist = np.linalg.norm(p1 - p2)

    unit_direction = (p2 - p1) / dist
    partition_width = dist / partition_size

    domain = partition_width * np.arange(1, partition_size)

    return p1 + unit_direction * domain[:, np.newaxis]


def closest_point_of_line_segment(points, start_points, segment_vectors):
    # Adapted from public domain algorithm
    # https://gdbooks.gitbooks.io/3dcollisions/content/Chapter1/closest_point_on_line.html
    k = vg.shape.check(locals(), "points", (-1, 3))
    vg.shape.check(locals(), "start_points", (k, 3))
    vg.shape.check(locals(), "segment_vectors", (k, 3))

    # Compute t values such that
    # `result = reference_point + t * vector_along_line`.
    square_of_segment_lengths = vg.dot(segment_vectors, segment_vectors)
    # Degenerate segments will cause a division by zero, so handle that.
    t = np.nan_to_num(
        vg.dot(points - start_points, segment_vectors) / square_of_segment_lengths
    )

    # When `0 <= t <= 1`, the point is on the segment. When `t < 0`, the
    # closest point is the segment start. When `t > 1`, the closest point is
    # the segment end.
    #
    # Start with the `0 <= t <= 1 case`, then use masks to apply the clamp.
    result = start_points + t.reshape(-1, 1) * segment_vectors

    clamped_to_start_point = t < 0
    result[clamped_to_start_point] = start_points[clamped_to_start_point]

    clamped_to_end_point = t > 1
    result[clamped_to_end_point] = (
        start_points[clamped_to_end_point] + segment_vectors[clamped_to_end_point]
    )

    return result
