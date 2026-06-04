def safe_execute(
    fn,
    *args,
    retries=3
):

    for attempt in range(retries):

        try:

            result = fn(*args)

            if result:
                return result

        except Exception:
            pass

    return {
        "status":"FAILED"
    }