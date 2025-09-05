# Building a CI/CD Pipeline for LangGraph Platform Deployments using Github Actions 🦜🕸️

This repository demonstrates how you can automate the deployment of agents to LangGraph Platform (LGP) using Github Actions and the latest LGP [Control Plane API v2](https://docs.langchain.com/langgraph-platform/api-ref-control-plane).

The project contains two key workflows that leverage the **Control Plane API v2** for robust deployment management:

### 🚀 New Deployment Workflow (`.github/workflows/new-deployment.yml`)
- **Triggers**: Push to `main` branch or merged pull requests
- **Creates new deployments** on LangGraph Platform using Control Plane API v2
- **Builds and pushes** Docker images to Docker Hub
- **Waits for deployment** to be ready before completing
- **Uses proper error handling** and status checking

### 🔄 New Revision Workflow (`.github/workflows/new-revision.yml`)
- **Triggers**: Push to `main` branch or merged pull requests  
- **Updates existing deployments** with new revisions using Control Plane API v2
- **Builds and pushes** updated Docker images
- **Waits for revision deployment** to complete
- **Handles deployment status monitoring**

## Key Features ✨

- **Control Plane API v2**: Uses the latest API endpoints (`/v2/deployments`)
- **Robust Error Handling**: Proper HTTP status checking and error reporting
- **Deployment Monitoring**: Waits for deployments to reach `DEPLOYED` status
- **Flexible Configuration**: Supports both US and EU regions
- **Comprehensive Logging**: Detailed status updates throughout the process

## Required Secrets

Configure these in your GitHub repository:

```
DOCKER_USERNAME          # Your Docker Hub username
DOCKER_PASSWORD          # Your Docker Hub password/token
LANGSMITH_API_KEY        # LangSmith API key for Control Plane API authentication
INTEGRATION_ID           # GitHub integration ID for LangGraph Platform (hosted only)
LISTENER_ID              # Listener ID for self-hosted deployments (self-hosted only)
OPENAI_API_KEY          # OpenAI API key for the agent
ANTHROPIC_API_KEY       # Anthropic API key (optional)
TAVILY_API_KEY          # Tavily API key (optional)
```

## Repository Variables

For non-sensitive configuration, use GitHub repository **Variables** (not Secrets):

```
CONTROL_PLANE_HOST       # Control Plane API host (for self-hosted deployments)
DEPLOYMENT_ID           # Deployment ID for revision updates
K8S_NAMESPACE           # Kubernetes namespace (for self-hosted deployments)
```

**Note**: Use **Variables** for non-sensitive data like URLs and IDs, and **Secrets** for sensitive data like API keys.

## Environment Configuration

### Control Plane Host
The workflows support flexible Control Plane host configuration for different deployment types:

#### **LangGraph Cloud (Hosted)**
- **US Region**: `https://api.host.langchain.com` (default)
- **EU Region**: `https://eu.api.host.langchain.com`

#### **Self-Hosted Deployments**
For self-hosted LangGraph Platform deployments, set your custom Control Plane URL:

**Option 1: Repository Variables (Recommended)**
1. Go to your repository **Settings** → **Secrets and variables** → **Actions** → **Variables** tab
2. Add `CONTROL_PLANE_HOST` variable with your custom URL (e.g., `https://langgraph.yourcompany.com`)

**Option 2: Direct Edit**
1. Edit both workflow files
2. Replace the `CONTROL_PLANE_HOST` environment variable with your custom URL

### Deployment ID Configuration
For the **new-revision workflow**, configure your deployment ID:

**Option 1: Repository Variables (Recommended)**
1. Run the **new-deployment workflow** first to create a deployment
2. Copy the deployment ID from the workflow output  
3. Go to repository **Settings** → **Secrets and variables** → **Actions** → **Variables** tab
4. Add `DEPLOYMENT_ID` variable with the copied value

**Option 2: Direct Edit**
1. Run the **new-deployment workflow** first to create a deployment
2. Copy the deployment ID from the workflow output
3. Edit `new-revision.yml` and replace `your-deployment-id-here` with the actual deployment ID

## Quick Start 🚀

### For LangGraph Cloud Users
1. **Fork this repository**
2. **Configure the required secrets** in your GitHub repository settings
3. **Update the Docker image name** in both workflow files (`IMAGE_NAME` environment variable)
4. **Get your Integration ID** from LangGraph Platform settings
5. **Push to main branch** to trigger the new-deployment workflow
6. **Copy the deployment ID** from the workflow output
7. **Set the deployment ID** as a repository variable for future updates

### For Self-Hosted Customers
1. **Fork this repository**
2. **Configure the required secrets** in your GitHub repository settings (except `LISTENER_ID` - see step 7)
3. **Set repository variables**:
   - `CONTROL_PLANE_HOST`: Your self-hosted Control Plane URL
   - `K8S_NAMESPACE`: Your Kubernetes namespace (optional, defaults to 'default')
4. **Update the Docker image name** in both workflow files (`IMAGE_NAME` environment variable)  
5. **Change deployment type** in both workflow files: Set `DEPLOYMENT_TYPE: 'dev_free'`
6. **Push to main branch** to trigger the new-deployment workflow (it will list available listeners)
7. **Get your Listener ID** from the workflow output:
   - The workflow will automatically list all available listeners
   - Copy the Listener ID you want to use
   - Add `LISTENER_ID` as a GitHub Secret with the copied UUID
8. **Re-run the workflow** - it will now create the deployment successfully
9. **Copy the deployment ID** and set it as the `DEPLOYMENT_ID` repository variable

## Key Differences: Hosted vs Self-Hosted 🔍

| Feature | LangGraph Cloud (Hosted) | Self-Hosted |
|---------|---------------------------|-------------|
| **Source Type** | `"github"` | `"external_docker"` |
| **Deployment Type** | `"dev"` or `"prod"` | `"dev_free"` |
| **Required Secrets** | `INTEGRATION_ID` | `LISTENER_ID` |
| **Image Handling** | Built from GitHub repo | Pre-built Docker image |
| **Resource Management** | Managed by LangGraph | Requires `resource_spec` |
| **Configuration** | Minimal setup | Requires `listener_config` |

Based on the [deployment schema definition](https://gtm.smith.langchain.dev/api-host/docs), the workflows automatically detect your deployment type and use the appropriate API structure.

## Getting Listener ID for Self-Hosted Deployments 🎯

### **Method 1: Automated (Recommended)**
The `new-deployment.yml` workflow automatically lists available listeners when deploying to self-hosted platforms:

1. **Set `DEPLOYMENT_TYPE: 'dev_free'`** in the workflow
2. **Run the workflow** - it will list all available listeners in the logs
3. **Copy the Listener ID** from the output
4. **Add as GitHub Secret** named `LISTENER_ID`

### **Method 2: Manual API Call**
You can also manually query the listeners using the Control Plane API:

```bash
# List all available listeners
curl -X GET \
  "https://your-langgraph-control-plane.com/v2/listeners" \
  -H "X-Api-Key: YOUR_LANGSMITH_API_KEY" \
  -H "Content-Type: application/json"
```

**Example Response:**
```json
{
  "resources": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "production-cluster",
      "compute_type": "k8s",
      "status": "READY"
    },
    {
      "id": "987fcdeb-51a2-43d7-b123-456789abcdef", 
      "name": "dev-cluster",
      "compute_type": "k8s", 
      "status": "READY"
    }
  ]
}
```

Choose the appropriate listener ID based on your deployment needs (dev vs production).

## API Reference 📚

This implementation follows the official [LangGraph Control Plane API v2 documentation](https://docs.langchain.com/langgraph-platform/api-ref-control-plane) and includes:

- **POST /v2/deployments** - Create new deployments
- **PATCH /v2/deployments/{id}** - Update existing deployments  
- **GET /v2/deployments/{id}/revisions** - List deployment revisions
- **GET /v2/deployments/{id}/revisions/{revision_id}** - Get revision status

## Example Code 💻

The repository includes `example_from_new_docs.py` which demonstrates the Control Plane API v2 usage patterns that the workflows implement.

## Support 🆘

For issues related to:
- **LangGraph Platform**: [LangGraph Documentation](https://docs.langchain.com/langgraph-platform/)
- **Control Plane API**: [API Reference](https://docs.langchain.com/langgraph-platform/api-ref-control-plane)
- **GitHub Actions**: [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Environment Variables Reference 📋

Below is a complete list of all environment variables used in the workflows. Use this to create your `.env.example` file:

### **GitHub Secrets** (Sensitive Data)
```bash
# Docker Registry Authentication
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password-or-token

# LangGraph Platform Authentication
LANGSMITH_API_KEY=your-langsmith-api-key

# Deployment Configuration (Choose one based on deployment type)
INTEGRATION_ID=your-github-integration-id        # For LangGraph Cloud (hosted) only
LISTENER_ID=your-listener-id                     # For self-hosted deployments only

# Agent API Keys
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key         # Optional
TAVILY_API_KEY=your-tavily-api-key               # Optional
```

### **GitHub Repository Variables** (Non-Sensitive Configuration)
```bash
# Control Plane Configuration (for self-hosted deployments)
CONTROL_PLANE_HOST=https://langgraph.yourcompany.com

# Deployment Management
DEPLOYMENT_ID=your-deployment-id-from-first-run

# Kubernetes Configuration (for self-hosted deployments)
K8S_NAMESPACE=default                             # Optional, defaults to 'default'
```

### **Workflow Environment Variables** (Set in workflow files)
```bash
# Python and Build Configuration
PYTHON_VERSION=3.11

# Docker Configuration
REGISTRY=docker.io                                # or ghcr.io for GitHub Container Registry
IMAGE_NAME=your-dockerhub-username/your-image-name

# Control Plane Configuration
CONTROL_PLANE_HOST=https://api.host.langchain.com # Default for LangGraph Cloud US
DEPLOYMENT_TYPE=dev                               # 'dev' for hosted, 'dev_free' for self-hosted

# Timeout Configuration
MAX_WAIT_TIME=1800                                # 30 minutes in seconds
```

### **Configuration by Deployment Type**

#### **LangGraph Cloud (Hosted)**
```bash
# Required Secrets
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password
LANGSMITH_API_KEY=your-langsmith-api-key
INTEGRATION_ID=your-github-integration-id
OPENAI_API_KEY=your-openai-api-key

# Workflow Configuration
CONTROL_PLANE_HOST=https://api.host.langchain.com  # or https://eu.api.host.langchain.com
DEPLOYMENT_TYPE=dev                                # or 'prod'
```

#### **Self-Hosted Deployments**
```bash
# Required Secrets
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password
LANGSMITH_API_KEY=your-langsmith-api-key
LISTENER_ID=your-listener-id
OPENAI_API_KEY=your-openai-api-key

# Repository Variables
CONTROL_PLANE_HOST=https://langgraph.yourcompany.com
DEPLOYMENT_ID=your-deployment-id
K8S_NAMESPACE=your-k8s-namespace                   # Optional

# Workflow Configuration
DEPLOYMENT_TYPE=dev_free
```