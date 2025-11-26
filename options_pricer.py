import numpy as np
from scipy.stats import norm

def bs_price(S, K, r, sigma, T, option_type="call"):
    if T<=0:
        # payoff at expiry
        return max(S-K,0) if option_type=="call" else max(K-S,0)
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type=="call":
        price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    else:
        price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
    return price


def delta(S, K, r, sigma, T, option_type="call"):
    if T <= 0:
        if option_type == "call":
            return 1 if S > K else 0
        else:  # put
            return -1 if S < K else 0


    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return norm.cdf(d1) if option_type=="call" else norm.cdf(d1) - 1


def gamma(S, K, r, sigma, T):
    if T<=0:
        return 0
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return norm.pdf(d1)/(S*sigma*np.sqrt(T))


def theta(S, K, r, sigma, T, option_type="call"):
    if T<=0:
        return 0
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type=="call":
        Theta = -(S*norm.pdf(d1)*sigma)/(2*np.sqrt(T)) - K*r*np.exp(-r*T)*norm.cdf(d2)
    else:
        Theta = -(S*norm.pdf(d1)*sigma)/(2*np.sqrt(T)) + K*r*np.exp(-r*T)*norm.cdf(-d2)
    return Theta


def vega(S, K, r, sigma, T, option_type="call"):
    if T<=0:
        return 0
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return S*norm.pdf(d1)*np.sqrt(T)


def rho(S, K, r, sigma, T, option_type="call"):
    if T<=0:
        return 0
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type=="call":
        rho = K*T*np.exp(-r*T)*norm.cdf(d2)
    else:
        rho = -K*T*np.exp(-r*T)*norm.cdf(-d2)
    return rho
