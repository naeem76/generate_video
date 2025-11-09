# Deploy Wan2.2 to RunPod - Step by Step Guide

## Prerequisites
- Docker Desktop installed and running
- Docker Hub account (sign up at https://hub.docker.com if you don't have one)
- RunPod account (https://runpod.io)

## Step 1: Build Docker Image

Open your terminal in this project directory and run:

```bash
# Login to Docker Hub
docker login

# Build the image (replace YOUR_DOCKERHUB_USERNAME with your actual username)
docker build -t YOUR_DOCKERHUB_USERNAME/wan22-video:latest .

# This will take 15-30 minutes as it downloads models and installs dependencies
```

## Step 2: Push to Docker Hub

```bash
# Push the image to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/wan22-video:latest
```

## Step 3: Create RunPod Serverless Endpoint

1. **Go to RunPod Console**: https://console.runpod.io

2. **Navigate to Serverless**: Click on "Serverless" in the left sidebar

3. **Create New Endpoint**:
   - Click "+ New Endpoint" button
   - **Name**: `wan22-video-generator` (or any name you prefer)
   - **Container Image**: `YOUR_DOCKERHUB_USERNAME/wan22-video:latest`
   - **Container Disk**: `20 GB` (minimum, for models)
   - **GPUs**: Select GPU type (recommend: RTX 4090 or A100)
   - **Active Workers**: `0` (will scale up automatically)
   - **Max Workers**: `3` (or as needed)
   - **GPUs/Worker**: `1`
   - **Environment Variables**: (Optional)
     ```
     SERVER_ADDRESS=127.0.0.1
     ```

4. **Advanced Settings**:
   - **Idle Timeout**: `5 seconds` (to save costs)
   - **Execution Timeout**: `600 seconds` (10 minutes for video generation)
   - **Enable Network Volume**: (Optional, if you have custom models)

5. Click **"Deploy"**

## Step 4: Wait for Build

- RunPod will pull your Docker image and initialize
- This takes 5-10 minutes for first deployment
- Status will show "Ready" when complete

## Step 5: Get Your Endpoint ID

1. Once deployed, click on your endpoint
2. Copy the **Endpoint ID** (looks like: `abc123xyz456`)
3. Get your **API Key** from: https://console.runpod.io/user/settings

## Step 6: Update Your .env File

Create or update your `.env` file:

```env
RUNPOD_ENDPOINT_ID=your-endpoint-id-here
RUNPOD_API_KEY=your-api-key-here
```

## Step 7: Test Your Endpoint

```bash
python run_video_generation.py
```

## Troubleshooting

### Build takes too long
- This is normal! The Dockerfile downloads several GB of models
- Subsequent builds will be faster (Docker caching)

### Out of disk space
- Increase Container Disk to 30-40 GB in RunPod settings

### Worker keeps failing
- Check RunPod logs in the console
- Ensure GPU has enough VRAM (minimum 16GB)
- Try reducing video resolution/length in parameters

### Cost optimization
- Set Idle Timeout to 5 seconds
- Use Spot Instances (cheaper but can be interrupted)
- Start with Max Workers = 1 for testing

## Estimated Costs (per hour)
- RTX 4090: ~$0.50/hour
- A100 (40GB): ~$1.50/hour
- L40S: ~$1.00/hour

Only charged when workers are active (processing jobs).

## Next Steps

Once deployed, you can:
- Use the Python client (`generate_video_client.py`)
- Call the API directly via HTTP
- Integrate into your applications
- Share the endpoint with others (they need your API key)

