import matplotlib.pyplot as plt
import numpy             as np

xrange    =   -200, 200
yrange    =   -200, 200
rrange    =      0, max(xrange + yrange)
phirange  = -np.pi, np.pi
xyrange   = xrange,   yrange
rphirange = rrange, phirange

xbins    = 400
ybins    = 400
rbins    = 400
phibins  = 400 
xybins   = xbins,   ybins
rphibins = rbins, phibins

xmin  , xmax   =   xrange
ymin  , ymax   =   yrange
rmin  , rmax   =   rrange
phimin, phimax = phirange

sipm_x  = np.linspace(-195., 195., 40)[:, np.newaxis]
sipm_y  = np.linspace(-195., 195., 40)[:, np.newaxis]
sipm_dx = 0.5
sipm_dy = 0.5


def hist_tracking_plane(*args, **kwargs):
    plt.figure()
    return plt.hist(*args, bins=rbins, range=rrange, **kwargs)


def hist2d(*args, **kwargs):
    plt.figure()
    return plt.hist2d(*args, **kwargs)


def hist2d_tracking_plane(*args, **kwargs):
    return hist2d(*args, bins=xybins, range=xyrange, **kwargs)


def profile_tracking_plane(*args, **kwargs):
    plt.figure()
    return plt.errorbar(*args, **kwargs)


def plot_source(structure, Npoints=1e6):
    """
    Build a 2D-histogram with the z-integrated shape of the
    structure at the EL mesh with the tracking plane granularity.
    """
    Npoints = int(Npoints)
    points  = structure(Npoints) 
    return hist2d_tracking_plane(points.x, points.y)


def plot_xy_distribution(simulator, close=False):
    if not close:
        return hist2d_tracking_plane(simulator.x, simulator.y)

    selection = simulator.r < rmax
    x_mean, x_rms = np.mean(simulator.x[selection]), np.std(simulator.x[selection])
    y_mean, y_rms = np.mean(simulator.y[selection]), np.std(simulator.y[selection])
    return hist2d(simulator.x, simulator.y, bins=xybins, range=((x_mean - 3*x_rms,
                                                                 x_mean + 3*x_rms),
                                                                (y_mean - 3*y_rms,
                                                                 y_mean + 3*y_rms)))


def plot_sipm_xy_response(simulator):
    selection_x = np.apply_along_axis(np.any, 0, np.abs(simulator.x - sipm_x) < sipm_dx)
    selection_y = np.apply_along_axis(np.any, 0, np.abs(simulator.y - sipm_y) < sipm_dx)
    selection   = selection_x & selection_y
    return hist2d_tracking_plane(simulator.x[selection], simulator.y[selection])


def plot_dr_profile(simulator, dr_bins=50, dr_max=30):
    selection = simulator.r < rmax
    x_mean = np.mean(simulator.x[selection])
    y_mean = np.mean(simulator.y[selection])

    if not hasattr(dr_bins, "__iter__"):
        dr_bins = np.linspace(0, dr_max, dr_bins+1)
    dr_range = np.diff(dr_bins) * 0.5

    dr = ((simulator.x[selection] - x_mean)**2 +
          (simulator.y[selection] - y_mean)**2)**0.5


    def profile_in_bin(x):
        count  = np.count_nonzero((dr > x[0]) &
                                  (dr < x[1]))
        sigma  = max(3., np.sqrt(count))
        count /= np.pi * np.sum(x)
        sigma /= np.pi * np.sum(x)
        return np.array([count, sigma])
        
    mean, std_dev = \
    np.apply_along_axis(profile_in_bin, 0,
                        np.stack([dr_bins[:-1],
                                  dr_bins[1: ]]))
    dr_bins = dr_bins[:-1] + dr_range
    return profile_tracking_plane(dr_bins, mean, std_dev, dr_range, fmt=".")


def plot_r_distribution(simulator):
    return hist_tracking_plane((simulator.x**2 + simulator.y**2)**0.5)
