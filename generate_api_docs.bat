@ECHO off
ECHO Make sure CPython venv exists.
ECHO Doc generation doesn't work with PyPy.
PAUSE
ECHO ##################################
ECHO Generating Markdown files ...
ECHO ##################################
.\venv\Scripts\pydocmd.exe simple bossfight.server+ bossfight.server.gameService++ > .\docs\api\server.gameService.md
.\venv\Scripts\pydocmd.exe simple bossfight.server+ bossfight.server.gameLoop++ > .\docs\api\server.gameLoop.md
.\venv\Scripts\pydocmd.exe simple bossfight.core+ bossfight.core.gameServiceProtocol++ > .\docs\api\core.gameServiceProtocol.md
.\venv\Scripts\pydocmd.exe simple bossfight.core+ bossfight.core.sharedGameData++ > .\docs\api\core.sharedGameData.md
.\venv\Scripts\pydocmd.exe simple bossfight.core+ bossfight.core.mixins++ > .\docs\api\core.mixins.md
.\venv\Scripts\pydocmd.exe simple bossfight.client+ bossfight.client.gameServiceConnection++ > .\docs\api\client.gameServiceConnection.md
.\venv\Scripts\pydocmd.exe simple bossfight.client+ bossfight.client.serverManager++ > .\docs\api\client.serverManager.md
.\venv\Scripts\pydocmd.exe simple bossfight.client+ bossfight.client.config++ > .\docs\api\client.config.md
ECHO ##################################
ECHO Doc generation completed.
ECHO Remember: If you add a new module
ECHO    you must add it to this script!
ECHO ##################################
PAUSE