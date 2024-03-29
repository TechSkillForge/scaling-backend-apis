# Quick Start Guide to Scaling Your Backend API with Go

This guide is all about setting up and scaling a simple backend API for managing books. We use Go for the API logic, Nginx for distributing incoming requests, and Docker to containerize and manage our services.

## Before You Start

Let’s make sure you have everything you need:

### Required Tools

- **Docker**: Version 20.10.20 or newer.
- **Go (Golang)**: Version 1.22 or newer.

Check your installations by running `docker --version` and `go version` in your terminal. If you don't have them installed or need an update, visit the official Docker and Go websites for installation instructions.

### Configuration Adjustments

Before launching the API, we need to fine-tune a few settings:

1. **Service Resources**: Allocate resources to your services in the `docker-compose.yml` file. Here’s a basic guideline within our example's limitations:

   **Resource Allocation Chart**:

   | Service     | CPU (Cores) | Memory (GB) |
   | ----------- | ----------- | ----------- |
   | api1 + api2 | TBD         | TBD         |
   | nginx       | TBD         | TBD         |
   | postgres    | TBD         | TBD         |
   | **Total**   | **1.5**     | **3GB**     |

   Replace `TBD` with values that fit within the total available resources.

2. **Nginx Configuration**: Set up Nginx to load balance the requests between the two API services. You'll need to create an Nginx configuration file and link it in the `docker-compose.yml` file under volumes for the Nginx service.

3. **Database Setup**: Design your database schema and create handlers for interacting with the database. This involves defining the tables and relationships needed to store and manage book data.

## Running the Application

With the prerequisites ready, you can get the application up and running:

1. Open your terminal.
2. Navigate to your project's directory, where your `docker-compose.yml` is located.
3. Execute the following command:

```bash
docker-compose up -d
```

This command starts all the necessary services in detached mode, running in the background. You're now ready to use the API for creating and reading book entries.

## Running the Stress Test

Once you have the API running and working as expected, you can conduct a stress test on the application using the Locust service. The script sends a large number of requests to the Nginx server to simulate high traffic load and test the application's performance under stress.

1. Access the Locust web interface by opening `http://localhost:8089` in your browser.

You will be presented with the Locust web interface where you can configure the number of users, spawn rate, and test duration. You can use the default options we provided but feel free to adjust them to test the limits of your application.

2. Start the test by clicking the "Start swarming" button.

The test will begin and run for 3 minutes, you will see real-time statistics on the number of requests, response times, and other metrics. You can monitor the performance of your application under stress and identify any bottlenecks or issues.
