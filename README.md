# FastAPI Hello World - Kubernetes Learning Project

A simple FastAPI application designed to demonstrate Kubernetes basics. This project includes a FastAPI application with health checks, Docker containerization, and Kubernetes manifests for learning container orchestration.

## 🎯 Project Purpose

This repository is designed to help you learn Kubernetes fundamentals by:
- Deploying a simple FastAPI application to Kubernetes
- Understanding Pods, Deployments, and Services
- Learning how to interact with Kubernetes clusters
- Practicing common Kubernetes operations (scaling, health checks, load balancing)

## 📋 Application Overview

A FastAPI application that provides:
- Health check endpoint for Kubernetes probes
- Current time in Costa Rica timezone (UTC-6)
- Time-based greetings

## 🚀 API Endpoints

### GET /healthz
Health check endpoint for Kubernetes liveness and readiness probes.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET /now
Returns the current Costa Rica time (UTC-6) in ISO format.

**Response:**
```json
{
  "now": "2023-10-15T08:30:45.123456-06:00"
}
```

### GET /hello?name={name}
Returns a greeting based on the current time of day in Costa Rica timezone (UTC-6) along with the provided name.

**Query Parameters:**
- `name` (optional): Name to include in the greeting

**Response:**
```json
{
  "message": "Good Morning Andrés"
}
```

**Greeting times (Costa Rica time, UTC-6):**
- Good Morning: 05:00 - 11:59
- Good Afternoon: 12:00 - 16:59
- Good Evening: 17:00 - 20:59
- Good Night: 21:00 - 04:59

## 🏗️ Project Structure

```
.
├── src/
│   ├── main.py              # FastAPI application
│   └── service/
│       └── time.py          # Business logic for time operations
├── k8s/                     # Kubernetes manifests
│   ├── deployment.yaml      # Deployment configuration
│   ├── service.yaml         # Service configuration
│   ├── ingress.yaml         # Ingress configuration (optional)
│   └── README.md            # Detailed Kubernetes documentation
├── Dockerfile               # Docker image definition
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 📚 Understanding Kubernetes Concepts (With Analogies)

### Pod
**Analogy:** A Pod is like a **apartment unit** that contains one or more containers (roommates). Pods are the smallest deployable unit in Kubernetes.

- **What it does:** Runs your application containers
- **Lifecycle:** Pods are ephemeral - they can be created, destroyed, and recreated
- **Key point:** Each Pod gets its own IP address and can contain multiple containers that share resources

### Deployment
**Analogy:** A Deployment is like a **property manager** that ensures you always have the right number of apartments (Pods) running, replacing any that break.

- **What it does:** Manages Pods, ensures desired number of replicas are running
- **Features:** Self-healing (replaces failed Pods), rolling updates, rollbacks
- **Key point:** You don't manage Pods directly - the Deployment does it for you

### Service
**Analogy:** A Service is like a **reception desk** that provides a stable phone number (IP address) even when the people behind the desk (Pods) change.

- **What it does:** Provides a stable endpoint to access Pods, load balances traffic
- **Types:** ClusterIP (internal), NodePort (external via node IP), LoadBalancer (cloud provider)
- **Key point:** Services abstract away Pod IPs - you always use the Service IP/name

### ReplicaSet
**Analogy:** A ReplicaSet is like a **template and counter** that the Deployment uses to maintain the desired number of identical Pods.

- **What it does:** Ensures a specified number of Pod replicas are running
- **Relationship:** Deployments create and manage ReplicaSets
- **Key point:** You typically don't interact with ReplicaSets directly - Deployments handle it

### Container
**Analogy:** A Container is like a **shipping container** - it packages your application with everything it needs to run, isolated from other containers.

- **What it does:** Runs your application in an isolated environment
- **Image:** Built from a Dockerfile, contains your application code and dependencies
- **Key point:** Containers are portable and consistent across different environments

## 🐳 Local Development

### Prerequisites
- Python 3.11+
- Docker
- Kubernetes (Minikube for local development)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application Locally
```bash
uvicorn src.main:app --reload
```

The application will be available at `http://localhost:8000`

### API Documentation
Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🐳 Docker

### Build the Docker Image
```bash
docker build -t fastapi-hello:latest .
```

### Run the Docker Container
```bash
docker run -p 8000:8000 fastapi-hello
```

The application will be available at `http://localhost:8000`

## ☸️ Kubernetes Deployment with Minikube

Minikube is a tool that runs a single-node Kubernetes cluster on your local machine. It's perfect for learning Kubernetes without needing a cloud provider.

### Prerequisites for Minikube
- [Minikube installed](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl installed](https://kubernetes.io/docs/tasks/tools/)
- Docker (Minikube uses Docker to run containers)

### Step 1: Start Minikube
```bash
# Start Minikube with sufficient resources
minikube start --memory=4096 --cpus=2

# Verify Minikube is running
minikube status
```

### Step 2: Build Docker Image in Minikube

**Important:** Minikube has its own Docker daemon. You need to build your image inside Minikube's environment.

```bash
# Point Docker to Minikube's daemon
eval $(minikube docker-env)

# Build the image (this builds inside Minikube)
docker build -t fastapi-hello:latest .

# Verify the image exists in Minikube
minikube image ls | grep fastapi-hello

# Unset Docker environment to use your local Docker again
eval $(minikube docker-env -u)
```

### Step 3: Deploy to Kubernetes
```bash
# Deploy the application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check deployment status
kubectl get deployments
kubectl get pods -l app=fastapi-hello
kubectl get services
```

### Step 4: Access the Application

#### Option A: Port Forward (Recommended for Testing)
```bash
# Port-forward the service to your local machine
kubectl port-forward service/fastapi-hello-service 8000:80

# Access at http://localhost:8000
```

#### Option B: Minikube Service
```bash
# Open service in browser (Minikube will assign a NodePort)
minikube service fastapi-hello-service
```

#### Option C: Direct Pod Access
```bash
# Port-forward to a specific pod
kubectl port-forward <pod-name> 8000:8000
```

### Step 5: Verify Everything Works
```bash
# Test health check
curl http://localhost:8000/healthz

# Test time endpoint
curl http://localhost:8000/now

# Test greeting endpoint
curl "http://localhost:8000/hello?name=Andrés"
```

## 🔍 Common Kubernetes Operations

### View Resources
```bash
# List all pods
kubectl get pods

# List pods with labels
kubectl get pods -l app=fastapi-hello

# List services
kubectl get services

# List deployments
kubectl get deployments

# Get detailed information about a pod
kubectl describe pod <pod-name>
```

### View Logs
```bash
# View logs for a specific pod
kubectl logs <pod-name>

# Follow logs in real-time
kubectl logs -f <pod-name>

# View logs for all pods with a label
kubectl logs -l app=fastapi-hello -f

# View logs with timestamps
kubectl logs <pod-name> --timestamps

# View last N lines
kubectl logs <pod-name> --tail=50
```

### Scale Deployment
```bash
# Scale to 3 replicas
kubectl scale deployment fastapi-hello --replicas=3

# Verify scaling
kubectl get pods -l app=fastapi-hello
```

### Delete and Recreate Pods (Self-Healing Demo)
```bash
# List pods
kubectl get pods -l app=fastapi-hello

# Delete a pod (Deployment will create a new one automatically)
kubectl delete pod <pod-name>

# Watch pods being recreated
kubectl get pods -l app=fastapi-hello -w
```

### Update Deployment
```bash
# After making changes, rebuild the image
eval $(minikube docker-env)
docker build -t fastapi-hello:latest .
eval $(minikube docker-env -u)

# Restart deployment to use new image
kubectl rollout restart deployment/fastapi-hello

# Or delete and recreate
kubectl delete deployment fastapi-hello
kubectl apply -f k8s/deployment.yaml
```

## 🧪 Testing Load Balancing

### Understanding Load Balancing

Kubernetes Services use **connection-based load balancing**, not request-based. This means:
- All requests on the same TCP connection go to the same Pod
- New connections are distributed across Pods
- HTTP keep-alive reuses connections, so multiple requests may hit the same Pod

### Test Load Distribution
```bash
# This will likely hit one pod (connection reuse)
for i in {1..10}; do curl http://localhost:8000/now; done

# This should distribute across pods (new connections)
for i in {1..10}; do curl -H "Connection: close" http://localhost:8000/now; done

# Or use --no-keepalive
for i in {1..10}; do curl --no-keepalive http://localhost:8000/now; done
```

### Monitor Which Pods Handle Requests
```bash
# Terminal 1: Watch logs from all pods
kubectl logs -l app=fastapi-hello -f

# Terminal 2: Send requests
for i in {1..50}; do curl -H "Connection: close" http://localhost:8000/now; done
```

## 🏥 Health Checks Explained

### Liveness Probe
**Analogy:** Like a **heartbeat monitor** - checks if the application is still alive and running.

- **Purpose:** Detects if the application has crashed or is unresponsive
- **Action:** If it fails, Kubernetes restarts the Pod
- **Configuration:** Checks `/healthz` endpoint every 10 seconds (after 30s initial delay)

### Readiness Probe
**Analogy:** Like a **"Ready to serve" sign** - checks if the application is ready to handle traffic.

- **Purpose:** Determines if the application is ready to receive requests
- **Action:** If it fails, the Pod is removed from Service endpoints (traffic stops)
- **Configuration:** Checks `/healthz` endpoint every 5 seconds (after 5s initial delay)

### Why Both?
- **Liveness:** "Is the app running?" → Restart if not
- **Readiness:** "Can the app handle requests?" → Stop sending traffic if not

This allows Kubernetes to:
- Restart crashed applications (liveness)
- Wait for slow-starting applications (readiness)
- Handle temporary issues without unnecessary restarts

## 🔧 Troubleshooting

### Pods Not Starting
```bash
# Check pod status
kubectl get pods -l app=fastapi-hello

# Describe pod to see events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check if image exists in Minikube
minikube image ls | grep fastapi-hello
```

### Image Pull Errors
```bash
# Rebuild image in Minikube
eval $(minikube docker-env)
docker build -t fastapi-hello:latest .
eval $(minikube docker-env -u)

# Verify imagePullPolicy is set to IfNotPresent in deployment.yaml
```

### Health Check Failures
```bash
# Test health endpoint from inside pod
kubectl exec -it <pod-name> -- curl http://localhost:8000/healthz

# Check if endpoint exists in your code
kubectl logs <pod-name> | grep healthz
```

### Port Forward Issues
```bash
# Check if service exists
kubectl get service fastapi-hello-service

# Check service endpoints
kubectl get endpoints fastapi-hello-service

# Verify pods are ready
kubectl get pods -l app=fastapi-hello
```

## 🚀 Next Steps: Deploying to EKS (AWS)

When ready to deploy to a production cluster like AWS EKS:

1. **Push image to a registry:**
   ```bash
   # Build and tag for ECR
   docker build -t fastapi-hello:latest .
   docker tag fastapi-hello:latest <account-id>.dkr.ecr.<region>.amazonaws.com/fastapi-hello:latest
   
   # Push to ECR
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/fastapi-hello:latest
   ```

2. **Update deployment.yaml:**
   - Change `image` field to your ECR image URL
   - Update `imagePullPolicy` to `Always` or remove it (default)

3. **Deploy to EKS:**
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

4. **Create LoadBalancer or Ingress:**
   - Use AWS LoadBalancer Controller for Ingress
   - Or change Service type to LoadBalancer

## 📖 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [k8s/README.md](k8s/README.md) - Detailed Kubernetes manifest documentation

## 🎓 Learning Objectives

By working through this project, you'll learn:
- ✅ How to containerize applications with Docker
- ✅ How to deploy applications to Kubernetes
- ✅ Understanding of Pods, Deployments, and Services
- ✅ How health checks work in Kubernetes
- ✅ How to scale applications
- ✅ How load balancing works in Kubernetes
- ✅ How to troubleshoot Kubernetes deployments
- ✅ Common kubectl commands

## 📝 Example Usage

```bash
# Health check
curl http://localhost:8000/healthz

# Get current Costa Rica time
curl http://localhost:8000/now

# Get greeting with name
curl "http://localhost:8000/hello?name=Andrés"
```

## 🤝 Contributing

This is a learning project. Feel free to:
- Add more endpoints
- Experiment with different Kubernetes features
- Improve documentation
- Share your learning experiences

## 📄 License

This project is for educational purposes.

---

**Happy Learning! 🚀**
