"""
A toy MC to simulate the anode signal produced by different structures that emmit light isotropically from the EL mesh.

@Author: G. Martinez Lema
@Date  : 16/10/2014

Notes:
- Root-free version on 06/06/2017
"""

import abc
import numpy as np
import collections


Point3D  = collections.namedtuple("Point3D", "x y z")
Points3D = Point3D

class Source:
    """
    Abstract classgenerating the 2D/3D-shape that produces light at the EL mesh.
    """
    def __init__(self,
                 name,
                 long_diff = 0,
                 tran_diff = 0):
        self.name      = name
        self.long_diff = long_diff
        self.tran_diff = tran_diff

    @abc.abstractmethod
    def get_points(self, n=1):
        """
        Generate a random point within the source structure.
        Must be implemented in each particular case.
        """
        return Points3D([0]*n, [0]*n, [4.5]*n)

    def __call__(self, n=1):
        points = self.get_points(n)
        if self.tran_diff > 0:
            points.x += np.random.gauss(0, self.tran_diff, size=n)
            points.y += np.random.gauss(0, self.tran_diff, size=n)
        if self.long_diff > 0:
            point.x  += np.random.gauss(0, self.long_diff, size=n) 
        return points
    
    def get_example(self):
        return self.get_points(1)


class Pointlike(Source):
    """
    Pointlike source.
    """
    def __init__(self, x0, y0, z0):
        Source.__init__(self, "Pointlike")
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0

    def get_points(self, n=1):
        return Points3D(np.full(n, self.x0),
                        np.full(n, self.y0),
                        np.full(n, self.z0))


class UniformEllipse(Source):
    """
    Uniform ellipse.
    """
    def __init__(self, x_axis, y_axis, x0, y0, z0):
        Source.__init__(self, "Uniform Ellipse")
        self.a  = x_axis
        self.b  = y_axis
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0

    def get_points(self, n=1):
        a, b  = np.sort(np.random.rand(2, n), axis=0)
        r     = np.random.rand(n)**0.5
        theta = 2*np.pi*a/b
        x     = self.a * r * np.cos(theta)
        y     = self.b * r * np.sin(theta)
        z     = np.zeros(n)
        return Points3D(x + self.x0,
                        y + self.y0,
                        z + self.z0)


class GaussianEllipse(Source):
    """
    Gaussian ellipse.
    """
    def __init__(self, sigma_x, sigma_y, x0, y0, z0):
        Source.__init__(self, "Gaussian ellipse")
        self.sigma_x = sigma_x
        self.sigma_y = sigma_y
        self.x0      = x0
        self.y0      = y0
        self.z0      = z0
        
    def get_points(self, n=1):
        x = np.random.Gaus(self.x0, self.sigma_x, size=n)
        y = np.random.Gaus(self.y0, self.sigma_y, size=n)
        z = np.zeros(n) +  self.z0
        return Points3D(x, y, z)


class UniformCircle(UniformEllipse):
    """
    Uniform circle.
    """
    def __init__(self, r, x0, y0, z0):
        UniformEllipse.__init__(self, r, r, x0, y0, z0)
        self.name = "Uniform Circle"


class GaussianCircle(GaussianEllipse):
    """
    Gaussian circle.
    """
    def __init__(self, sigma, x0, y0, z0):
        GaussianEllipse.__init__(self, sigma, sigma, x0, y0, z0)


class StraightLine(Source):
    """
    A straight line in the x-y-z plane.
    """
    def __init__(self, x0, y0, z0, dx, dy, dz):
        Source.__init__(self, "Straight line")
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def get_points(self, n=1):
        r = np.random.rand(n)
        x = r * self.dx + self.x0
        y = r * self.dy + self.y0
        z = r * self.dz + self.z0
        return Point3D(x, y, z)


class LightEmissionSimulator:
    """
    The master class that produces results.
    """
    def __init__(self, source, Nphotons=1e8):
        self.source    = source
        self.Nphotons  = int(Nphotons)
        self.x, self.y = self._Generate()
        self.r         = (self.x**2 + self.y**2)**0.5
        self.phi       = np.arctan2(self.y, self.x)

    def _Generate(self):
        """
        Generate signal in the SiPMs.
        """
        points = self.source             (self.Nphotons)
        thetas = np.arccos(np.random.rand(self.Nphotons))
        phis   = 2* np.pi* np.random.rand(self.Nphotons)

        x = points.z * np.tan(thetas) * np.cos(phis)
        y = x        * np.tan(  phis)

        return x + points.x, y + points.y
