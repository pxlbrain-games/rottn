# bossfight

Indie game with only procedurally generated boss levels. Online/LAN-Coop. Aim: Boss-AI uses procedurally generated Neural Nets with Reinforcement Learning capacity.

## Development Environment 

https://www.python.org/
Recommended IDE: VSCode + Python Extension (https://code.visualstudio.com/download)

### Windows

1. Clone Repository (https://git-scm.com/download/win)
1. Run `.\dev_setup.bat` as Administrator
1. IDE-specific setup (VSCode: install pylint, enable pytest for unit tests in `.\tests\`)

### \*nix/MacOS

No setup scripts yet.

## Documentation

Recommended modelling tool: https://www.draw.io/

Save diagrams (.xml and exported .pdf) to `.\docs`.

## Testing

Start the client with `python -m bossfight.client`.
You can run the server seperately with `python -m bossfight.server`, but currently it is expected that the client starts the server as a subprocess.

### Unit Tests

py.test (https://docs.pytest.org) unit tests in `.\tests\` folder.
