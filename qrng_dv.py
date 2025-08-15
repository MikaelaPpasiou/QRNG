from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# qiskit => IBM’s open-source Python framework for working with quantum computers
# let's you build & simulate quantum circuits 

qc = QuantumCircuit(1, 1)  # QuantumCircuit(number of quantum bits, number of classical bits) => creates a 1-qubit quantum circuit
qc.h(0)   # applying the Hadamard gate => puts the qubit (index(0)) in a superposition of |0> and |1>
qc.measure(0, 0)  # measuring the qubit (index(0)) and storing the result in the classical bit (index(0))


backend = AerSimulator()  # aersimulator => simulates quantum circuits, shots=10 => run the entire qc 10 separate times
transpiled_qc = transpile(qc, backend)  # transpile => convert the quantum circuit to a form suitable for the backend
job = backend.run(transpiled_qc, shots=1000000)
result = job.result()

counts = result.get_counts()
print("Random bits generated:", counts)

'''
examples of some runs: 
Random bits generated: {'1': 499475, '0': 500525}
Random bits generated: {'1': 499569, '0': 500431}
Random bits generated: {'0': 500029, '1': 499971}
Random bits generated: {'1': 499614, '0': 500386}
Random bits generated: {'0': 500986, '1': 499014}
'''