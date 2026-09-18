@echo off
rem Nightly mover-universe pull (mover-universe design, analysis/mover_universe_design.md §3).
rem - Captures the session's mover roster (first capture wins; later runs no-op).
rem - Pulls the roster names' 1-min bars into data\intraday_movers (backfills
rem   the rolling 7-day window), then QA.
rem - Proposed task: patternScanner-mover-pull, daily 22:35 (after the 22:05
rem   S&P pull); registration is the user's command (see INTRAday_OPERATIONS.md).
setlocal
cd /d "C:\Users\Silver Pangolin\PycharmProjects\patternScanner"
set LOG=%TEMP%\mover_pull.log
echo [%date% %time%] start >> "%LOG%"

set CSV=
for /f "tokens=1* delims= " %%a in ('python -X utf8 tools\mover_roster.py 2^>^&1 ^| findstr "CSV_PATH"') do set CSV=%%b
if "%CSV%"=="" (
  echo [%date% %time%] ERROR: roster capture produced no CSV path >> "%LOG%"
  exit /b 3
)
echo [%date% %time%] roster %CSV% >> "%LOG%"

python -X utf8 tools\fetch_intraday_bars.py --universe "%CSV%" --archive-root data\intraday_movers --qa >> "%LOG%" 2>&1
set RC=%errorlevel%
echo [%date% %time%] fetch exit=%RC% >> "%LOG%"
exit /b %RC%
