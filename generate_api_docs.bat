@ECHO off
ECHO Make sure CPython venv exists.
ECHO Doc generation doesn't work with PyPy.
PAUSE
ECHO ##################################
ECHO Generating Markdown files ...
ECHO ##################################
.\venv\Scripts\pydocmd.exe simple bossfight.server+ bossfight.server.game_loop++ > .\docs\api\server.game_loop.md
.\venv\Scripts\pydocmd.exe simple bossfight.core+ bossfight.core.activities++ > .\docs\api\core.activities.md
.\venv\Scripts\pydocmd.exe simple bossfight.client+ bossfight.client.server_manager++ > .\docs\api\client.server_manager.md
.\venv\Scripts\pydocmd.exe simple bossfight.client+ bossfight.client.config++ > .\docs\api\client.config.md
.\venv\Scripts\pydocmd.exe simple bossfight.client+ bossfight.client.player_controls++ > .\docs\api\client.player_controls.md
.\venv\Scripts\pydocmd.exe simple bossfight.client+ bossfight.client.ui++ > .\docs\api\client.ui.md
.\venv\Scripts\pydocmd.exe simple bossfight.client.scenes+ bossfight.client.scenes.levelScene++ > .\docs\api\client.scenes.levelScene.md
ECHO ##################################
ECHO Doc generation completed.
ECHO Remember: If you add a new module
ECHO    you must add it to this script!
ECHO ##################################
PAUSE