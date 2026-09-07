# Sources and course mapping

## Supplied lecture material

| Lecture | Concepts used |
| --- | --- |
| Lecture 1.2 - Multiple States.pdf | Composite-state simulation and measurement marginalization. |
| Lecture 2 - Quantum Circuits.pdf | Hadamards, circuit composition, and phase kickback. |
| Lecture 4.1 - Quantum Query Algorithms.pdf | Query model, Deutsch, Deutsch-Jozsa, and Simon algorithms. |
| Lecture 4.2 - Foundations of Quantum Algorithms.pdf | Measuring computational cost and distinguishing computational models. |

The original PDFs are not distributed.

## Public references

- [IBM Quantum Learning: query algorithms](https://quantum.cloud.ibm.com/learning/courses/fundamentals-of-quantum-algorithms/quantum-query-algorithms/introduction)
- [IBM Quantum Learning: Deutsch-Jozsa](https://quantum.cloud.ibm.com/learning/courses/fundamentals-of-quantum-algorithms/quantum-query-algorithms/deutsch-jozsa-algorithm)
- [IBM Quantum Learning: Simon](https://quantum.cloud.ibm.com/learning/courses/fundamentals-of-quantum-algorithms/quantum-query-algorithms/simon-algorithm)

## Original experiment choices

The explicit XOR-coset oracle, six-bit secret 101101, selected shot budgets, 400-trial experiment, and CSV reporting were implemented for this project. GF(2) elimination is implemented directly. Wilson intervals use z = 1.96. The exact spanning probability for k samples in dimension d is the product over j = 0,...,d-1 of (1 - 2^(j-k)), with probability zero when k < d.
