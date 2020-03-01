# dockerproj

This project outlines how to setup a Docker container which deploys a simple 'Hello World' Flask App, which is also able to take in a JSON payload.

This project is created on Google Cloud Platform.

1. As usual, the first step is to create your project on GCP and activate Cloud Shell and your project with Activate project with: ```gcloud config set project [PROJECT_ID]```

2. Create GitHub Repository and initialize a README.md and .gitignore for Python

3. Next create a SSH key pair by typing ```ssh-keygen -t rsa``` in Cloud Shell and press 'Enter' key thrice and access the SSH key via ```cat ~/.ssh/id_rsa.pub``` in Cloud Shell. Go to GitHub - Settings >> SSH and GPG keys and copy and paste the ssh-key

4. ```git clone``` the repository with SSH to GCP and ```cd [YOUR REPO]``` into the directory which you have cloned from GitHub

5. Create the following files under the repository using ```touch Dockerfile```, ```touch requirements.txt```, ```touch app.py```, ```config.py``` and ```touch Makefile```
	The contents of the files are as per the repository.
	* ```Dockerfile``` allows Docker images to be built automatically by reading the instructions provided in the Dockerfile
	* ```requirements.txt``` contains packages that the app requires to be installed
	* ```Makefile``` contains compilation directives
	* ```app.py``` will contain the codes for our Flask app
	* ```config.py``` has the required Gunicorn (https://vsupalov.com/what-is-gunicorn/) (WSGI application server) configuration to 	run the Flask app
reference for configuring Dockerfile and config.py: https://medium.com/google-cloud/a-guide-to-deploy-flask-app-on-google-kubernetes-engine-bfbbee5c6fb

6. Before we run the application, we would need to do some linting on our code, and since we would be creating a Docker image based on the Dockerfile we created, we would need to lint our ```Dockerfile``` as well: we would add the following lines to our ```Makefile```
```
lint:
	hadolint Dockerfile 
	pylint --disable=R,C,W1203 app.py
 ```
7. Since we do not have hadolint preinstalled on GCP, we would enter the following lines of code on Cloud Shell
  ```sudo wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.17.5/hadolint-Linux-x86_64 &&```                ```sudo chmod +x /bin/hadolint```, which basically downloads and install hadolint as root user (```chmod +x``` basically makes the file executable). 
  
8. Next, on shell, we will create a virtual environment for our project: ```python3 -m venv ~/.dockerproj``` and activate the virtual environment using ```source ~/.dockerproj/bin/activate``` 
  
9. We will do ```make install``` to install all the packages outlined in ```requirements.txt```, then ```make lint``` to check if the code lints.
  
10. Now we can finally run our Flask app with the following command ```gunicorn app:app --config=config.py```. We will see that a server address will pop up and we can click on it to preview our website
  
We will now proceed to creating a Docker image.

  11.  First, we will build an image from our Dockerfile ```docker build --tag=app .```
  
  12. We can then check if our Docker image has been created by doing ```docker image ls```. Once the image ```app``` has been created, we can run the following command ```docker run -d -p 8080:8080 config.py``` and we will see from ```docker ps -a``` command that our server is running on the backgroun. We can click on the Web preview on the top right of Cloud Shell to view our Hello World app.
  
Now, we will push our Docker image to DockerHub 
  
  13. We will first need to setup a DockerHub account (if you dont existingly have one)

  14. To deploy our Docker image to DockerHub, we will first create a shell script using ```touch push-docker.sh``` which allows for pull, (optional) retag, save, load and push Docker images
  
  ```
  #!/usr/bin/env bash
# This tags and uploads an image to Docker Hub

#Assumes this is built
#docker build --tag=app .


dockerpath="[DockerHub username]/app"

# Authenticate & Tag
echo "Docker ID and Image: $dockerpath"
docker login &&\
    docker image tag app $dockerpath

# Push Image
docker image push $dockerpath 
```

  15. Next, we will do ```docker login``` to login into our account, and ```chmod +x push-docker.sh && ./push-docker.sh```

  16. Now we will see that our Docker image associated with our app is in DockerHub (https://hub.docker.com/r/jrc92/app) and we are done!
  
  We can now pull our Dockerimage with the following command: ```docker pull jrc92/app``` and we can check if our image is downloaded using ```docker image ls```. We can then do ```docker run -d -p 8080:8080 jrc92/app``` on shell and preview our Hello World app.
 
