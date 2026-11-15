
# --- [FN-WIKILIFE : MSYS2 BASH SHELL ON STARTUP] ---
export WIKILIFE_ROOT="/d/projects/wiki-live-core"
if [ -d "$WIKILIFE_ROOT" ]; then cd "$WIKILIFE_ROOT"; fi
if [ -f "Gemini.md" ] && [ -f "README.md" ] && [ -f "config/mutual_lock.json" ]; then
    export WIKILIFE_LOCK="LOCKED_OK"
else
    export WIKILIFE_LOCK="CHECK_REQ"
fi
export PS1="[FN-WIKILIFE | BASH] \w \$ "
ts=$(date "+%Y-%m-%d %H:%M:%S")
mkdir -p config
echo "[$ts] MSYS2_BASH_STARTUP | Trunk: $(git branch --show-current 2>/dev/null) | MutualLock: $WIKILIFE_LOCK" >> config/startup_bash.log
echo -e "\033[36m[FN-WIKILIFE | MSYS2 BASH STARTUP] Trunk: $(git branch --show-current 2>/dev/null) | MutualLock: $WIKILIFE_LOCK | Log: config/startup_bash.log\033[0m"
