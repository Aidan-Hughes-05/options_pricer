Black Scholes equation and formulae:

$$\frac{\partial{V}}{\partial{t}} + \frac{1}{2}\sigma^{2}S^{2}\frac{\partial^2{V}}{\partial{S^2}} + rS\frac{\partial{V}}{\partial{S}} - rV = 0, $$
 
$$C = SN(d_1) - Xe^{-r(T-t)}N(d_2),$$$$P = Ke^{r(T-t)}N(-d_2) - SN(-d_1)$$

where, 

$$d_1 = \frac{\ln{\frac{S_0}{K}} + (r+\sigma^2)(T-t)}{\sigma\sqrt{T-t}}, d_2 = \frac{\ln{\frac{S_0}{K}} + (r-\sigma^2)(T-t)}{\sigma\sqrt{T-t}}$$

Greeks:

$$\Delta = \frac{\partial{V}}{\partial{S}} = \pm N(\pm d_1) $$ 

$$\Gamma = \frac{\partial^2{V}}{\partial{S^2}} = \frac{N^{\prime}(d_1)}{S\sigma\sqrt{T-t}}$$

$$\Theta = \frac{\partial{V}}{\partial{t}} = -\frac{SN^{\prime}(d_1)\sigma}{S2\sqrt{T-t}} \mp rKe^{-r(T-t)}N^{\prime}(\pm d_2) $$

$$\nu = \frac{\partial{V}}{\partial{\sigma}} = SN^{\prime}(d_1)\sqrt{T-t}$$

$$\rho = \frac{\partial{V}}{\partial{r}} = \pm K(T-t)e^{-r(T-t)}N(\pm d_2)$$

$N(x)$ and $N^{\prime}(x)$ are the standard normal cdf and pdf repectively
