import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
import pickle

def PoissonPP( rt, Dx, Dy=None ):
    '''
    Determines the number of events `N` for a rectangular region,
    given the rate `rt` and the dimensions, `Dx`, `Dy`.
    Returns a <2xN> NumPy array.
    '''
    if Dy == None:
        Dy = Dx
    N = scipy.stats.poisson( rt*Dx*Dy ).rvs()
    x = scipy.stats.uniform.rvs(0,Dx,((N,1)))
    y = scipy.stats.uniform.rvs(0,Dy,((N,1)))
    P = np.hstack((x,y))
    return(P)


def ThomasPP( kappa, sigma, mu, Dx ):
    '''
    each forming a Poisson( mu ) numbered cluster of points,
    having an isotropic Gaussian distribution with variance `sigma`
    '''
    # create a set of parent points from a Poisson( kappa )
    # distribution on the square region [0,Dx] X [0,Dx]
    parents = PoissonPP( kappa, Dx )
    # M is the number of parents
    M = parents.shape[0]
    # an empty list for the Thomas process points
    TP = list()
    # for each parent point..
    for i in range( M ):
        # determine a number of children according
        # to a Poisson( mu ) distribution
        N = scipy.stats.poisson( mu ).rvs()
    # for each child point..
        for j in range( N ):
        # place a point centered on the location of the parent according
        # to an isotropic Gaussian distribution with sigma variance
            pdf = scipy.stats.norm( loc=parents[i,:2], scale=(sigma,sigma) )
            # add the child point to the list TP
            TP.append( list( pdf.rvs(2) ) )
    x,y = zip(*TP)
    pts = [x,y]
    return pts 

def makepos(rawpts):
    ## round these floating decimal coords
    bb = [ round(i) for i in rawpts[0] ]
    cc = [ round(i) for i in rawpts[1] ]
    ## make a set of unique tuples, for tree positions
    dd = set(list(zip(bb,cc)))


