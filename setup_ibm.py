from qiskit_ibm_runtime import QiskitRuntimeService

service =QiskitRuntimeService(
    channel="ibm_cloud",
    token="my private token",
    instance="my personal crn",
)

available_backends = service.backends()
print("Available backends:", available_backends)

backend = available_backends[0]  # e.g., IBMBackend('ibm_brisbane')

print("Selected backend:", backend)
