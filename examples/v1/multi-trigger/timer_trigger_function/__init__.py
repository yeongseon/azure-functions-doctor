import datetime
import logging
import azure.functions as func

# Timer trigger passes a TimerRequest object

def main(mytimer: func.TimerRequest) -> None:  # noqa: D401
    """Timer trigger logging current UTC time."""
    utc_now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    if mytimer.past_due:
        logging.warning("Timer trigger is past due!")
    logging.info("v1 multi-trigger timer fired at %s", utc_now)
