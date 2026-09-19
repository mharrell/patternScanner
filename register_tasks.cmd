@echo off
rem One-shot registration of patternScanner's nightly scheduled tasks.
rem (Registration is the user's command; agent shells are not permitted
rem to register machine-level scheduled tasks. This script exists so the
rem user can do it by typing one short name instead of pasting paths.)
cd /d "%~dp0"
schtasks /create /tn "patternScanner-mover-pull" /xml "tools\tasks\mover_pull_task.xml" /f
schtasks /create /tn "patternScanner-gate-opener" /xml "tools\tasks\gate_opener_task.xml" /f
echo.
echo Both tasks registered (re-running is safe; /f overwrites).
pause
