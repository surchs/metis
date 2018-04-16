import numpy as np
import nibabel as nib


def sca(ts_p, mask, atlas):
    """
    Return the seed based correlation maps of an individual time series
    based on an atlas
    :param ts_p: path to the time series
    :param mask: mask volume as boolean
    :param atlas: atlas volume as integer
    :return seed_fz: the fisher-z transformed seed map of all atlas regions
    """
    # Mask the Atlas
    atlas_m = atlas[mask]
    # Load the time series
    ts = nib.load(ts_p).get_data()[mask]
    # Get the average in network signal
    regions = np.unique(atlas[atlas!=0])
    avg_net = np.array([np.mean(ts[atlas_m == region, :], 0) for region in regions])
    # Seed stack
    seed_stack = corr2_coeff(avg_net, ts)
    # FisherZ transform
    seed_fz = np.arctanh(seed_stack)
    return seed_fz


def corr2_coeff(A,B):
    # Rowwise mean of input arrays & subtract from input arrays themeselves
    A_mA = A - A.mean(1)[:, None]
    B_mB = B - B.mean(1)[:, None]

    # Sum of squares across rows
    ssA = (A_mA**2).sum(1)
    ssB = (B_mB**2).sum(1)

    # Finally get corr coeff
    return np.dot(A_mA, B_mB.T)/np.sqrt(np.dot(ssA[:, None], ssB[None]))
