\# Docker Notes App



A simple Flask web application containerized using Docker and Docker Compose.



\## Features

\- Add and display notes

\- Flask application with a health-check endpoint

\- Docker image built using a Dockerfile

\- Docker Compose for application management

\- Port mapping from host port 8080 to container port 5000



\## Technologies

\- Python

\- Flask

\- Docker

\- Docker Compose

\- HTML and CSS



\## Run locally



Build and start the application:



```bash

docker compose up -d --build

```



Open http://localhost:8080 in your browser.



Check application health at http://localhost:8080/health.



Stop the application:



```bash

docker compose down

```



\## Learning outcomes

Learned containerization, Docker images and containers, port mapping, container networking, logs, and Docker Compose.



