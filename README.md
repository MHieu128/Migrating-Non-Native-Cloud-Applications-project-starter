# TechConf Registration Website

## Project Overview

The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:

- The web application is not scalable to handle user load at peak
- When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
- The current architecture is not cost-effective

In this project, you are tasked to do the following:

- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:

- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App

1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
     - `POSTGRES_URL`
     - `POSTGRES_USER`
     - `POSTGRES_PW`
     - `POSTGRES_DB`
     - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function

1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

   **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.

   - The Azure Function should do the following:
     - Process the message which is the `notification_id`
     - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
     - Query the database to retrieve a list of attendees (**email** and **first name**)
     - Loop through each attendee and send a personalized subject message
     - After the notification, update the notification status with the total number of attendees notified

2. Publish the Azure Function

### Part 3: Refactor `routes.py`

1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis

Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

For basic/tesing using:

| Azure Resource            | Service Tier            | Monthly Cost |
| ------------------------- | ----------------------- | ------------ |
| _Azure Postgres Database_ | Basic, 1 vCore(s), 5 GB | 25.32 USD    |
| _Azure Service Bus_       | Basic                   | 0.05 USD     |
| _Azure Function App_      | Basic B1                | 12.41 USD    |
| Azure Service App Plan    | Basic B1                | 12.41 USD    |
| _Total cost_              | N/A                     | 50.19 USD    |

For essential using:

| Azure Resource            | Service Tier              | Monthly Cost |
| ------------------------- | ------------------------- | ------------ |
| _Azure Postgres Database_ | Gen 5, 4 vCore(s), 100 GB | 267.29 USD   |
| _Azure Service Bus_       | Standard                  | 10 USD       |
| _Azure Function App_      | Premium EP1               | 157.72 USD   |
| Azure Service App Plan    | Premium P1V3              | 113.15 USD   |
| _Total cost_              | N/A                       | 548.16 USD   |

## Architecture Explanation

I've implemented a bifurcated approach to optimize cost considerations for Azure's architectural design, utilizing two distinct subscriptions to address specific operational requirements. In the initial subscription, our focus is on accommodating testing needs and supporting the operation of smaller web applications. For such use cases, there's typically no imperative to scale up the web application, and the registration numbers remain relatively modest, particularly in small-scale web tech conferences.

In contrast, the second subscription is earmarked for handling substantial user traffic, comparable to Next.js's registration and access patterns witnessed with Next.js. This subscription is intended to cater to online tech conferences hosted by significant enterprises, where many users actively access and register for these events. In this context, the imperative is to provide a web application with robust scalability to meet surges in demand. However, it's essential to acknowledge that database cost considerations loom large within this second subscription. Depending on our ability to accurately estimate the volume of website visitors, it may become necessary to implement measures to limit database capacity.

This bifurcated approach enables us to balance the differing needs of smaller-scale web apps and the demanding requirements of large-scale tech conferences while remaining mindful of the associated costs.
