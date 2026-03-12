import logging

import azure.functions as func

app = func.FunctionApp()


@app.timer_trigger(schedule="0 */5 * * * *", arg_name="timer", run_on_startup=False)
def TimerExample(timer: func.TimerRequest) -> None:  # noqa: N802 (Azure style name retained)
    if timer.past_due:
        logging.warning("The timer is running later than expected.")

    logging.info("Timer trigger executed successfully.")
