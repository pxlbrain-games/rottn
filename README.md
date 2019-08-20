# ROTTN

Indie game with only procedurally generated boss levels. Online/LAN-Coop. Boss-AI uses Deep Q Neural Nets in order to adapt to and learn from the player during a fight.

## Development Environment 

This project is using Python 3.6.5 (https://www.python.org/downloads/release/python-365/)

1. Install poetry (https://github.com/sdispater/poetry)
1. Run `poetry install`

## Documentation

**Navigation:**
- [ROTTN Game Design Document](./designdocument.md)
- [Player Story Map](https://app.wisemapping.com/c/maps/747726/public)

### Game Design Documentation

`.\designdocument.md` contains a [short design document](./docs/gamedesign/designdocument.md) that illustrates the overall vision and any documents we might come up with to describe game design aspects in the future. A [*Player Story Map*](https://app.wisemapping.com/c/maps/747726/edit) is maintained in [WiseMapping](https://app.wisemapping.com), an open source mind mapping tool, and contains a more detailed view on the features of the game.

## Testing

Start the client with `poetry run python -m rottn.client`.
You can run the server seperately with `poetry run python -m rottn.server`, but currently it is expected that the client starts the server as a subprocess.

### Unit Tests

Run `poetry run pytest tests`

![Screenshot](/screenshot.png)

