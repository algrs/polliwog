import numpy as np


def estimate_normal(planar_points):
    from sklearn.decomposition import PCA

    pca = PCA(n_components=3)
    normal = pca.fit(planar_points).components_[-1]
    normal /= np.linalg.norm(normal)
    return normal


def rotation_from_up_and_look(up, look):
    """
    Rotation matrix to rotate a mesh into a canonical reference frame. The
    result is a rotation matrix that will make up along +y and look along +z
    (i.e. facing towards a default opengl camera).

    Note that if you're reorienting a mesh, you can use its `reorient` method
    to accomplish this.

    up: The foot-to-head direction.
    look: The direction the eyes are facing, or the heel-to-toe direction.

    """
    up, look = np.array(up, dtype=np.float64), np.array(look, dtype=np.float64)
    if np.linalg.norm(up) == 0:
        raise ValueError("Singular up")
    if np.linalg.norm(look) == 0:
        raise ValueError("Singular look")
    y = up / np.linalg.norm(up)
    z = look - np.dot(look, y) * y
    if np.linalg.norm(z) == 0:
        raise ValueError("up and look are colinear")
    z = z / np.linalg.norm(z)
    x = np.cross(y, z)
    return np.array([x, y, z])


def euler(xyz, order="xyz", units="deg"):
    if not hasattr(xyz, "__iter__"):
        xyz = [xyz]
    if units == "deg":
        xyz = np.radians(xyz)
    r = np.eye(3)
    for theta, axis in zip(xyz, order):
        c = np.cos(theta)
        s = np.sin(theta)
        if axis == "x":
            r = np.dot(np.array([[1, 0, 0], [0, c, -s], [0, s, c]]), r)
        if axis == "y":
            r = np.dot(np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]), r)
        if axis == "z":
            r = np.dot(np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]]), r)
    return r
