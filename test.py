import numpy as np

from src.options_pricer import bs_price, delta, gamma, vega


def almost_equal(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_basic_prices():
    assert bs_price(100, 100, 0.01, 0.2, 1, "call") > 0
    assert bs_price(100, 100, 0.01, 0.2, 1, "put") > 0
    print("✓ Basic sanity tests passed.")


def test_put_call_parity():
    s, k, r, sigma, t = 100, 100, 0.01, 0.2, 1

    call = bs_price(s, k, r, sigma, t, "call")
    put  = bs_price(s, k, r, sigma, t, "put")

    lhs = call - put
    rhs = s - k*np.exp(-r*t)

    assert almost_equal(lhs, rhs)
    print("✓ Put–call parity passed.")


def test_delta_finite_difference():
    s, k, r, sigma, t = 100, 100, 0.01, 0.2, 1
    h = 1e-4

    call_plus  = bs_price(s+h, k, r, sigma, t, "call")
    call_minus = bs_price(s-h, k, r, sigma, t, "call")

    fd_delta = (call_plus - call_minus) / (2*h)
    analytic = delta(s, k, r, sigma, t, "call")

    assert almost_equal(fd_delta, analytic, tol=1e-4)
    print("✓ Delta finite-difference test passed.")


def test_gamma_finite_difference():
    s, k, r, sigma, t = 100, 100, 0.01, 0.2, 1
    h = 1e-4

    c_plus  = bs_price(s+h, k, r, sigma, t, "call")
    c_mid   = bs_price(s,   k, r, sigma, t, "call")
    c_minus = bs_price(s-h, k, r, sigma, t, "call")

    fd_gamma = (c_plus - 2*c_mid + c_minus) / (h*h)
    analytic = gamma(s, k, r, sigma, t)

    assert abs(fd_gamma - analytic) < 1e-3
    print("✓ Gamma finite-difference test passed.")


def test_vega_finite_difference():
    s, k, r, sigma, t = 100, 100, 0.01, 0.2, 1
    h = 1e-4

    c_plus  = bs_price(s, k, r, sigma+h, t, "call")
    c_minus = bs_price(s, k, r, sigma-h, t, "call")

    fd_vega = (c_plus - c_minus) / (2*h)
    analytic = vega(s, k, r, sigma, t)

    assert abs(fd_vega - analytic) < 1e-3
    print("✓ Vega finite-difference test passed.")


def test_expiry_payoff():
    r, sigma, t = 0.01, 0.2, 0
    assert bs_price(110, 100, r, sigma, t, "call") == 10
    assert bs_price(90,  100, r, sigma, t, "call") == 0
    assert bs_price(90,  100, r, sigma, t, "put")  == 10
    assert bs_price(110, 100, r, sigma, t, "put")  == 0
    print("✓ Expiry payoff tests passed.")


def test_expiry_delta():
    r, sigma, t = 0.01, 0.2, 0
    assert delta(110, 100, r, sigma, t, "call") == 1
    assert delta(90,  100, r, sigma, t, "call") == 0
    assert delta(90,  100, r, sigma, t, "put")  == -1
    assert delta(110, 100, r, sigma, t, "put")  == 0
    print("✓ Expiry delta tests passed.")


def test_delta_symmetry():
    s, k, r, sigma, t = 100, 100, 0.01, 0.2, 1
    d_call = delta(s, k, r, sigma, t, "call")
    d_put  = delta(s, k, r, sigma, t, "put")
    assert almost_equal(d_put, d_call - 1)
    print("✓ Call–put delta symmetry passed.")


def test_small_time_behaviour():
    s, k, r, sigma = 100, 100, 0.01, 0.2
    t_small = 1e-4

    g = gamma(s, k, r, sigma, t_small)
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
