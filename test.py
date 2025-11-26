import numpy as np
from scipy.stats import norm
from options_pricer import bs_price, delta, gamma, theta, vega, rho   


def almost_equal(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_basic_prices():
    assert bs_price(100, 100, 0.01, 0.2, 1, "call") > 0
    assert bs_price(100, 100, 0.01, 0.2, 1, "put") > 0
    print("✓ Basic sanity tests passed.")


def test_put_call_parity():
    S, K, r, sigma, T = 100, 100, 0.01, 0.2, 1

    call = bs_price(S, K, r, sigma, T, "call")
    put  = bs_price(S, K, r, sigma, T, "put")

    lhs = call - put
    rhs = S - K*np.exp(-r*T)

    assert almost_equal(lhs, rhs)
    print("✓ Put–call parity passed.")


def test_delta_finite_difference():
    S, K, r, sigma, T = 100, 100, 0.01, 0.2, 1
    h = 1e-4

    call_plus  = bs_price(S+h, K, r, sigma, T, "call")
    call_minus = bs_price(S-h, K, r, sigma, T, "call")

    fd_delta = (call_plus - call_minus) / (2*h)
    analytic = delta(S, K, r, sigma, T, "call")

    assert almost_equal(fd_delta, analytic, tol=1e-4)
    print("✓ Delta finite-difference test passed.")


def test_gamma_finite_difference():
    S, K, r, sigma, T = 100, 100, 0.01, 0.2, 1
    h = 1e-4

    c_plus  = bs_price(S+h, K, r, sigma, T, "call")
    c_mid   = bs_price(S,   K, r, sigma, T, "call")
    c_minus = bs_price(S-h, K, r, sigma, T, "call")

    fd_gamma = (c_plus - 2*c_mid + c_minus) / (h*h)
    analytic = gamma(S, K, r, sigma, T)

    assert abs(fd_gamma - analytic) < 1e-3
    print("✓ Gamma finite-difference test passed.")


def test_vega_finite_difference():
    S, K, r, sigma, T = 100, 100, 0.01, 0.2, 1
    h = 1e-4

    c_plus  = bs_price(S, K, r, sigma+h, T, "call")
    c_minus = bs_price(S, K, r, sigma-h, T, "call")

    fd_vega = (c_plus - c_minus) / (2*h)
    analytic = vega(S, K, r, sigma, T)

    assert abs(fd_vega - analytic) < 1e-3
    print("✓ Vega finite-difference test passed.")


def test_expiry_payoff():
    r, sigma, T = 0.01, 0.2, 0
    assert bs_price(110, 100, r, sigma, T, "call") == 10
    assert bs_price(90,  100, r, sigma, T, "call") == 0
    assert bs_price(90,  100, r, sigma, T, "put")  == 10
    assert bs_price(110, 100, r, sigma, T, "put")  == 0
    print("✓ Expiry payoff tests passed.")


def test_expiry_delta():
    r, sigma, T = 0.01, 0.2, 0
    assert delta(110, 100, r, sigma, T, "call") == 1
    assert delta(90,  100, r, sigma, T, "call") == 0
    assert delta(90,  100, r, sigma, T, "put")  == -1
    assert delta(110, 100, r, sigma, T, "put")  == 0
    print("✓ Expiry delta tests passed.")


def test_delta_symmetry():
    S, K, r, sigma, T = 100, 100, 0.01, 0.2, 1
    d_call = delta(S, K, r, sigma, T, "call")
    d_put  = delta(S, K, r, sigma, T, "put")
    assert almost_equal(d_put, d_call - 1)
    print("✓ Call–put delta symmetry passed.")


def test_small_time_behaviour():
    S, K, r, sigma = 100, 100, 0.01, 0.2
    T_small = 1e-4

    g = gamma(S, K, r, sigma, T_small)
    assert g > 1  # should spike
    print("✓ Near-expiry gamma behaviour passed.")


def run_all_tests():
    print("\nRunning Black–Scholes tests...\n")
    test_basic_prices()
    test_put_call_parity()
    test_delta_finite_difference()
    test_gamma_finite_difference()
    test_vega_finite_difference()
    test_expiry_payoff()
    test_expiry_delta()
    test_delta_symmetry()
    test_small_time_behaviour()
    print("\nALL TESTS PASSED ✔✔✔\n")


if __name__ == "__main__":
    run_all_tests()
