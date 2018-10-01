# BossFight

Indie game with only procedurally generated boss levels. Online/LAN-Coop. Boss-AI uses Deep Q Neural Nets in order to adapt to and learn from the player during a fight.

![Screenshot](/screenshot.png)

## Development Environment 

This project is using Python 3.6.5 or newer (https://www.python.org/)

Recommended IDE: VSCode + "official" Python Extension (https://code.visualstudio.com/download)

### Windows

1. Clone Repository (https://git-scm.com/download/win)
1. Run `.\dev_setup.bat` as Administrator
1. IDE-specific setup (VSCode: enable pytest for unit tests in `.\tests\`)

If you're missing dependencies run `.\dev_update.bat` to install them in your venv.

### \*nix/MacOS

No setup scripts yet.

## Documentation

Documentation stuff goes to `.\docs\`.

**Navigation:**
- [BossFight API Documentation](./docs/api/overview.md)
- [BossFight Game Design Document](./docs/gamedesign/designdocument.md)

### Diagrams

Recommended modelling tool: https://www.draw.io/

Save diagrams (.xml and exported .pdf with same name) to `.\docs\diagrams\`.

### API Documentation

We generate markdown files from docstrings using *pydocmd* (https://github.com/NiklasRosenstein/pydoc-markdown).
When you made changes in an API module, just run `.\generate_api_docs.bat` to update the documentation.

If you added a new module, you have to add a line to the batch script. Example for new core module:
`.\venv\Scripts\pydocmd.exe simple bossfight.core+ bossfight.core.myModule++ > .\docs\api\core.myModule.md`

### Game Design Documentation

`.\docs\gamedesign\` contains a short design document that illustrates the overall vision and a player story map that contains the detailed design decisions.

## Testing

Start the client with `python -m bossfight.client`.
You can run the server seperately with `python -m bossfight.server`, but currently it is expected that the client starts the server as a subprocess.

### Unit Tests

py.test (https://docs.pytest.org) unit tests in `.\tests\` folder.
