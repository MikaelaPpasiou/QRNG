from qiskit_ibm_runtime import QiskitRuntimeService

service =QiskitRuntimeService(
    channel="ibm_cloud",
    token="OWY5yeNEw3WUUPMExF0icIK_91V6N-Bo8Canib5GRmz_",
    instance="crn:v1:bluemix:public:quantum-computing:us-east:a/120c5cd49f344249a131f67253088239:af95353a-e70b-44f3-9781-2ef5d46383b9::",
)

available_backends = service.backends()
print("Available backends:", available_backends)

backend = available_backends[0]  # e.g., IBMBackend('ibm_brisbane')

print("Selected backend:", backend)
