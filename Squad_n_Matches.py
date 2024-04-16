import math

import Poisson

GOAL_NUM = 8


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

    return avg, math.sqrt(var)


def func1(u, p):
    # formula to calculate the average over 90 mins = 5.400 seconds
    return 0.5 * (u * math.erf((5400 - u) / (p * math.sqrt(2))) + u * math.erf(u / (p * math.sqrt(2))) + p * (
            math.e ** (- ((5400 - u) ** 2) / (2 * (p ** 2))) - math.e ** ((- u ** 2) / (2 * (p ** 2)))) / math.sqrt(
        2 * math.pi))


def func2(u, p):
    # formula to calculate the standard deviation over 90 mins = 5400 seconds
    return math.sqrt((p / (2 * math.sqrt(2 * math.pi))) * (
            (math.sqrt(2 * math.pi) * math.erf((5400 - u) / (p * math.sqrt(2)))) + math.sqrt(
        2 * math.pi) * math.erf(u / (p * math.sqrt(2))) + 2 * (u - 5400) * math.e ** (
                    - ((5400 - u) ** 2) / (2 * (p ** 2))) - 2 * u * math.e ** ((- u ** 2) / (2 * (p ** 2)))))


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
        self.std_scored_over_90_mins = func2(self.avg_scored, self.var_scored)
        self.std_suff_over_90_mins = func2(self.avg_suff, self.var_suff)


class Match:
    def __init__(self, Home_squad, Visitor_squad):
        assert isinstance(Home_squad, Squad) and isinstance(Visitor_squad, Squad)
        self.home_squad = Home_squad
        self.visitor_squad = Visitor_squad

        self.temp = self.get_score_expectancy()
        self.home_score_expectancy = self.temp[0]
        self.visitor_score_expectancy = self.temp[1]

        self.score_expectancy = self.home_score_expectancy + self.visitor_score_expectancy

        # self.SE_confidence = self.get_confidence_interval()

        self.fixed_score_num_probs = []
        for i in range(0, GOAL_NUM):
            vals = Poisson.Poisson_distrib(self.score_expectancy).prob_calc(i)
            self.fixed_score_num_probs.append(vals[0])
        print(len(self.fixed_score_num_probs))
        self.overs = []
        self.unders = []
        self.multig = self.get_multigoals(1, GOAL_NUM)
        self.nogoal = self.get_nogoal(GOAL_NUM)

        for i in range(0, len(self.fixed_score_num_probs)):
            self.unders.append(sum(self.fixed_score_num_probs[1:i + 1] * 100, self.fixed_score_num_probs[0] * 100))
        for i in range(0, len(self.unders)):
            self.overs.append(100 - self.unders[i])
        self.print_analysis()
        self.get_result_predictions()

    def get_score_expectancy(self):
        home_score_expectancy = self.home_squad.avg_scored_over_90_mins
        home_suff_expectancy = self.home_squad.avg_suff_over_90_mins
        visitor_score_expectancy = self.visitor_squad.avg_scored_over_90_mins
        visitor_suff_expectancy = self.visitor_squad.avg_suff_over_90_mins

        # alfa = -0.1 * (home_score_expectancy/(home_score_expectancy-visitor_suff_expectancy) + visitor_score_expectancy/(visitor_score_expectancy-home_suff_expectancy))
        # alfa = -0.1*(home_score_expectancy + visitor_score_expectancy)/(home_suff_expectancy+visitor_suff_expectancy-home_score_expectancy-visitor_score_expectancy)
        alfa = 0.5*min(math.fabs(home_score_expectancy/math.log(visitor_suff_expectancy, math.e)), math.fabs(visitor_score_expectancy/math.log(home_suff_expectancy, math.e)))
        print("Alfa_tuner = {}".format(alfa))

        # home_correlated_score = home_score_expectancy + alfa * (visitor_suff_expectancy - home_score_expectancy)
        home_correlated_score = home_score_expectancy + alfa*math.log(visitor_suff_expectancy, math.e)
        # visitor_correlated_score = visitor_score_expectancy + alfa * (home_suff_expectancy - visitor_score_expectancy)
        visitor_correlated_score = visitor_score_expectancy + alfa*math.log(home_suff_expectancy, math.e)

        # print("Coefficient threshold for home: {}\nCoefficient threshold for visitors: {}".format(home_score_expectancy/(home_score_expectancy-visitor_suff_expectancy), visitor_score_expectancy/(visitor_score_expectancy-home_suff_expectancy)))
        print("Coefficient threshold for home: {}\nCoefficient threshold for visitors: {}".format(math.fabs(home_score_expectancy/math.log(visitor_suff_expectancy, math.e)), math.fabs(visitor_score_expectancy/math.log(home_suff_expectancy, math.e))))


        return home_correlated_score, visitor_correlated_score

    def get_sub_probs_given(self, goals):
        print("\n\n{} goals : {} %\n".format(goals, self.fixed_score_num_probs[goals] * 100))
        # for i in range(0, goals+1):
        # print("({}-{}) {} - {} = {} %".format(self.home_squad.name,self.visitor_squad.name, i, goals-i, Poisson.Bin_distrib(self.home_score_expectancy/self.score_expectancy, goals).prob_calc(i) * 100))
        for i in range(0, goals + 1):
            print("Absolute prob ({}-{}) {} - {} = {} %".format(self.home_squad.name, self.visitor_squad.name, i,
                                                                goals - i,
                                                                self.fixed_score_num_probs[goals] * Poisson.Bin_distrib(
                                                                    self.home_score_expectancy / self.score_expectancy,
                                                                    goals).prob_calc(i) * 100))

    def get_result_predictions(self):
        temp_1 = 0
        temp_x = 0
        temp_2 = 0
        for goals in range(0, GOAL_NUM):
            for i in range(0, goals + 1):
                if i > goals - i:
                    temp_1 += self.fixed_score_num_probs[goals] * Poisson.Bin_distrib(
                        self.home_score_expectancy / self.score_expectancy, goals).prob_calc(i)
                elif i < goals - i:
                    temp_2 += self.fixed_score_num_probs[goals] * Poisson.Bin_distrib(
                        self.home_score_expectancy / self.score_expectancy, goals).prob_calc(i)
                else:
                    temp_x += self.fixed_score_num_probs[goals] * Poisson.Bin_distrib(
                        self.home_score_expectancy / self.score_expectancy, goals).prob_calc(i)
        print("\nOUTCOMES:\nexact result:\n1: {} %\nX: {} %\n2: {} %\nPrecision:{} %".format(temp_1 * 100, temp_x * 100,
                                                                                             temp_2 * 100, (1 - (
                    temp_1 + temp_2 + temp_x)) * 100))
        print("\nDouble chance:\n1X: {} %\nX2: {} %\n12: {} %".format((temp_1 + temp_x) * 100, (temp_x + temp_2) * 100,
                                                                      (temp_1 + temp_2) * 100))

    def print_analysis(self):
        print(
            "LOCALI:\nNome: {}\nMedia gol fatti: {}\nDeviazione standard gol fatti: {}\nMedia gol subiti: {}\nDeviazione Standard gol subiti: {}\nMedia gol fatti ai minuti: {}\nMedia gol subiti ai minuti: {}\nDeviazione standard gol fatti ai minuti: {}\nDeviazione standard gol subiti ai minuti: {}\n".format(
                self.home_squad.name, self.home_squad.avg_scored, self.home_squad.var_scored, self.home_squad.avg_suff,
                self.home_squad.var_suff, self.home_squad.avg_scored_over_90_mins,
                self.home_squad.avg_suff_over_90_mins,
                self.home_squad.std_scored_over_90_mins,
                self.home_squad.std_suff_over_90_mins))
        print(
            "OSPITI:\nNome: {}\nMedia gol fatti: {}\nVarianza gol fatti: {}\nMedia gol subiti: {}\nVarianza gol subiti: {}\nMedia gol fatti ai minuti: {}\nMedia gol subiti ai minuti: {}\nDeviazione standard gol fatti ai minuti: {}\nDeviazione standard gol subiti ai minuti: {}\n".format(
                self.visitor_squad.name, self.visitor_squad.avg_scored, self.visitor_squad.var_scored,
                self.visitor_squad.avg_suff, self.visitor_squad.var_suff, self.visitor_squad.avg_scored_over_90_mins,
                self.visitor_squad.avg_suff_over_90_mins,
                self.visitor_squad.std_scored_over_90_mins,
                self.visitor_squad.std_suff_over_90_mins))
        print(
            "Goal Expectancy: {}\nHome goal expectancy: {}\nVisitor goal expectancy: {}\nConfidence Interval:[,]\n".format(
                self.score_expectancy,
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

        print("\n MULTIGOL:")
        for i in range(len(self.multig[1])):
            print("({}): {} %".format(self.multig[1][i], self.multig[0][i] * 100))
        # for i in range(0, GOAL_NUM):
        # self.get_sub_probs_given(i)

        print("\nGOL/NOGOL:")
        print("GOL: {}\nNOGOL: {}".format(100-self.nogoal, self.nogoal))

    def get_confidence_interval(self):
        # provided by Wiki
        interval_min = (1 - 1.96 / math.sqrt(3 * self.score_expectancy - 1)) * self.score_expectancy
        interval_max = (1 + 1.96 / math.sqrt(3 * self.score_expectancy - 1)) * self.score_expectancy

        return interval_min, interval_max

    def get_multigoals(self, minimum, maximum):
        vals = []
        indices = []
        for i in range(minimum, maximum):
            for j in range(i + 1, maximum):
                vals.append(sum(self.fixed_score_num_probs[i:j], 0))
                indices.append("{},{}".format(i, j))
        return vals, indices

    def get_nogoal(self, goals):
        temp = (self.fixed_score_num_probs[0]) * 100
        for i in range(1, goals):
            temp += self.fixed_score_num_probs[i] * Poisson.Bin_distrib(
                self.home_score_expectancy / self.score_expectancy,
                i).prob_calc(i) * 100
            temp += self.fixed_score_num_probs[i] * Poisson.Bin_distrib(
                self.visitor_score_expectancy / self.score_expectancy,
                i).prob_calc(i) * 100
        return temp
