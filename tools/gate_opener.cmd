@echo off
rem Gate opener for the §5-gated intraday campaigns (Task Scheduler:
rem patternScanner-gate-opener, daily 23:45, after the 23:00 push).
rem - Runs tools/gate_opener.py: each gated tool refuses (exit 2) on unmet
rem   floors WITHOUT consuming its one-shot; exit 0 = measured (once).
rem - Measured results are archived to data/measurements/<tool>/ (tracked).
rem - Never writes verdicts (pre-reg §8 + ledger are session work).
setlocal
cd /d "C:\Users\Silver Pangolin\PycharmProjects\patternScanner"
set LOG=%TEMP%\gate_opener.log
echo [%date% %time%] start >> "%LOG%"
if exist "data\intraday\.lock" (
  echo [%date% %time%] SKIP: pull still running >> "%LOG%"
  exit /b 0
)
python -X utf8 tools\gate_opener.py >> "%LOG%" 2>&1
echo [%date% %time%] exit=%errorlevel% >> "%LOG%"
exit /b %errorlevel%