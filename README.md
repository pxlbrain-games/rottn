# BossFight

Indie game with only procedurally generated boss levels. Online/LAN-Coop. Aim: Boss-AI uses procedurally generated Neural Nets with Reinforcement Learning capacity.

## Development Environment 

This project is using Python 3.6.5 or newer (https://www.python.org/)

Recommended IDE: VSCode + Python Extension (https://code.visualstudio.com/download)

### Windows

1. Clone Repository (https://git-scm.com/download/win)
1. Run `.\dev_setup.bat` as Administrator
1. IDE-specific setup (VSCode: enable pytest for unit tests in `.\tests\`)

### \*nix/MacOS

No setup scripts yet.

## Documentation

Documentation stuff goes to `.\docs\`. Try and maintain good doumentation habits (it's hard, I know ...).

### Diagrams

Recommended modelling tool: https://www.draw.io/

Save diagrams (.xml and exported .pdf with same name) to `.\docs\diagrams\`.

### API Documentation

Generate code documentation from docstrings using *pydocmd* (https://github.com/NiklasRosenstein/pydoc-markdown). Example command in Python terminal (venv) from project directory:

`pydocmd simple bossfight.server+ bossfight.server.gameService+ > .\docs\api\server.core.gameService.md`

Generate a new .md file whenever API components and/or their docstrings have been changed or added.

## Testing

Start the client with `python -m bossfight.client`.
You can run the server seperately with `python -m bossfight.server`, but currently it is expected that the client starts the server as a subprocess.

### Unit Tests

py.test (https://docs.pytest.org) unit tests in `.\tests\` folder.
