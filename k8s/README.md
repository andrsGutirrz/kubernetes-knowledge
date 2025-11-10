# Kubernetes Deployment

This directory contains Kubernetes manifests for deploying the FastAPI application.

## Useful kubectl Commands to Generate Boilerplate

### Generate Deployment YAML
```bash
kubectl create deployment fastapi-hello --image=fastapi-hello:latest --dry-run=client -o yaml > deployment.yaml
```

### Generate Service YAML
```bash
kubectl create service clusterip fastapi-hello-service --tcp=80:8000 --dry-run=client -o yaml > service.yaml
```

### Generate ConfigMap YAML
```bash
kubectl create configmap my-config --from-literal=key=value --dry-run=client -o yaml > configmap.yaml
```

### Generate Secret YAML
```bash
kubectl create secret generic my-secret --from-literal=username=admin --dry-run=client -o yaml > secret.yaml
```

### Generate Namespace YAML
```bash
kubectl create namespace my-namespace --dry-run=client -o yaml > namespace.yaml
```

## Files in this directory

- **deployment.yaml** - Kubernetes Deployment with health checks
- **service.yaml** - Service to expose the application within the cluster
- **ingress.yaml** - Ingress for external access (optional)
- **kustomization.yaml** - Kustomize configuration for managing resources

## Deployment Steps

### 1. Build and push Docker image
```bash
# Build the image
docker build -t fastapi-hello:latest .

# Tag for your registry (replace with your registry)
docker tag fastapi-hello:latest your-registry/fastapi-hello:latest

# Push to registry
docker push your-registry/fastapi-hello:latest
```

### 2. Update deployment.yaml
Update the `image` field in `deployment.yaml` to point to your Docker image registry.

### 3. Deploy to Kubernetes

**Option A: Using kubectl directly**
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
# kubectl apply -f ingress.yaml  # If using ingress
```

**Option B: Using kustomize**
```bash
kubectl apply -k .
```

### 4. Check deployment status
```bash
# Check pods
kubectl get pods -l app=fastapi-hello

# Check service
kubectl get service fastapi-hello-service

# Check logs
kubectl logs -l app=fastapi-hello -f
```

### 5. Access the application
```bash
# Port forward to access locally
kubectl port-forward service/fastapi-hello-service 8000:80

# Then access at http://localhost:8000
```

## Health Checks

The deployment includes:
- **Liveness Probe**: Checks if the container is alive (30s initial delay, every 10s)
- **Readiness Probe**: Checks if the container is ready to serve traffic (5s initial delay, every 5s)

Both probes use the `/healthz` endpoint.

## Resource Limits

The deployment sets resource requests and limits:
- **Requests**: 100m CPU, 128Mi memory
- **Limits**: 200m CPU, 256Mi memory

Adjust these based on your application's needs.

## Scaling

To scale the deployment:
```bash
kubectl scale deployment fastapi-hello --replicas=3
```

Or update the `replicas` field in `deployment.yaml` and apply:
```bash
kubectl apply -f deployment.yaml
```

