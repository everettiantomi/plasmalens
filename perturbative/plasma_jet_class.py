import numpy as np
from scipy.optimize import root_scalar

class sieplasmajet(object):
    def __init__(self, theta_E_g, eta, phi, psi0_plasma_num, theta_0_num, B, C, delta_rs, deltab_10, deltab_20):

        self.theta_E_g = theta_E_g
        self.eta = eta
        self.phi = phi
        self.psi0_plasma_num = psi0_plasma_num
        self.theta_0_num = theta_0_num
        self.B = B
        self.C = C
        self.delta_rs = delta_rs
        self.deltab_10 = deltab_10
        self.deltab_20 = deltab_20
        
        def f(r):
            tmp_f = r - theta_E_g + C/r * (r/B/theta_0_num)**C * psi0_plasma_num * np.exp(-(r/B/theta_0_num)**C)
            return tmp_f
            
        zero = root_scalar(f, bracket=[theta_E_g*.1, theta_E_g*1.9], method='bisect')
        self.theta_E = zero.root
        self.r = zero.root
        r = self.r
        
        tmp_psi = theta_E_g*r*np.sqrt(1.-eta*np.cos(2.*phi)) + \
                  psi0_plasma_num*np.exp(-(r/B/theta_0_num)**C) 
        self.psi = tmp_psi


        tmp_dpsi = theta_E_g*r*(np.sqrt( 1. - eta*np.cos(2*phi)) - 1)
        self.dpsi = tmp_dpsi


        tmp_psi0 = theta_E_g*r + psi0_plasma_num*np.exp(-(r/B/theta_0_num)**C)
        self.psi0 = tmp_psi0


        tmp_psi_plasma = psi0_plasma_num*np.exp(-(r/B/theta_0_num)**C)
        self.psi_plasma = tmp_psi_plasma

        tmp_ddpsi_dr = theta_E_g*(np.sqrt( 1. - eta*np.cos(2*phi)) - 1)
        self.ddpsi_dr = tmp_ddpsi_dr


        tmp_ddpsi_dphi = theta_E_g*r*eta*np.sin(2.*phi)/np.sqrt(1.-eta*np.cos(2.*phi))
        self.ddpsi_dphi = tmp_ddpsi_dphi
        
        tmp_d2dpsi_dphi2 = theta_E_g*r*eta*( 2*np.cos(2.*phi)/np.sqrt(1.-eta*np.cos(2.*phi)) - (1.-eta*np.cos(2.*phi))**(-3/2)*eta*np.sin(2*phi)**2)
        self.d2dpsi_dphi2 = tmp_d2dpsi_dphi2


        tmp_d2psi0 = self.psi_plasma * ( - C*(C-1)/r**2*(r/B/theta_0_num)**C + (C/r*(r/B/theta_0_num)**C)**2 )
        self.d2psi0_dr2 = tmp_d2psi0

        
        Delta = delta_rs**2 - ( 1/r*self.ddpsi_dphi - deltab_10*np.sin(phi) + deltab_20*np.cos(phi) )**2

        delta_r_1 = 1/(1 - self.d2psi0_dr2 )*(self.ddpsi_dr + deltab_10*np.cos(phi) + deltab_20*np.sin(phi) + np.sqrt(Delta))
        delta_r_2 = 1/(1 - self.d2psi0_dr2 )*(self.ddpsi_dr + deltab_10*np.cos(phi) + deltab_20*np.sin(phi) - np.sqrt(Delta))

        self.delta_r_1 = delta_r_1
        self.delta_r_2 = delta_r_2

        tmp_delta_r_criticline =  1/(1 - self.d2psi0_dr2 )*( self.ddpsi_dr + 1/r*self.d2dpsi_dphi2 )
        self.delta_r_criticline = tmp_delta_r_criticline
        
        tmp_caustic_1 = 1/r*(self.d2dpsi_dphi2 * np.cos(phi) + self.ddpsi_dphi * np.sin(phi) )
        self.caustic_1 = tmp_caustic_1
        tmp_caustic_2 = 1/r*(self.d2dpsi_dphi2 * np.sin(phi) - self.ddpsi_dphi * np.cos(phi) )
        self.caustic_2 = tmp_caustic_2
        
    def critic(self): #exact
        
        theta_E_g = self.theta_E_g
        eta = self.eta
        psi0_plasma_num = self.psi0_plasma_num
        theta_0_num = self.theta_0_num
        B = self.B
        C = self.C
        delta_rs = self.delta_rs
        deltab_10 = self.deltab_10
        deltab_20 = self.deltab_20
        
        def g(r, *args): #psit = psitotal = psi0 + dpsi
            phi = args[0]
            dpsit_dr = theta_E_g*np.sqrt( 1. - eta*np.cos(2*phi)) - C/r*(r/B/theta_0_num)**C*self.psi_plasma
            d2psit_dr2 = self.psi_plasma*( - C*(C-1)/r**2*(r/B/theta_0_num)**C + (C/r*(r/B/theta_0_num)**C)**2 )
            dpsit_dphi = theta_E_g*r*eta*np.sin(2.*phi)/np.sqrt(1.-eta*np.cos(2.*phi))
            d2psit_dphi2 = theta_E_g*r*eta*( 2*np.cos(2.*phi)/np.sqrt(1.-eta*np.cos(2.*phi)) - \
                                            (1.-eta*np.cos(2.*phi))**(-3/2)*eta*np.sin(2*phi)**2)
            d2psit_drdphi = theta_E_g*eta*np.sin(2.*phi)/np.sqrt(1.-eta*np.cos(2.*phi))  
            tmp = 1/r*( (1 - d2psit_dr2 )*(r - dpsit_dr - 1/r*d2psit_dphi2  ) - 1/r*( 1/r*dpsit_dphi - d2psit_drdphi  )**2 )  
            return tmp                      
        
        r = []                          
        for phi in self.phi:
            zero = root_scalar(g, args = phi , bracket=[theta_E_g*.1, theta_E_g*1.9], method='bisect')
            r.append(zero.root)
        
        r = np.array(r)
        return r 
                                  
                                  
                                  
                                  
        