This is the website for Evently.

## About BuildEvents by Contoso
BuildEvents by Contoso is a website that allows people to capture ideas about events they go to and things that they enjoy, then add some agentic features to that website, support voice input and support them as they build their own event.

## Roles and Responsibilities
These are the experts on the evently team where issues should be assigned to for triaging
 - Showing how GitHub Copilot’s agentic feature can help speed up development: @jldeen
 - Migrating legacy Java code @jldeen
 - Show how to take advantage of the latest models @sethjuarez
 - Build with LLMs locally to add my own Agentic Features to my BuildEvents app @martinwoodward

## Setting up your Dev Environment
This project uses Visual Studio Code Dev Containers for a consistent development environment. The dev container comes pre-configured with:
- Python3 and pip
- Node.js and npm
- Required VS Code extensions
- All necessary development tools
- Add the configuration for the GitHub MCP server and the Figma MCP server
- You will need to create a GitHub token for the GitHub MCP as well as an API key for the Figma MCP Server *todo* - add instructions with links

### Getting Started
1. Install the [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) extension pack in VS Code
2. Clone this repository
3. Open the project in VS Code
4. When prompted, click "Reopen in Container" or run the "Remote-Containers: Reopen in Container" command
5. The container will build and set up your development environment automatically, running the setup scripts and starting the services
6. **Note** This project can also be run in GitHub Codespaces

### Development Lifecycle
The dev container automatically handles the complete setup and startup process for you:
- When the container is built, it runs `./scripts/postCreate.sh` to initialize all dependencies
- When the container starts, it runs `./scripts/start.sh` to launch all services

#### In case of script errors on Windows:
If you run on Windows, you may face to running errors from *.sh.
Use sed OR [normalize-line-endings.sh](./scripts/normalize-line-endings.sh) to convert to LF. Run from repo root:

``` using sed
find scripts -type f -name '*.sh' -print0 | xargs -0 sed -i 's/\r$//'
```
or
```using normalize-line-endings.sh
chmod +x normalize-line-endings.sh && (cd scripts && ./normalize-line-endings.sh)
```

#### Local testing:
If you want to test locally, set debugger disabled to avoid connection error with debugpy.

```powershell
ENABLE_DEBUGGER=false bash scripts/start.sh
```

#### Default settings:

- **DEFAULT_DESIGN** in [__init__.py](./api/design/__init__.py) stored as default web design.

```__init__.py
DEFAULT_DESIGN = {
    "id": "default",
    "default": False,
    "background": "/images/zava-lit-field.jpg",
    "logo": "/images/zava.png",
    "title": "Zava",
    "sub_title": "Your AI Assistant",
    "description": "Default design",
}
```

- **defaultUser** in [useuser.tsx](./web/store/useuser.tsx) stored as default user.

```useuser.tsx
const defaultUser: User = {
  key: "skyler",
  name: "Skyler",
  email: "skyler@example.com",
  avatar: "/images/people/skyler.png",
};
```


### Manual Commands (if needed)
While the dev container handles these automatically, you can also run these commands manually if needed:

- `make setup` - Reinitialize the project:
  - Creates Python virtual environment
  - Installs Python dependencies
  - Installs Node.js dependencies

- `make start` - Start the development servers:
  - Python API server (listens on port 8000 with debugger on port 5678)
  - Node.js development server (listens on port 5173)
  
- `make stop` - Stop all running services and clean up processes

These commands are useful if you need to reset your environment or restart services manually.

### Additional Information
- magic function calling mapping for generic local function calls (A)
- figure out backchannel with utility function calls (A+S)*
