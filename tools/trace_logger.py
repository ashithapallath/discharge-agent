import json
import os
from datetime import datetime


def log_trace(trace_data):

    os.makedirs(
        "outputs/traces",
        exist_ok=True
    )

    filename = (
        f"outputs/traces/"
        f"trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    with open(
        filename,
        "w"
    ) as f:

        json.dump(
            trace_data,
            f,
            indent=4
        )

    print(
        f"Trace saved: {filename}"
    )