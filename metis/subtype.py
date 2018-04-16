import numpy as np
import scipy as sp
import patsy as pat
from scipy import cluster as scl
from .connectivity import corr2_coeff
from sklearn import linear_model as sln
from sklearn import preprocessing as skp


def nuisance_regression(stack, model, form):
    """
    Take a csv file and a list of covariates.
    Regress these from a stack of data
    """
    # TODO: what to do with missing data in the model? Should it be constrained?
    # TODO: are we going to implement the multi-job model from sklearn here
    dmatrix = pat.dmatrix(form, data=model)

    mod = sln.LinearRegression(fit_intercept=False, normalize=False)
    res = mod.fit(dmatrix, stack)
    resid = stack - res.predict(dmatrix)
    # Get the intercept
    glob_mean = res.coef_[:, 0]

    return resid, glob_mean


def subtype(stack, n_subtypes=3, mode='corr'):
    """
    Compute subtypes
    :param stack_path:
    :param out_path:
    :return:
    """
    #TODO: Make memory only
    #TODO: replace the I/O
    #I/O
    """
    mask_img = nib.load(mask_path)
    mask = mask_img.get_data().astype(bool)
    n_vox = np.sum(mask)
    stack, stack_meta = mio.read_all(stack_path)
    """
    n_vox = stack.shape[1]
    # Compute subtype
    if mode == 'dist':
        norm = skp.scale(stack, axis=1)
        dist = sp.spatial.distance.pdist(norm)
    elif mode == 'corr':
        sim = np.corrcoef(stack)
        mask = np.triu(sim, 1).astype(bool)
        svec = sim[mask]
        dist = 1 - svec
    else:
        raise Exception('{} is not implemented as a distance'
                        ' method for subtypes'.format(mode))

    link = scl.hierarchy.linkage(dist, method='ward')
    order = scl.hierarchy.dendrogram(link, no_plot=True)['leaves']
    part = scl.hierarchy.fcluster(link, n_subtypes, criterion='maxclust')

    sbt_vec = np.zeros((n_vox, n_subtypes))
    for pid, p in enumerate(np.unique(part)):
        sbt_vec[:, pid] = np.mean(stack[part == p, :], 0)

    return sbt_vec, part, order


def subtype_weights(data_stack, sbt_stack):
    """
    Compute the weights for data. Currently only works if the data and subtypes
    have the same number of features

    data_stack: subject * feature
    sbt_stack: feature * subtype

    :param data_stack:
    :param sbt_stack:
    :return:
    """
    #TODO: make independent of number of features
    weights = corr2_coeff(data_stack, sbt_stack.T)
    return weights
