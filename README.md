# Building a CI/CD Pipeline for LangGraph Platform Deployments using Github Actions 🦜🕸️

This repository demonstrates how you can automate the deployment of agents to LangGraph Platform (LGP) using Github Actions

The project contains two key workflows:

### 🚀 New Deployment Workflow (`.github/workflows/new-deployment.yml`)
- **Triggers**: Push to `main` branch or merged pull requests
- **Creates new deployments** on LangGraph Platform programmatically
- **Builds and pushes** Docker images to Docker Hub

### 🔄 New Revision Workflow (`.github/workflows/new-revision.yml`)
- **Triggers**: Push to `main` branch or merged pull requests  
- **Updates existing deployments** with new revisions
- **Builds and pushes** updated Docker images

## Required Secrets

Configure these in your GitHub repository:

```
DOCKER_USERNAME          # Your Docker Hub username
DOCKER_PASSWORD          # Your Docker Hub password/token
LANGSMITH_API_KEY        # LangSmith API key for deployments. Will be used to authenticate into LGP
OPENAI_API_KEY          # OpenAI API key for the agent
```