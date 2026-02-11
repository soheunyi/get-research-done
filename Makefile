PYTHON ?= python3
DEST ?= .

.PHONY: \
	sync-skills check-skills sync-codex sync-agy \
	install-runtime install-codex install-claude install-opencode install-gemini install-agy install-legacy-codex \
	install-core install-all install-help

sync-skills:
	$(PYTHON) scripts/sync_skill_boilerplate.py --fix

sync-codex: sync-skills
	$(PYTHON) scripts/sync_codex_wrappers.py

check-skills:
	$(PYTHON) scripts/sync_skill_boilerplate.py --check

sync-agy:
	$(PYTHON) scripts/sync_agy_wrappers.py

install-runtime:
	mkdir -p "$(DEST)/.grd/templates" "$(DEST)/.grd/workflows"
	cp -R templates/. "$(DEST)/.grd/templates/"
	cp -R workflows/. "$(DEST)/.grd/workflows/"

install-codex: install-runtime
	mkdir -p "$(DEST)/.agents/skills"
	cp -R skills/. "$(DEST)/.agents/skills/"

install-claude: install-runtime
	mkdir -p "$(DEST)/.claude/skills"
	cp -R skills/. "$(DEST)/.claude/skills/"

install-opencode: install-runtime
	mkdir -p "$(DEST)/.opencode/skills"
	cp -R skills/. "$(DEST)/.opencode/skills/"

install-gemini: install-runtime
	mkdir -p "$(DEST)/.gemini/skills"
	cp -R skills/. "$(DEST)/.gemini/skills/"

install-agy: install-runtime
	mkdir -p "$(DEST)/.agent/skills"
	cp -R agy/skills/. "$(DEST)/.agent/skills/"

install-legacy-codex: install-runtime
	mkdir -p "$(DEST)/.codex/skills"
	cp -R skills/. "$(DEST)/.codex/skills/"

install-core: install-runtime install-codex install-claude install-opencode install-gemini

install-all:
	bash scripts/install.sh "$(DEST)"

install-help:
	@echo "Install targets (use DEST=/path/to/repo):"
	@echo "  make install-runtime DEST=..."
	@echo "  make install-codex DEST=..."
	@echo "  make install-claude DEST=..."
	@echo "  make install-opencode DEST=..."
	@echo "  make install-gemini DEST=..."
	@echo "  make install-agy DEST=..."
	@echo "  make install-legacy-codex DEST=..."
	@echo "  make install-core DEST=...      # runtime + codex/claude/opencode/gemini"
	@echo "  make install-all DEST=...       # full installer script"
