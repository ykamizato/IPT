import numpy as np

def G_tau_to_freq(ntau, beta, G_tau, cutoff):
    """
    The length of G_tau should be ntau + 1.
    G_tau contains the value of Greens's on equally distributed tau points from 0 to beta.
    The first and last elements of G_tau are for tau = 0 and tau = beta, respectively.
    G(iwn) for n >= cutoff are replaced by the asymptotic behavior 1/iwn.
    """
    assert G_tau.shape[0] == ntau+1

    G_tau_ex = np.zeros((2*ntau), dtype=complex)
    G_tau_ex[0:ntau+1] = G_tau[:]
    G_tau_ex[(ntau+1):] = -G_tau[1:ntau]

    #1/iomega correction
    for itau in range(ntau+1):
        G_tau_ex[itau] += 0.5

    for itau in range(ntau+1, 2*ntau):
        G_tau_ex[itau] += -0.5

    y = np.fft.ifft(G_tau_ex, axis=0)

    G_omega = np.zeros((ntau), dtype=complex)
    for im in range(cutoff):
        G_omega[im] = beta*y[2*im+1]

    omega_n = np.array([(2*n+1)*np.pi/beta for n in range(ntau)])
    for im in range(ntau):
       G_omega[im] += 1/(1J*omega_n[im])

    return G_omega

if __name__ == '__main__':
    ntau = 10000
    beta = 10.0
    pole = 1.0
    taus = np.linspace(0, beta, ntau+1)
    G_tau = -np.exp(-taus * pole)/(1 + np.exp(-beta * pole))

    Giwn = G_tau_to_freq(ntau, beta, G_tau, cutoff = int(ntau/2))

    n_iwn = len(Giwn)
    iwn = 1J * (2*np.arange(n_iwn)+1)*np.pi/beta
    Giwn_true = 1/(iwn - pole)

    for n in range(len(Giwn)):
        print(n, Giwn[n].real, Giwn[n].imag, Giwn_true[n].real, Giwn_true[n].imag)
