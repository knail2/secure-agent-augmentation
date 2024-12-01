# Secure Agent Augmentation

**Secure Agent Augmentation** is a scalable, secure framework for AI agents to interact with external systems, perform complex multi-agent workflows, and manage asynchronous operations. Built with production-grade technologies like FastAPI, and using OAuth 2.0 for robust security, the goal for this framework is to provide developers intending to enhance their AI agent capabilities beyond POCs and laptops and into productions. The goal to to make AI deployments safer, more capable, and fully accessible in hosted environments.

## Key Features

- **Scalable Production-Grade API**: Utilizes FastAPI for rapid, yet scalable, deployment. Easily integrates into containerized environments (e.g., Docker, Kubernetes).
- **Hosted Cloud-Ready Architecture**: Built to be deployed on popular hosting solutions instead of running on your laptop like most open-source solutions.
- **Security First Approach**: Implements OAuth 2.0 for user authentication and authorization, with granular scopes for controlling access to specific actions and data for calling agents
- **AI Agents with External Actions**: Enables AI agents to interact with real-world APIs and services, leveraging reliable production practices.
- **Multi-Agent Asynchronous Workflows (future)**: Supports complex workflows involving multiple AI agents that can operate asynchronously, leveraging callbacks to notify of completed tasks.
- **OpenAPI support**: Supports the OpenAPI spec out of the box which allows both humans and computers to understand and interact with the API’s functionalities without having access to the underlying codebase.

## Why Secure Agent Augmentation?

**Secure Agent Augmentation** represents a secure, versatile framework for enhancing the capabilities of AI agents through providing a safe, authenticated and scalable runtime execution for external actions, and in the future, executing multi-agent framework tasks. 

I built this framework because all common and new agent framework project are written without consideration of security and scalability mind. These frameworks work great on laptops, but can't be easily enhanced for production-grade deployment.


## Getting Started

### Prerequisites
- Python 3.9 or higher
- Docker
- multiple libraries (check out requirements.txt)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/knail2/secure-agent-augmentation.git
   cd secure-agent-framework
   ```

2. **Install Dependencies**: (recommended to do this step in a virtual environment, see below jupyter notebook setup)
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```
   By default, this runs the server on `http://127.0.0.1:8000`.


### Getting Jupyter Notebooks to work on your computer

This section explains how to install the pre-requisite libraries so that you can use the notebooks within this book. So that the libraries are safely installed for the context of this book, we use the python [virtual environment](https://docs.python.org/3/library/venv.html) concept.



1. [Install](https://www.python.org/downloads/) Python on your computer. Recommended versions are 3.9 through 3.12
2. Clone the repository: `git clone https://github.com/victordibia/multiagent-systems-with-autogen.git`
3. Go into the directory: `cd multiagent-systems-with-autogen`
4. Create a virtual environment: `python -m venv venv`
5. Activate the virtual environment: `. ./venv/bin/activate` 
6. Install the required libraries into this environment: `pip install -r requirements.txt`
7. Run Jupyter Lab: `jupyter lab`
8. Within Jupyter Lab, change directories into the respective chapter and open the python notebooks.


### Example Usage

- **Register an Action**: Create AI agent actions accessible via REST endpoints.
- **Control Access with OAuth 2.0 Scopes**: Limit who can call actions, and what data they have access to, using fine-grained scopes.
- **Multi-Agent Asynchronous Workflow**: Trigger a complex action that involves multiple agents working together, asynchronously.

### Sample API Endpoint

To create a simple AI action, add a new endpoint:

```python
from fastapi import APIRouter, Depends
from app.security import oauth2_scheme

router = APIRouter()

@router.get("/run-action", tags=["actions"])
async def run_action(token: str = Depends(oauth2_scheme)):
    # Logic for the AI agent action
    return {"message": "Action executed successfully."}
```

### Multi-Agent Asynchronous Workflow Example

Here is an example of triggering an asynchronous multi-agent workflow:

```python
from fastapi import APIRouter, Depends
from app.security import oauth2_scheme
import asyncio

router = APIRouter()

@router.post("/trigger-async-workflow", tags=["workflows"])
async def trigger_async_workflow(token: str = Depends(oauth2_scheme)):
    # Start an async workflow involving multiple agents
    task = asyncio.create_task(async_workflow())
    return {"message": "Workflow triggered successfully, you will be notified upon completion."}

async def async_workflow():
    # Simulate a complex, multi-agent workflow
    await asyncio.sleep(5)  # Simulate work being done asynchronously
    # Logic to post results to a callback endpoint or update status
    print("Workflow completed, posting results.")
```

## Security
- **OAuth 2.0 Scopes**: Fine-tune access control by assigning different scopes to each API endpoint.
- **Secure Defaults**: All actions require an OAuth token for access.

## Contributing

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a Pull Request.

## License
[MIT](LICENSE)

## Contact
Feel free to open an issue or pull request if you encounter any problems or have a feature request.
