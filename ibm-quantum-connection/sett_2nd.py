from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

service = QiskitRuntimeService(
    channel='ibm_cloud',
    token='',
    instance='',
)

available_backends = service.backends()
print('Available backends:', available_backends)

backend = service.least_busy(operational=True, simulator=False)
print('Using backend:', backend.name)

qc = QuantumCircuit(1)
qc.h(0)
qc.measure_all()

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
qc_transpiled = pm.run(qc)

sampler = Sampler(mode=backend)
job = sampler.run([qc_transpiled], shots=1024)
result = job.result()

pub = result[0]
counts = pub.data.meas.get_counts()
bitstrings = pub.data.meas.get_bitstrings()

print('Counts:', counts)
print('First 10 random bits:', ''.join(bitstrings[:10]))
