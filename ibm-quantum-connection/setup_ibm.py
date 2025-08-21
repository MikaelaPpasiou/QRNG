'''
from qiskit_ibm_runtime import QiskitRuntimeService

service =QiskitRuntimeService(
    channel="ibm_cloud",
    token="",
    instance="",
)

available_backends = service.backends()
print("Available backends:", available_backends)

backend = available_backends[0]  # e.g., IBMBackend('ibm_brisbane')

print("Selected backend:", backend)
'''

from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# 1) Connect to IBM Quantum
service = QiskitRuntimeService()
available_backends = service.backends()
print("Available backends:", available_backends)

backend = available_backends[0] 
backend = service.least_busy(operational=True, simulator=False)
print("Using backend:", backend.name)

# 2) Define simple QRNG circuit
qc = QuantumCircuit(1)
qc.h(0)
qc.measure_all()

# 3) Transpile the circuit for this backend
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
qc_transpiled = pm.run(qc)

# 4) Run the transpiled circuit
sampler = Sampler(mode=backend)
job = sampler.run([qc_transpiled], shots=1024)
result = job.result()

# 5) Extract results
pub = result[0]
counts = pub.data.meas.get_counts()
bitstrings = pub.data.meas.get_bitstrings()

print("Counts:", counts)
print("First 10 random bits:", "".join(bitstrings[:10]))


'''
(cutie) mikaelapasiou@Mikaelas-MacBook-Pro qrng %  cd /Users/mikaelapasiou/qrng ; /usr/bin/env /Users/mikaelapasiou/qrng/.venv/bin/python /
Users/mikaelapasiou/.vscode/extensions/ms-python.debugpy-2025.10.0-darwin-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 53887 -
- /Users/mikaelapasiou/qrng/setup_ibm.py 
Using backend: ibm_brisbane
Counts: {'0': 474, '1': 550}
First 10 random bits: 0010011111


(cutie) mikaelapasiou@Mikaelas-MacBook-Pro qrng %  cd /Users/mikaelapasiou/qrng ; /usr/bin/env /Users/mikaelapasiou/qrng/.venv/bin/python /
Users/mikaelapasiou/.vscode/extensions/ms-python.debugpy-2025.10.0-darwin-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 54025 -
- /Users/mikaelapasiou/qrng/setup_ibm.py 
Using backend: ibm_brisbane
Counts: {'0': 451, '1': 573}
First 10 random bits: 0010110101
'''
