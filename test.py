import numpy as np
from mayavi import mlab

################################################################################
# Disable the rendering, to get bring up the figure quicker:
figure = mlab.gcf()
mlab.clf()
figure.scene.disable_render = True

# Creates two set of points using mlab.points3d: red point and
# white points
x1, y1, z1 = np.random.random((3, 10))
red_glyphs = mlab.points3d(x1, y1, z1, color=(1, 0, 0),
                resolution=20)

x2, y2, z2 = np.random.random((3, 10))
white_glyphs = mlab.points3d(x2, y2, z2, color=(0.9, 0.9, 0.9),
                resolution=20)

# Add an outline to show the selected point and center it on the first
# data point.
outline = mlab.outline(line_width=3)
outline.outline_mode = 'cornered'
outline.bounds = (x1[0]-0.1, x1[0]+0.1,
                  y1[0]-0.1, y1[0]+0.1,
                  z1[0]-0.1, z1[0]+0.1)

# Every object has been created, we can reenable the rendering.
figure.scene.disable_render = False
################################################################################


# Here, we grab the points describing the individual glyph, to figure
# out how many points are in an individual glyph.
glyph_points = red_glyphs.glyph.glyph_source.glyph_source.output.points.to_array()


def picker_callback(picker):
    """ Picker callback: this get called when on pick events.
    """
    print('works!!')
    if picker.actor in red_glyphs.actor.actors:
        # Find which data point corresponds to the point picked:
        # we have to account for the fact that each data point is
        # represented by a glyph with several points
        point_id = picker.point_id/glyph_points.shape[0]
#        print('works!!')
        # If the no points have been selected, we have '-1'
        if point_id != -1:
            # Retrieve the coordinnates coorresponding to that data
            # point
            x, y, z = x1[point_id], y1[point_id], z1[point_id]
            # Move the outline to the data point.
            outline.bounds = (x-0.1, x+0.1,
                              y-0.1, y+0.1,
                              z-0.1, z+0.1)


picker = figure.on_mouse_pick(picker_callback)

# Decrease the tolerance, so that we can more easily select a precise
# point.
picker.tolerance = 0.01

mlab.title('Click on red balls')

mlab.show()

def test_plot3d():
    """Generates a pretty set of lines."""
    n_mer, n_long = 6, 11
    dphi = np.pi / 1000.0
    phi = np.arange(0.0, 2 * np.pi + 0.5 * dphi, dphi)
    mu = phi * n_mer
    x = np.cos(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
    y = np.sin(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
    z = np.sin(n_long * mu / n_mer) * 0.5

    l = mlab.plot3d(x, y, z, np.sin(mu), tube_radius=0.025, colormap='Spectral')
    return l

def test_mesh():
    """A very pretty picture of spherical harmonics translated from
    the octaviz example."""
    pi = np.pi
    cos = np.cos
    sin = np.sin
    dphi, dtheta = pi / 250.0, pi / 250.0
    [phi, theta] = np.mgrid[0:pi + dphi * 1.5:dphi,
                               0:2 * pi + dtheta * 1.5:dtheta]
    m0 = 4
    m1 = 3
    m2 = 2
    m3 = 3
    m4 = 6
    m5 = 2
    m6 = 6
    m7 = 4
    r = sin(m0 * phi) ** m1 + cos(m2 * phi) ** m3 + \
        sin(m4 * theta) ** m5 + cos(m6 * theta) ** m7
    x = r * sin(phi) * cos(theta)
    y = r * cos(phi)
    z = r * sin(phi) * sin(theta)

    return mlab.mesh(x, y, z, colormap="bone")


def test_surf():
    """Test surf on regularly spaced co-ordinates like MayaVi."""
    def f(x, y):
        sin, cos = np.sin, np.cos
        return sin(x + y) + sin(2 * x - y) + cos(3 * x + 4 * y)

    x, y = np.mgrid[-7.:7.05:0.1, -5.:5.05:0.05]
    print(y)
    s = mlab.surf(x, y, f)
    #cs = contour_surf(x, y, f, contour_z=0)
    return s

def test_surf2():
    """Test surf on regularly spaced co-ordinates like MayaVi."""
    def f(x, y):
        sin, cos = np.sin, np.cos
        return sin(x + y) + sin(2 * x - y) + cos(3 * x + 4 * y)

    x = np.array([[1,1,1],[2,2,2],[3,3,3]])
    y = np.array([[1,1,1],[1,1,1],[1,1,1]])
    z = np.array([[3,2,1],[3,2,1],[3,2,1]])

    s = mlab.surf(x, y, z, warp_scale='auto')
    #cs = contour_surf(x, y, f, contour_z=0)
    return s

#l = test_surf()
#mlab.show()

