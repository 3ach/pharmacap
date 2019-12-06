import math


# Come from literature
# mandema et al, j clin pharm
# characterization and validation of a pharmacokinetic model for controlled-release oxycodone 
F_rel = 1.02
f_1 = 0.38
k_c1 = 1.11
k_c2 = 0.11
t_lag = 0.206


def plasma_concentration(time):
    adjusted_time = time - t_lag
    c1_component = f_1 * k_c1 * math.exp(-k_c1 * adjusted_time)
    c2_component = (1 - f_1) * k_c2 * math.exp(-k_c2 * adjusted_time)

    return F_rel * (c1_component + c2_component)

def convolve(x, y):
    total_length = len(y) + len(x) - 1
    x_flipped = x[::-1]
    solution = []

    for offset in range(-len(x) + 1, total_length):
        instance = 0
        
        for n in range(min(len(x), len(y))):
            try:
                if n + offset < 0:
                    instance += 0
                else:
                    instance += y[n+offset] * x_flipped[n]
            except:
                instance += 0

        solution.append(instance)

    return solution


times = [x / 2 for x in range(20)]
concentrations = [plasma_concentration(time) for time in times]
doses = [math.exp(-x) + (math.exp(-(x - 5)) if x >=5 else 0) for x in range(11)]

print(doses)
c_concs = convolve(doses, concentrations)

max_concentration = max(c_concs)
norm_concentrations = [12 * (c_conc / max_concentration) for c_conc in c_concs]

for time, norm_concentration, concentration in zip(times, norm_concentrations, c_concs):
    leds = "".join(['*' for _ in range(int(norm_concentration))])
    print(f"{time}\t|{leds}\t\t\t\t|{concentration}")
