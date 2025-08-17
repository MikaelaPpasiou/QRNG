from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="inqdbw4Q0jeYBosio4Anie7TeY38CBM5vsJ3E8mKw2eS",
    overwrite=True
)
service = QiskitRuntimeService(channel="ibm_quantum_platform")
print(service.list_instances())
service.set_default_instance("qrngg") 
print(service.backends())

