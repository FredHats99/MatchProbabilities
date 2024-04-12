import math

import Poisson


def get_avg_var(list_num):
    n = len(list_num)

    # Calcola la media
    if n == 0:
        avg = 0
    else:
        avg = sum(list_num) / n

    # Calcola la varianza
    if n == 0:
        var = 0
    else:
        somma_quad_diff = sum((x - avg) ** 2 for x in list_num)
        var = somma_quad_diff / n

    return avg, var


def func1(u, p):
    return 0.5 * (u * math.erf((5400 - u) / p) + u * math.erf(u / p) + p * (
            math.e ** (- ((5400 - u) ** 2) / (p ** 2)) - math.e ** ((- u ** 2) / (p ** 2))) / math.sqrt(
        math.pi))


class Squad:
    def __init__(self, name, score_list, suff_list):
        self.name = name
        self.matches = len(score_list)
        avg_var_scored = get_avg_var(score_list)
        avg_var_suff = get_avg_var(suff_list)
        self.avg_scored = avg_var_scored[0]
        self.var_scored = avg_var_scored[1]
        self.avg_suff = avg_var_suff[0]
        self.var_suff = avg_var_suff[1]
        self.avg_scored_over_90_mins = func1(self.avg_scored, self.var_scored)
        self.avg_suff_over_90_mins = func1(self.avg_suff, self.var_suff)


class Match:
    def __init__(self, Home_squad, Visitor_squad):
        assert isinstance(Home_squad, Squad) and isinstance(Visitor_squad, Squad)
        self.home_squad = Home_squad
        self.visitor_squad = Visitor_squad

        self.home_score_expectancy = self.get_score_expectancy()[0]
        self.visitor_score_expectancy = self.get_score_expectancy()[1]

        self.score_expectancy = self.home_score_expectancy + self.visitor_score_expectancy

        self.fixed_score_num_probs = []
        for i in range(0, 7):
            vals = Poisson.Poisson_distrib(self.score_expectancy).prob_calc(i)
            self.fixed_score_num_probs.append(vals[0])

        self.overs = []
        self.unders = []

        for i in range(0, len(self.fixed_score_num_probs)):
            self.unders.append(sum(self.fixed_score_num_probs[1:i + 1] * 100, self.fixed_score_num_probs[0] * 100))
        for i in range(0, len(self.unders)):
            self.overs.append(100 - self.unders[i])
        # self.print_analysis()

    def get_score_expectancy(self):
        home_score_expectancy = self.home_squad.avg_scored_over_90_mins
        home_suff_expectancy = self.home_squad.avg_suff_over_90_mins
        visitor_score_expectancy = self.visitor_squad.avg_scored_over_90_mins
        visitor_suff_expectancy = self.visitor_squad.avg_suff_over_90_mins

        home_correlated_score = home_score_expectancy - 0.5 * (visitor_suff_expectancy - home_score_expectancy)
        visitor_correlated_score = visitor_score_expectancy - 0.5 * (home_suff_expectancy - visitor_score_expectancy)

        return home_correlated_score, visitor_correlated_score

    def get_sub_probs_given(self, goals):
        print("\n\n{} goals : {} %\n".format(goals, self.fixed_score_num_probs[goals] * 100))
        # for i in range(0, goals+1):
        # print("({}-{}) {} - {} = {} %".format(self.home_squad.name,self.visitor_squad.name, i, goals-i, Poisson.Bin_distrib(self.home_score_expectancy/self.score_expectancy, goals).prob_calc(i) * 100))
        for i in range(0, goals+1):
            print("Absolute prob ({}-{}) {} - {} = {} %".format(self.home_squad.name,self.visitor_squad.name, i, goals-i, self.fixed_score_num_probs[goals]*Poisson.Bin_distrib(self.home_score_expectancy/self.score_expectancy, goals).prob_calc(i) * 100))

    def print_analysis(self):
        print(
            "LOCALI:\nNome: {}\nMedia gol fatti: {}\nVarianza gol fatti: {}\nMedia gol subiti: {}\nVarianza gol subiti: {}\nMedia gol fatti ai minuti: {}\nMedia gol subiti ai minuti: {}\n".format(
                self.home_squad.name, self.home_squad.avg_scored, self.home_squad.var_scored, self.home_squad.avg_suff,
                self.home_squad.var_suff, self.home_squad.avg_scored_over_90_mins,
                self.home_squad.avg_suff_over_90_mins))
        print(
            "OSPITI:\nNome: {}\nMedia gol fatti: {}\nVarianza gol fatti: {}\nMedia gol subiti: {}\nVarianza gol subiti: {}\nMedia gol fatti ai minuti: {}\nMedia gol subiti ai minuti: {}\n".format(
                self.visitor_squad.name, self.visitor_squad.avg_scored, self.visitor_squad.var_scored,
                self.visitor_squad.avg_suff, self.visitor_squad.var_suff, self.visitor_squad.avg_scored_over_90_mins,
                self.visitor_squad.avg_suff_over_90_mins))
        print(
            "Goal Expectancy: {}\nHome goal expectancy: {}\nVisitor goal expectancy: {}\n".format(self.score_expectancy,
                                                                                                  self.home_score_expectancy,
                                                                                                  self.visitor_score_expectancy))

        for i in range(0, len(self.fixed_score_num_probs)):
            print("{} goal: {} %".format(i, self.fixed_score_num_probs[i] * 100))

        print("\nUNDER:")
        for i in range(0, len(self.unders)):
            print("{}.5: {} %".format(i, self.unders[i]))

        print("\nOVER:")
        for i in range(0, len(self.overs)):
            print("{}.5: {} %".format(i, self.overs[i]))
