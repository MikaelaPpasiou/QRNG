from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# 1) Connect to IBM Quantum (only once!)
service = QiskitRuntimeService(
    channel="ibm_cloud",
    token="MVe5phDGE9XbcDg3SoVmMYCMCiFxH178gYk7CkaKq3hK",
    instance="crn:v1:bluemix:public:quantum-computing:us-east:a/77e4bd4e9fcb4f6b83714ce02037a001:14996580-386a-4a73-8b95-f445d9653efc::",
)

available_backends = service.backends()
print("Available backends:", available_backends)

# Pick the least busy backend
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
