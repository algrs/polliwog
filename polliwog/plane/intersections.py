import numpy as np
import vg
from .._common.shape import columnize


def intersect_segment_with_plane(
    start_points, segment_vectors, points_on_plane, plane_normals
):
    orig_shape = start_points.shape
    start_points, _, transform_result = columnize(
        start_points, (-1, 3), name="start_points"
    )
    vg.shape.check(locals(), "segment_vectors", orig_shape)
    vg.shape.check(locals(), "points_on_plane", orig_shape)
    vg.shape.check(locals(), "plane_normals", orig_shape)

    # Compute t values such that
    # `result = reference_point + t * segment_vectors`.
    t = np.nan_to_num(
        vg.dot(points_on_plane - start_points, plane_normals)
        / vg.dot(segment_vectors, plane_normals)
    )

    intersection_points = start_points + t.reshape(-1, 1) * segment_vectors

    # Discard points which lie past the ends of the segment.
    intersection_points[t < 0] = np.nan
    intersection_points[t > 1] = np.nan

    return transform_result(intersection_points)
