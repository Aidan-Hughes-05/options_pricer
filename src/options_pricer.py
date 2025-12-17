import numpy as np
from scipy.stats import norm

def d1_d2(s, k, r, sigma, t):
    d1 = (np.log(s / k) + (r + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    return d1, d2


def bs_price(s, k, r, sigma, t, option_type="call"):
    if t<=0:
        # payoff at expiry
        return max(s-k,0) if option_type=="call" else max(k-s,0)
    d1, d2 = d1_d2(s, k, r, sigma, t)
    if option_type=="call":
        price = s*norm.cdf(d1) - k*np.exp(-r*t)*norm.cdf(d2)
    else:
        price = k*np.exp(-r*t)*norm.cdf(-d2) - s*norm.cdf(-d1)
    return price


def delta(s, k, r, sigma, t, option_type="call"):
    if t <= 0:
        if option_type == "call":
            return 1 if s > k else 0
        else:  # put
            return -1 if s < k else 0


    d1, _ = d1_d2(s, k, r, sigma, t)
    return norm.cdf(d1) if option_type=="call" else norm.cdf(d1) - 1


def gamma(s, k, r, sigma, t):
    if t<=0:
        return 0
    d1, _ = d1_d2(s, k, r, sigma, t)
    return norm.pdf(d1)/(s*sigma*np.sqrt(t))


def theta(s, k, r, sigma, t, option_type="call"):
    if t<=0:
        return 0
    d1, d2 = d1_d2(s, k, r, sigma, t)
    if option_type=="call":
        the = -(s*norm.pdf(d1)*sigma)/(2*np.sqrt(t)) - k*r*np.exp(-r*t)*norm.cdf(d2)
    else:
        the = -(s*norm.pdf(d1)*sigma)/(2*np.sqrt(t)) + k*r*np.exp(-r*t)*norm.cdf(-d2)
    return the


def vega(s, k, r, sigma, t):
    if t<=0:
        return 0
    d1, _ = d1_d2(s, k, r, sigma, t)
    return s*norm.pdf(d1)*np.sqrt(t)


def rho(s, k, r, sigma, t, option_type="call"):
    if t<=0:
        return 0
    d1, d2 = d1_d2(s, k, r, sigma, t)
    if option_type=="call":
        ro = k*t*np.exp(-r*t)*norm.cdf(d2)
    else:
        ro = -k*t*np.exp(-r*t)*norm.cdf(-d2)
    return ro
