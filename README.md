# Langchain PDF Streamlit Application

This repository contains the necessary files to deploy a Streamlit application on a Kubernetes cluster. The application processes PDF documents using the Langchain library.

![](langchain-pdf.jpeg)

## Prerequisites

- Docker
- Kubernetes cluster
- kubectl CLI tool
- Docker multi-platform build support (Buildx)

## Building the Docker image

Build the Docker image using Docker Buildx for multi-platform support. In your terminal, run:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t your-username/langchain-pdf-app:latest --push .
```

This command builds the Docker image and pushes it to your Docker repository.

## Deploying to Kubernetes

To deploy the Streamlit application to your Kubernetes cluster, use the provided Kubernetes configuration files in the k8s directory.

```bash
kubectl apply -f k8s/
```

This command creates a deployment and a service on your Kubernetes cluster.

## Accessing the Streamlit Application

After the service is deployed, you can access the Streamlit application through the IP address of the service. To find the IP address, run:

```bash
kubectl get service langchain-pdf-service
```
