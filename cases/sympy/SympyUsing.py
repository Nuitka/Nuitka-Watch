# nuitka-project: --standalone
from sympy import expand, symbols, integrate, tan, summation
from sympy.core.cache import clear_cache

if __name__ == "__main__":
    clear_cache()
    x, y, z = symbols("x y z")
    expand((1 + x + y + z) ** 20)

    x, y = symbols("x y")
    f = (1 / tan(x)) ** 10
    integrate(f, x)

    x, i = symbols("x i")
    summation(x**i / i, (i, 1, 400))

    x, y, z = symbols("x y z")
    str(expand((x + 2 * y + 3 * z) ** 30))
