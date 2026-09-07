"""Explicit small-oracle simulations; Python runtime is not quantum query cost."""
import numpy as np


def walsh(n):
    if not isinstance(n, int) or not 1 <= n <= 8:
        raise ValueError('Use 1 to 8 input qubits for this dense simulator')
    size = 2**n
    return np.array([[(-1)**((x & y).bit_count() % 2) for y in range(size)]
                     for x in range(size)], float)/np.sqrt(size)


def deutsch_jozsa(table):
    table = np.asarray(table)
    n = int(np.log2(len(table))) if len(table) else 0
    if table.shape != (2**n,) or not np.isin(table, [0, 1]).all():
        raise ValueError('Expected a power-of-two Boolean truth table')
    if table.sum() not in (0, len(table)//2, len(table)):
        raise ValueError('Deutsch-Jozsa requires a constant or balanced oracle')
    # H^n -> phase oracle (-1)^f(x) -> H^n; target |-> is factored out.
    amplitudes = walsh(n) @ ((-1.0)**table / np.sqrt(len(table)))
    return np.abs(amplitudes)**2


def classical_dj(table):
    """Deterministic sequential algorithm under the same constant/balanced promise."""
    deutsch_jozsa(table)  # validate; not charged as part of the query-model algorithm
    first = table[0]
    queries = 1
    for value in table[1:len(table)//2+1]:
        queries += 1
        if value != first:
            return 'balanced', queries
    return 'constant', queries


def simon_table(n, secret):
    walsh(n)  # enforce the simulator size limit
    if not isinstance(secret, int) or not 0 < secret < 2**n:
        raise ValueError('Secret must be a nonzero n-bit integer')
    # A unique representative for each two-element XOR coset.
    return np.array([min(x, x ^ secret) for x in range(2**n)], int)


def simon_probabilities(n, secret):
    table = simon_table(n, secret)
    size = 2**n
    state = np.zeros((size, size), complex)
    # Result of one reversible Uf application to uniform input and |0> output.
    state[np.arange(size), table] = 1/np.sqrt(size)
    after_h = walsh(n) @ state
    # Marginalize the output register; explicit measurement there is unnecessary.
    return np.sum(np.abs(after_h)**2, axis=1)


def gf2_nullspace(samples, n):
    """Return a basis for the binary nullspace by row reduction, O(samples*n^2)."""
    if not 1 <= n <= 8 or any(not 0 <= int(y) < 2**n for y in samples):
        raise ValueError('Invalid sample width')
    rows = [int(y) for y in samples if y]
    rank = 0
    pivots = []
    for bit in range(n-1, -1, -1):
        pivot = next((j for j in range(rank, len(rows)) if (rows[j] >> bit) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for j in range(len(rows)):
            if j != rank and (rows[j] >> bit) & 1:
                rows[j] ^= rows[rank]
        pivots.append(bit)
        rank += 1
    basis = []
    for free in [b for b in range(n) if b not in pivots]:
        vector = 1 << free
        for row, pivot in zip(rows[:rank], pivots):
            if (row & vector).bit_count() % 2:
                vector |= 1 << pivot
        basis.append(vector)
    return basis


def recover_secret(samples, n):
    basis = gf2_nullspace(samples, n)
    return basis[0] if len(basis) == 1 else None
