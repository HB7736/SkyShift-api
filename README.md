# SkyShift API

SkyShift API is a server developed using Flask for SkyShift, providing integration with Terraform and Jenkins. This API facilitates interactions such as retrieving GitHub repository information, managing user sessions, generating Terraform scripts, and performing Jenkins operations.

## Features

- **GitHub Integration**
  - List user repositories
  - Retrieve repository information
- **User Session Management**
  - Create, list, remove, start, and destroy user sessions
- **Terraform Integration**
  - Generate Terraform scripts for infrastructure setup
- **Jenkins Integration**
  - Create, get secrets, delete nodes
  - Create and trigger Jenkins jobs
  - Get build outputs
- **AWS EC2 Instance Management**
  - Generate AWS EC2 instance Terraform scripts

## Installation

To run the SkyShift API, you can use the pre-built Docker image available on Docker Hub. Follow these steps:

1. **Pull the Docker Image**

   ```bash
   docker pull hb7736/skyshift-api:latest
   ```

2. **Run the Docker Container**

   Before running the container, you need to set the required environment variables. Replace the placeholders with your actual values:

   ```bash
   docker run --name skyshift \
     -p 5000:5000 \
     -e JENKINS_URL={URL} \
     -e JENKINS_USERNAME={USERNAME} \
     -e JENKINS_PASSWORD={PASSWORD} \
     -e API_URL={API_URL} \
     -e AWS_ACCESS_KEY={AWS_ACCESS_KEY} \
     -e AWS_SECRET_KEY={AWS_SECRET_KEY} \
     hb7736/skyshift-api:latest
   ```
   For URLs, ensure mentioning protocol with port! i.e. `http://localhost:5000`,
   You can set default values for these environment variables in the `server/modules/variables.py` file if needed.

## API Endpoints

### GitHub Integration

- **`POST /github/list_repos`**: List repositories for a given GitHub username.
- **`POST /github/repo_info`**: Retrieve information about a specific GitHub repository.

### User Session Management

- **`POST /user/create_session`**: Create a new user session.
- **`POST /user/list_sessions`**: List all sessions for a user.
- **`POST /user/remove_session`**: Remove a specific user session.
- **`POST /user/remove_all_sessions`**: Remove all sessions for a user.
- **`POST /user/start_session`**: Start a specific user session.
- **`POST /user/session_info`**: Get information about a specific user session.
- **`POST /user/destroy_session`**: Destroy a specific user session.

### Terraform Integration

- **`POST /terraform/generate_script`**: Generate Terraform script for specified infrastructure.

### Jenkins Integration

- **`POST /jenkins/create_node`**: Create a Jenkins node.
- **`POST /jenkins/get_node_secret`**: Get the secret for a Jenkins node.
- **`POST /jenkins/delete_node`**: Delete a Jenkins node.
- **`POST /jenkins/create_job`**: Create a Jenkins job.
- **`POST /jenkins/trigger_build`**: Trigger a build for a Jenkins job.
- **`POST /jenkins/build_output`**: Get the build output for a Jenkins job.

### AWS EC2 Instance Management

- **`POST /generate_terraform_code/aws_instance`**: Generate Terraform script for setting up an AWS EC2 instance.
