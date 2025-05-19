# Hello-world-Project
This project deploys a simple "Hello World" web app using AWS, Kubernetes (EKS), and Terraform. It includes a basic CI/CD pipeline (GitHub Actions or Jenkins) to automate build, Docker image push, and deployment to a Kubernetes cluster.

The pipeline includes code linting, Docker image creation, and deploying to a Kubernetes cluster running on Minikube. The GitHub Actions workflow is executed using a self-hosted runner on an AWS EC2 instance.

# Pre-requisites:
1. First I have created a new github repository which stores application code, Dockerfile, Kubernetes manifests, and CI/CD workflows.
   
2. Created AWS infrastructure: Launched an Ubuntu EC2 instance  AMI (Amazon Machine Image) with t2.medium as instance type.

3. For security configure security group with ports:
   
Port 22 (SSH) — so I could log into the server.

Port 8080 (HTTP) — because I'm using kubectl port-forward to expose my Flask app on this port.

Once instance was running , connected to instance via
```bash
ssh -i path/to/<key-pair-name>.pem ubuntu@ec2-public-ip
``` 
    


🏃‍♂️ What is a Runner?

A runner is a server, virtual machine, or container that runs the automation tasks defined in your pipeline (like in .github/workflows/*.yml for GitHub).
It listens for new jobs and executes them using the tools and commands you define in your CI/CD workflow.

There are two types of runner :

A. Hosted Runner(Managed runner) : Provided and maintained by platforms like GitHub.
Automatically created VM environments (e.g., Ubuntu, Windows, macOS) and Ephemeral in nature (destroyed after each job).

B. Self hosted runner: We can install the runner software on out own machine/server/cloud VM and executes workflows on our own infrastructure.


4. Register the EC2 as GitHub Self-Hosted Runner:
   
Navigate to your GitHub repo: Settings > Actions > Runners.
Click "New self-hosted runner".
Choose Linux and follow the instructions:
```bash
# Create a folder
$ mkdir actions-runner && cd actions-runner
# Download the latest runner package
$ curl -o actions-runner-linux-x64-2.324.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.324.0/actions-runner-linux-x64-2.324.0.tar.gz
# Optional: Validate the hash
$ echo "e8e24a3477da17040b4d6fa6d34c6ecb9a2879e800aa532518ec21e49e21d7b4  actions-runner-linux-x64-2.324.0.tar.gz" | shasum -a 256 -c
# Extract the installer
$ tar xzf ./actions-runner-linux-x64-2.324.0.tar.gz
```
# Create a folder
```bash
# Create the runner and start the configuration experience
# Enter name of the runner as you wanted (e.g. Runner-1) and set label as self-hosted
$ ./config.sh --url https://github.com/VaishnaveeLake/Hello-world-Project --token ASPD2VMZFE3CRZZLJT2B2FTIFLXD4
# Last step, run it!
$ ./run.sh
```

5. Once we set up self hosted runner up and running , first update it and install docker and minikube using following commands :
# Docker installation
```bash
sudo apt update
```
```bash
sudo apt install -y docker.io
sudo usermod -aG docker $USER
newgrp docker
```
# Minikube installation
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start
```
Once the set up is done , go to your local machine :

Write source code with required dependencies and dockerize the Hello World app.

Create a Dockerfile that uses python:3.11-slim and install dependencies from requirements.txt files.

After that write a kubernets manifest files which includes code to create deployment , service and ingress files and save it with .yaml extension.

To write an cicd pipeline create .github/workflows/cicd.yaml file and write pipeline .

Once the source code is ready push the files to repository .

# 🧾 Version Control with Git

```bash
# Check the current Git status
git status
# Stage all modified and new files
git add .
# Commit your changes with a meaningful message
git commit -m "Add CI/CD workflow and Kubernetes deployment config"
# Push changes to the remote repository (main branch)
git push origin main
```
Even if we commited the entire code to github repository the gitHub actions workflow will not run.

When we trigger a GitHub Actions workflow (like pushing code or making a pull request), GitHub tries to assign the job to an available runner that matches the label (like self-hosted, ubuntu-latest, etc.).

As our cicd pipeline is running on self hosted runner ,our EC2 instance should be up and running.

Go to the machine where self hosted runner installed .

Navigate to actions-runner directory and start run.sh script .

The run.sh is the script actually starts the self-hosted runner agent and connects the runner to github , listens for workflow jobs and executes the jobs step by step as defined in workflow and continuously sends logs and job status updates back to the GitHub Actions UI.

```bash
cd /actions-runner
./run.sh
```

![image](https://github.com/user-attachments/assets/d54e0b53-4031-4b27-946d-d9e4c754d241)


# How our pipeline would trigger and work will flow?

# 1. Clone the Repository
Clone the GitHub repository to local machine.
```bash
git clone https://github.com/VaishnaveeLake/Hello-world-Project.git
cd Hello-world-Project.git
```
# 2. Make Code Changes
Modify source code or manifest files as needed. Then, commit and push the changes.
```bash
git add .
git commit -m "Updated app logic or configuration"
git push origin main
```
# 3. Triggering the CI/CD Pipeline
As soon as I push my changes, the GitHub Actions workflow is automatically triggered.
This is because the workflow is set up to run on every push to the main branch.

# 4. Checkout and Linting
GitHub Actions checks out code using the actions/checkout@v3 action.
The pipeline runs a linting step (using tools like flake8) to detect any syntax or style issues.

# 5. Build Docker Image with Timestamp
A Docker image is built from the code using the Dockerfile.
The image tag includes a timestamp (e.g., hello-world-app:20240519123456) to uniquely identify each build.

# 6. Save Image to Local Folder as .tar
The pipeline saves the built Docker image to a local directory as a .tar file using:
```bash
docker save hello-world-app:$TAG -o docker-images/hello-world-app-$TAG.tar
```

![image](https://github.com/user-attachments/assets/e08a6648-917d-4c7e-94ee-c36329ec8cfe)


# 7. Download the .tar Image
We can download the image artifact from GitHub Actions (from the "Artifacts" section) if needed.

# 8. Load Docker image to Minikube and apply the deployment to the Kubernetes cluster inside Minikube
The .tar image is loaded into Minikube:
```bash
eval $(minikube -p minikube docker-env)
docker load -i docker-images/hello-world-app-$TAG.tar
```
The deployment and service are applied to the Kubernetes cluster:
```bash
kubectl apply -f deployment.yaml
```

![image](https://github.com/user-attachments/assets/7547f5bf-0804-4c95-9f96-6434eb276bc0)


# 9. Port Forwarding to Access the App
Port forwarding is used to expose the app from inside Minikube to EC2 instance:
```bash
kubectl port-forward service/hello-world 8080:80 --address 0.0.0.0
```

![image](https://github.com/user-attachments/assets/a47fc894-3168-4542-af16-e00f8c3b84f2)


![image](https://github.com/user-attachments/assets/501a193d-d60c-404e-a105-2109ff638558)


# 10. Test in Web Browser
Visit the app in a browser using EC2 instance’s public IP and forwarded port:
```bash
http://<EC2-IP-ADDRESS>:8080
```
The application has been successfully deployed on Minikube and is now up and running.


![image](https://github.com/user-attachments/assets/bb059528-791f-444e-bb9b-8e35d4655b2f)



# Issues faced and solution :

# ❌ Issue: Linting Error (flake8 - W503, E203, max-line-length)

When running flake8, you might encounter issues like:

W503: line break before a binary operator

E203: whitespace before a colon or comma

E501: line too long (usually > 79 or 88 chars, unless configured)

Fix: In the root of project, created a file named .flake8 to ignore rules that conflict with formatting.

# ❌ Issue: GitHub actions runner was not executing

CI/CD pipeline was triggered, but the runner didn’t pick up the job.

Fix: Ensured the run.sh script was running continuously on the self-hosted runner machine.

# ❌ Issue: Docker image not found during deployment

Kubernetes deployment failed because the local Docker image was not available inside Minikube.

Fix: Used eval $(minikube docker-env) before building the image so Docker builds inside Minikube's environment.

# ❌ Issue: Kubeconfig not set

kubectl could not connect to the cluster because kubeconfig was not configured.

Fix: Ensured minikube status is running else ran minikube start and ensured kubectl config use-context minikube was set properly.

# ❌ Issue: Pod CrashLoopBackOff Error

After deployment, the pod was repeatedly failing to start.

Fix: Checked pod logs using kubectl logs <pod-name> , the app tries to bind to a port already in use inside the container. Corrected the config.

# ❌ Issue: Deployment YAML tag not updating

Changes to the image tag in the Kubernetes deployment YAML were not reflected after applying the changes.

Used the sed command to automate the update of the image tag inside the YAML file before running kubectl apply command.

# ❌ Issue: Service was not accessible on browser

Deployed app was running inside minikube cluster, but not accessible via browser.

Fix: Used kubectl port-forward to forward a local port on my machine to the pod port inside the cluster, allowing browser access.


# If you want to run the application to another machine , what should you do?

CI pipeline runs successfully up to the point where the Docker image is built and saved as a .tar file.

Once image is saved to artifact , download the artifacts to your local machine and unzip the file.

```bash
unzip hello-world-app-20250519100909.zip
```
Load docker image 
```bash
docker load -i hello-world-app-20250519100909.tar
```
```bash
minikube image load hello-world-app:20250519100909  # Minikube should be pre-installed in you local machine
```
Go to the project and open terminal inside project, check and change container image name accordingly.

Run deployment.yaml file and check pods getting created

```bash
kubectl apply -f deployment.yaml
kubectl get pods
```

Once 2 pods are up and running start the minikube service to expose app .
```bash
minikube service hello-world
```

![image](https://github.com/user-attachments/assets/e9e0f128-1dc1-4fbc-b23b-3a2cd9623e4d)
 
Go to the browser and hit the URL. Application will be running on your local machine .

![image](https://github.com/user-attachments/assets/121758fd-a8ab-4ebd-89a5-6b73402fac20)
