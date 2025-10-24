<!--
---
name: Azure Functions Python Timer Trigger using Azure Developer CLI
description: This repository contains an Azure Functions timer trigger quickstart written in Python v2 and deployed to Azure Functions Flex Consumption using the Azure Developer CLI (azd). The sample uses managed identity and a virtual network to make sure deployment is secure by default.
page_type: sample
products:
- azure-functions
- azure
- entra-id
urlFragment: starter-timer-trigger-python
languages:
- python
- bicep
- azdeveloper
---
-->

# Azure Functions Python Timer Trigger using Azure Developer CLI

This template repository contains a timer trigger reference sample for functions written in Python v2 and deployed to Azure using the Azure Developer CLI (`azd`). The sample uses managed identity and a virtual network to make sure deployment is secure by default. You can opt out of a VNet being used in the sample by setting VNET_ENABLED to false in the parameters.

This project is designed to run on your local computer. You can also use GitHub Codespaces:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/azure-samples/functions-quickstart-python-azd-timer)

This codespace is already configured with the required tools to complete this tutorial using either `azd` or Visual Studio Code. If you're working a codespace, skip down to [Run your app section](#run-your-app-from-the-terminal).

## Common Use Cases for Timer Triggers

- **Regular data processing**: Schedule batch processing jobs to run at specific intervals
- **Maintenance tasks**: Perform periodic cleanup or maintenance operations on your data
- **Scheduled notifications**: Send automated reports or alerts on a fixed schedule
- **Integration polling**: Regularly check for updates in external systems that don't support push notifications

## Prerequisites

- [Azure Storage Emulator (Azurite)](https://learn.microsoft.com/azure/storage/common/storage-use-azurite) - Required for local development with Azure Functions
- [Python 3.11](https://www.python.org/downloads/) - The recommended Python version for Azure Functions
- [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local?pivots=programming-language-python#install-the-azure-functions-core-tools)
- [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- To use Visual Studio Code to run and debug locally:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
  - [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

## Initialize the local project

You can initialize a project from this `azd` template in one of these ways:

- Use this `azd init` command from an empty local (root) folder:

    ```shell
    azd init --template functions-quickstart-python-azd-timer
    ```

    Supply an environment name, such as `flexquickstart` when prompted. In `azd`, the environment is used to maintain a unique deployment context for your app.

- Clone the GitHub template repository locally using the `git clone` command:

    ```shell
    git clone https://github.com/Azure-Samples/functions-quickstart-python-azd-timer.git
    cd functions-quickstart-python-azd-timer
    ```

    You can also clone the repository from your own fork in GitHub.

## Run your app from the terminal

1. Start Azurite storage emulator in a separate terminal window:

   ```shell
   docker run -p 10000:10000 -p 10001:10001 -p 10002:10002 mcr.microsoft.com/azure-storage/azurite
   ```

2. From the `timer` folder, run this command to start the Functions host locally:

    ```shell
    func start
    ```

3. Wait for the timer schedule to execute the timer trigger.

4. When you're done, press Ctrl+C in the terminal window to stop the `func.exe` host process.

## Run your app using Visual Studio Code

1. Open the `timer` app folder in a new terminal.
2. Run the `code .` code command to open the project in Visual Studio Code.
3. In the command palette (F1), type `Azurite: Start`, which enables debugging without warnings.
4. Press **Run/Debug (F5)** to run in the debugger. Select **Debug anyway** if prompted about local emulator not running.
5. Wait for the timer schedule to trigger your timer function.

## Deploy to Azure

Run this command to provision the function app, with any required Azure resources, and deploy your code:

```shell
azd up
```

Alternatively, you can opt-out of a VNet being used in the sample. To do so, use `azd env` to configure `VNET_ENABLED` to `false` before running `azd up`:

```bash
azd env set VNET_ENABLED false
azd up
```

## Redeploy your code

You can run the `azd up` command as many times as you need to both provision your Azure resources and deploy code updates to your function app.

> [!NOTE]
> Deployed code files are always overwritten by the latest deployment package.

## Clean up resources

When you're done working with your function app and related resources, you can use this command to delete the function app and its related resources from Azure and avoid incurring any further costs:

```shell
azd down
```

## Source Code

The function code for the timer trigger is defined in [`timer_function.py`](./timer/timer_function.py).

This code shows the timer function implementation:  

```python
import datetime
import logging

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
```

The Python v2 programming model uses the [@app.timer_trigger](https://docs.microsoft.com/en-us/python/api/azure-functions/azure.functions.decorators#azure-functions-decorators-timer-trigger) decorator from [azure-functions](https://pypi.org/project/azure-functions/) to define the function

### Key Features

1. **Parameterized Schedule**: The function uses the `%TIMER_SCHEDULE%` environment variable to determine the execution schedule, making it configurable without code changes.

2. **run_on_startup Parameter**: Setting `run_on_startup=True` makes the function execute immediately when the app starts, in addition to running on the defined schedule. This is useful for testing but should be set to `False` in production.

3. **Past Due Detection**: The function checks if the timer is past due using the `mytimer.past_due` property, allowing for appropriate handling of delayed executions.

4. **Python v2 Programming Model**: This function uses the Python v2 programming model with decorators, providing a more intuitive and Pythonic development experience.

5. **Built-in Logging**: The function uses Python's built-in logging module, which integrates seamlessly with Azure Functions and Application Insights.

### Configuration

The timer schedule is configured through the `TIMER_SCHEDULE` application setting, which follows the NCRONTAB expression format. For example:

- `0 */5 * * * *` - Run once every 5 minutes
- `0 0 */1 * * *` - Run once every hour
- `0 0 0 * * *` - Run once every day at midnight

For more information on NCRONTAB expressions, see [Timer trigger for Azure Functions](https://learn.microsoft.com/azure/azure-functions/functions-bindings-timer).
