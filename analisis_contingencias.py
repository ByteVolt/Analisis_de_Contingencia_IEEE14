import numpy as np
#                 De  A   R   X
zdata = np.array[           
                                ]
Vbase = np.array[   ]
Sbase = np.array[   ]

# Matriz de admitancias
def ybus(zdata):
    nl = zdata[:,0]
    nr = zdata[:,1]
    R = zdata[:,2]
    X = zdata[:,3]
    nbr = len(zdata[:,0])
    nbus = max(np.max(nl), np.max(nr))
    Z = R + 1j*X  
    y = np.ones(nbr)/Z  
    Ybus = np.zeros((nbus, nbus), dtype=complex)

    for k in range(nbr):  
        if nl[k] > 0 and nr[k] > 0:
            Ybus[nl[k]-1, nr[k]-1] = Ybus[nl[k]-1, nr[k]-1] - y[k]
            Ybus[nr[k]-1, nl[k]-1] = Ybus[nl[k]-1, nr[k]-1]

    for n in range(nbus): 
        for k in range(nbr):
            if nl[k] == n+1 or nr[k] == n+1:
                Ybus[n, n] = Ybus[n, n] + y[k]

    return Ybus

#Analisis de contingencias
ZBASE = Vbase**2 / Sbase
Ybus = ybus(zdata)
YBUSC = ZBASE * Ybus
YBUSBASE = np.imag(YBUSC)
Xbus = 1 / YBUSBASE
BPRIMA1 = -1 * YBUSBASE
EXTRA = BPRIMA1
EXTRA = np.delete(EXTRA, 0, axis=1)
EXTRA = np.delete(EXTRA, 0, axis=0)
BPRIMA2 = EXTRA
THETAPRIMA = np.linalg.inv(BPRIMA2)
F = np.pad(np.linalg.inv(BPRIMA2), ((1, 1), (1, 1)), 'constant')
THETA = np.pad(THETAPRIMA, (1, 0), 'constant')
B1 = zdata[:, 0]
B2 = zdata[:, 1]
NLINEA = len(zdata[:, 0])
nbus = max(max(B1), max(B2))
FLUJO0 = np.zeros((nbus, nbus))

for k in range(NLINEA):
    FLUJO0[B1[k] - 1, B2[k] - 1] = BPRIMA1[B1[k] - 1, B2[k] - 1] * (THETA[B2[k] - 1] - THETA[B1[k] - 1])