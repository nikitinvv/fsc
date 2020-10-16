import numpy as np
import sys
import dxchange
import matplotlib
import matplotlib.pyplot as plt
import scipy as sp
import scipy.ndimage as ndimage
import statsmodels.api as sm

plt.rcParams['axes.labelsize'] = 60
plt.rcParams['axes.titlesize'] = 32

def halfbit(data, center):
    y, x = np.indices((data.shape))
    r = np.sqrt((x - center[1])**2 + (y - center[0])**2)
    r = r.astype(np.int)

    nr = np.bincount(r.ravel())
    return (0.2071+1.9102/np.sqrt(nr))/(1.2071+0.9102/np.sqrt(nr))

def radial_profile(data, center):
    y, x = np.indices((data.shape))
    r = np.sqrt((x - center[1])**2 + (y - center[0])**2)
    r = r.astype(np.int)

    tbinre = np.bincount(r.ravel(), data.real.ravel())
    tbinim = np.bincount(r.ravel(), data.imag.ravel())

    nr = np.bincount(r.ravel())
    radialprofile = (tbinre+1j*tbinim) / np.sqrt(nr)

    return radialprofile


if __name__ == "__main__":

    fname1 = sys.argv[1]
    fname2 = sys.argv[2]
    fnameout = sys.argv[3]
    wsize = int(sys.argv[4])
    pixel = float(sys.argv[5])
    frac = float(sys.argv[6])

    f1 = dxchange.read_tiff(fname1)
    f2 = dxchange.read_tiff(fname2)

    f1 = f1[f1.shape[0]//2-wsize//2+200:f1.shape[0]//2+200+wsize //
            2, f1.shape[1]//2-wsize//2+100:f1.shape[1]//2+100+wsize//2]
    f2 = f2[f2.shape[0]//2-wsize//2+200:f2.shape[0]//2+200+wsize //
            2, f2.shape[1]//2-wsize//2+100:f2.shape[1]//2+100+wsize//2]

    ff1 = np.fft.fftshift(np.fft.fftn(np.fft.fftshift(f1)))
    ff2 = np.fft.fftshift(np.fft.fftn(np.fft.fftshift(f2)))

    frc1 = radial_profile(ff1*np.conj(ff2), np.array(ff1.shape)//2) /\
        np.sqrt(radial_profile(np.abs(ff1)**2, np.array(ff1.shape)//2)
                * radial_profile(np.abs(ff2)**2, np.array(ff1.shape)//2))
    frc2 = sm.nonparametric.lowess(frc1.real, np.linspace(
        0, 1, len(frc1)), frac=frac, return_sorted=False)

    hbit = halfbit(ff1, np.array(ff1.shape)//2)
    #hhbit = sm.nonparametric.lowess(hbit.real, np.linspace(
     #   0, 1, len(frc1)), frac=frac, return_sorted=False)

    intersection = np.linspace(0, 1, f1.shape[1]//2)[np.where(frc2 < hbit)[0][1]]
    #print('slice, intersection:', idslice, inters)
    plt.figure(figsize=(10, 6))
    plt.plot(frc1[:wsize//2].real, linewidth=1.5, label=r'FRC', color='k')
    plt.plot(frc2[:wsize//2], linewidth=1.5, label=r'smoothed FRC', color='r' )
    plt.plot(hbit[:wsize//2], linewidth=1.5, label=r'1/2-bit threshold')
    plt.grid()
    plt.xlim([-5, wsize//2+6])
    plt.ylim([-0.02, 1.02])
    plt.xticks(np.int32(np.arange(0.0, 1.01, 0.2)*100)/100*(wsize/2+1),[0,0.2,0.4,0.6,0.8,1.0], fontsize=18)
    plt.yticks(np.arange(0, 1.1, 0.2), [0, 0.2, 0.4, 0.6, 0.8, 1.0], fontsize=18)
    plt.legend(fontsize=18)
   
    plt.ylabel('Correlation', rotation=90, fontsize=18)
    axes1 = plt.gca()
    #plt.title('Result: ' + str(np.int32(pixel/intersection*100)/100), fontsize=17)
    #axes2 = axes1.twiny()
    axes1.set_xlabel('Spatial/Nyquist frequency', fontsize=18)
#    axes2.set_xlabel('Spatial resolution', fontsize=14)
 #   axes2.set_xticks(np.int32(np.arange(0.1, 1.01, 0.1)*100)/100)
 #   axes2.set_xticklabels(np.int32(pixel*100 /
  #                              np.arange(0.1, 1.01, 0.1))/100, fontsize=8)
    plt.tight_layout()

    plt.savefig(fnameout, dpi=300)
