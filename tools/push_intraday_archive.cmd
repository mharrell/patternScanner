@echo off
rem Nightly archive push for the intraday track (Task Scheduler:
rem patternScanner-intraday-push, daily 23:00, after the 22:05 pull).
rem - Skips if a pull is still running (.lock present).
rem - Commits only data/intraday (never other files).
rem - Fast-forwards main first so a rejected push self-heals.
setlocal
cd /d "C:\Users\Silver Pangolin\PycharmProjects\patternScanner"
rem The S&P 600 contains a ticker literally named CON (a Windows reserved
rem device name); git-for-Windows refuses CON.* unless core.protectNTFS is
rem off, so the push sets it repo-local (self-healing).
git config core.protectNTFS false
set LOG=%TEMP%\intraday_push.log
echo [%date% %time%] start >> "%LOG%"
if exist "data\intraday\.lock" (
  echo [%date% %time%] SKIP: pull still running >> "%LOG%"
  exit /b 0
)
git add data/intraday data/paper >> "%LOG%" 2>&1
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "Intraday archive + paper log: nightly pull (auto)" -- data/intraday data/paper >> "%LOG%" 2>&1
)
git pull --ff-only origin main >> "%LOG%" 2>&1
if errorlevel 1 (
  echo [%date% %time%] ff-only pull failed; skipping push >> "%LOG%"
  exit /b 0
)
git push origin main >> "%LOG%" 2>&1
echo [%date% %time%] exit=%errorlevel% >> "%LOG%"
exit /b %errorlevel%
