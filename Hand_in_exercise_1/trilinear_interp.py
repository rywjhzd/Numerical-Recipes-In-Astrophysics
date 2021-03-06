import numpy as np
from integration import midpoint

# Define the range of input parameters as requied.
new_a = np.arange(1.1, 2.6, 0.1)
new_b = np.arange(0.5, 2.1, 0.1)
new_c = np.arange(1.5, 4.1, 0.1)

# Calculate A as a funtion of a,b,c.
def multi_A(a, b, c):
    A = np.zeros((len(a), len(b), len(c)))
    for i in range(len(a)):
        for j in range(len(b)):
            for k in range(len(c)):
                new_n_1d = lambda x:4*np.pi*x**2*(x/b[j])**(a[i]-3)*np.e**(-(x/b[j])**c[k])
                A[i][j][k] = 1/midpoint(new_n_1d, 0, 5, 100)
    return A

# Return new_A as a triple array.
new_A = multi_A(new_a, new_b, new_c)

# Define 3D interpolator.
def trilinear_interpolation(vertex, index, a, b, c):
    """
    vertex   ...  3d arrays wanted to interpolate
    index       ...  indices at which the vertex will be evaluated.

    Find the eight corners of a cube that surround our point of interest.
    Then perform interpolation between the upper and lower edges of front and back sides.
    This will give us interplolations of four lines so that we can find four points along
    them. Repeat the above process between the interpolation of the upper lower points found
    by the previous interpolation. This will return two points of the top and bottom sides.
    Perform the interpolation the third time and this will give the desired point within the boundary.
    The product of the value at the desired point and the entire volume is equal to the sum
    of the products of the value at each corner and the partial volume diagonally opposite the corner.

    Here I give the result of my interpolation if choosing x,y,z = 14, 15, 25,
    in comparison with the output of new_A:

    >>> new_A[14][15][25]
    0.02773651611406061
    >>> xyz = [(14),(15),(25)]
    >>> trilinear_interpolation(new_A, xyz, 0, 0, 0)
    array([0.02773652])
    >>> trilinear_interpolation(new_A, xyz, 0, 0, 0)[0]
    0.02773651611406061
    >>> trilinear_interpolation(new_A, xyz, 3.323, 1.6532, 3.657)[0]
    0.030102252960272247

    Reference: http://paulbourke.net/miscellaneous/interpolation/
    """

    # Take out the x,y,z coordinates from the vertex array.
    x0 = np.array([index[0]])
    y0 = np.array([index[1]])
    z0 = np.array([index[2]])

    # lattice points above x,y,z. For example, if we treat the origin (0,0,0) as (x0,y0,z0),
    # then the vertex (1,0,0) will just be (x1,x0,x0), and so on.
    x1 = x0 + 1
    y1 = y0 + 1
    z1 = z0 + 1

    # Since we are counting the index, vertices are confined within the index boundary.
    x1[np.where(x1==vertex.shape[0])] = x0.max()
    y1[np.where(y1==vertex.shape[1])] = y0.max()
    z1[np.where(z1==vertex.shape[2])] = z0.max()

    # Dimensions of the inner box. Here I define a small box inside the bigger boundary.
    # This will be our point of interest in 3D.
    # Default is the unit cube with a=b=c=0. It will return A unweighted.
    x = np.array([a])
    y = np.array([b])
    z = np.array([c])

    # Apply the trilinear interpolation formula.
    output = (vertex[x0,y0,z0]*(1-x)*(1-y)*(1-z) +
             vertex[x1,y0,z0]*x*(1-y)*(1-z) +
             vertex[x0,y1,z0]*(1-x)*y*(1-z) +
             vertex[x0,y0,z1]*(1-x)*(1-y)*z +
             vertex[x1,y0,z1]*x*(1-y)*z +
             vertex[x0,y1,z1]*(1-x)*y*z +
             vertex[x1,y1,z0]*x*y*(1-z) +
             vertex[x1,y1,z1]*x*y*z)

    return output
