import math


class Poisson_distrib:
    def __init__(self, lambda_value):
        self.lambda_value = lambda_value

    def prob_calc(self, value):
        under_value = (math.e ** (-self.lambda_value))*(self.lambda_value ** value)/(math.factorial(value))
        return under_value, 1-under_value
