import math


class Poisson_distrib:
    def __init__(self, lambda_value):
        self.lambda_value = lambda_value

    def prob_calc(self, value):
        under_value = (math.e ** (-self.lambda_value)) * (self.lambda_value ** value) / (math.factorial(value))
        return under_value, 1 - under_value


class Bin_distrib:

    def __init__(self, probability, extractions):
        self.prob = probability
        self.extractions = extractions

    def prob_calc(self, value):
        temp = coefficiente_binomiale(self.extractions, value) * ((self.prob) ** value) * (
                    (1 - self.prob) ** (self.extractions - value))
        return temp


def fattoriale(num):
    if num == 0 or num == 1:
        return 1
    else:
        return num * fattoriale(num - 1)


def coefficiente_binomiale(n, k):
    """
    Calcola il coefficiente binomiale C(n, k).

    Args:
        n (int): Numero totale di elementi.
        k (int): Numero di elementi da scegliere.

    Returns:
        int: Il coefficiente binomiale C(n, k).
    """

    if k < 0 or k > n:
        return 0
    else:
        return fattoriale(n) // (fattoriale(k) * fattoriale(n - k))
