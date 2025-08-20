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
