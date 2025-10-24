import datetime
import logging
import os

import azure.functions as func

# Create the function app instance
app = func.FunctionApp()

@app.timer_trigger(schedule="%TIMER_SCHEDULE%", 
                   arg_name="mytimer", 
                   run_on_startup=True,
                   use_monitor=False) 
def timer_function(mytimer: func.TimerRequest) -> None:
    """
    Timer-triggered function that executes on a schedule defined by TIMER_SCHEDULE app setting.
    
    Args:
        mytimer: Timer information including schedule status
    
    Notes:
        The run_on_startup=True parameter is useful for development and testing as it triggers
        the function immediately when the host starts, but should typically be set to False
        in production to avoid unexpected executions during deployments or restarts.
    """
    utc_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    logging.info(f'Python timer trigger function executed at: {utc_timestamp}')
    
    if mytimer.past_due:
        logging.warning('The timer is running late!')