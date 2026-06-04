def reconcile_medications(
    admission_meds,
    discharge_meds
):

    reconciliation = []

    for med in discharge_meds:

        reconciliation.append({
            "medication": med,
            "status": "continued"
        })

    return reconciliation