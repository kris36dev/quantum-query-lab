import numpy as np
import matplotlib.pyplot as plt
from algorithms import deutsch_jozsa, classical_dj, simon_probabilities, recover_secret
from reporting import arguments, csv_write, finish, style


def main():
    args, out = arguments('Oracle-query comparisons and hidden-string recovery')
    rng = np.random.default_rng(args.seed)
    style()
    dj_rows = []
    for n in range(1, 9):
        constant = np.zeros(2**n, int)
        balanced = np.array([0]*(2**(n-1))+[1]*(2**(n-1)))
        for label, table in [('constant', constant), ('balanced', balanced)]:
            p = deutsch_jozsa(table)
            _, queries = classical_dj(table)
            dj_rows.append({'qubits': n, 'oracle_type': label, 'classical_queries': queries,
                            'quantum_oracle_queries': 1, 'probability_all_zero': float(p[0])})
    csv_write(out/'deutsch_jozsa.csv', dj_rows)
    n, secret, repetitions = 6, 0b101101, 400
    p = simon_probabilities(n, secret)
    rows = []
    for shots in (2, 4, 6, 8, 12, 16, 24):
        successes = sum(recover_secret(rng.choice(2**n, size=shots, p=p), n) == secret
                        for _ in range(repetitions))
        analytic = float(np.prod([1-2.**(j-shots) for j in range(n-1)])) if shots >= n-1 else 0.
        rate = successes/repetitions
        # Wilson interval avoids zero-width error bars at 0 or 100% success.
        z = 1.96; denom = 1+z*z/repetitions
        center = (rate+z*z/(2*repetitions))/denom
        half = z*np.sqrt(rate*(1-rate)/repetitions+z*z/(4*repetitions**2))/denom
        rows.append({'oracle_calls': shots, 'success_rate': rate, 'exact_rank_probability': analytic,
                     'wilson_lower': center-half, 'wilson_upper': center+half, 'trials': repetitions})
    csv_write(out/'simon_recovery.csv', rows)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7), layout='constrained')
    constants = [r for r in dj_rows if r['oracle_type'] == 'constant']
    axes[0].plot([r['qubits'] for r in constants], [r['classical_queries'] for r in constants],
                 'o-', label='Deterministic classical worst case', color='#c56b26')
    axes[0].plot(range(1, 9), np.ones(8), 'o-', label='Deutsch-Jozsa', color='#007f86')
    axes[0].set(yscale='log', xlabel='Input qubits n', ylabel='Oracle queries (log scale)',
                title='Query cost under a constant/balanced promise')
    axes[0].legend(fontsize=8)
    x = [r['oracle_calls'] for r in rows]; y = np.array([r['success_rate'] for r in rows])
    axes[1].plot(x, [r['exact_rank_probability'] for r in rows], color='#007f86', label='Exact rank probability')
    axes[1].errorbar(x, y, yerr=[y-np.array([r['wilson_lower'] for r in rows]),
                     np.array([r['wilson_upper'] for r in rows])-y], fmt='o', capsize=3,
                     color='#c56b26', label='400 trials; 95% Wilson interval')
    axes[1].set(xlabel='Simon oracle calls / measurements', ylabel='Hidden-string recovery probability',
                title='Six-bit secret: 101101', ylim=(-.06, 1.1))
    axes[1].legend(fontsize=8)
    fig.suptitle('QUANTUM QUERY LAB  |  Query savings and sampling requirements', fontsize=14, fontweight='bold')
    fig.savefig(out/'overview.png', dpi=180); plt.close(fig)
    finish(out, {'seed': args.seed, 'largest_dj_n': 8, 'dj_classical_worst_case_queries_n8': 129,
                 'dj_quantum_oracle_queries': 1, 'simon_secret': '101101',
                 'simon_success_at_12_calls': next(r['success_rate'] for r in rows if r['oracle_calls'] == 12),
                 'recovery_trials_per_budget': repetitions, 'cost_model': 'oracle queries, not Python runtime',
                 'hardware_execution': False})


if __name__ == '__main__':
    main()
