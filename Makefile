PYTHON ?= python3
DEST ?= .
DEST_RESOLVED := $(if $(filter ~,$(DEST)),$(HOME),$(patsubst ~/%,$(HOME)/%,$(DEST)))

.PHONY: \
	sync-skills check-skills check-skill-lengths check-skill-references check-questioning-policy sync-codex sync-agy \
	install-runtime install-codex install-claude install-opencode install-gemini \
	install-core install-all install-help

sync-skills:
	$(PYTHON) scripts/sync_skill_boilerplate.py --fix

sync-codex: sync-skills
	$(PYTHON) scripts/sync_codex_wrappers.py

check-skill-lengths:
	$(PYTHON) scripts/check_skill_lengths.py

check-skill-references:
	$(PYTHON) scripts/check_skill_references.py --strict-mentions

check-questioning-policy:
	$(PYTHON) scripts/check_questioning_policy.py

check-skills:
	$(PYTHON) scripts/sync_skill_boilerplate.py --check
	$(PYTHON) scripts/check_skill_lengths.py
	$(PYTHON) scripts/check_skill_references.py --strict-mentions
	$(PYTHON) scripts/check_questioning_policy.py

sync-agy:
	$(PYTHON) scripts/sync_agy_wrappers.py

install-runtime:
	mkdir -p "$(DEST_RESOLVED)/.grd/templates" "$(DEST_RESOLVED)/.grd/workflows"
	cp -R templates/. "$(DEST_RESOLVED)/.grd/templates/"
	cp -R workflows/. "$(DEST_RESOLVED)/.grd/workflows/"

install-codex: install-runtime
	mkdir -p "$(DEST_RESOLVED)/.agents/skills"
	cp -R skills/. "$(DEST_RESOLVED)/.agents/skills/"

install-claude: install-runtime
	mkdir -p "$(DEST_RESOLVED)/.claude/skills"
	cp -R skills/. "$(DEST_RESOLVED)/.claude/skills/"

install-opencode: install-runtime
	mkdir -p "$(DEST_RESOLVED)/.opencode/skills"
	cp -R skills/. "$(DEST_RESOLVED)/.opencode/skills/"

install-gemini: install-runtime
	mkdir -p "$(DEST_RESOLVED)/.gemini/skills"
	cp -R skills/. "$(DEST_RESOLVED)/.gemini/skills/"

install-core: install-runtime install-codex install-claude install-opencode install-gemini

install-all:
	bash scripts/install.sh "$(DEST_RESOLVED)"

install-help:
	@echo "Install targets (use DEST=/path/to/repo):"
	@echo "  make install-runtime DEST=..."
	@echo "  make install-codex DEST=..."
	@echo "  make install-claude DEST=..."
	@echo "  make install-opencode DEST=..."
	@echo "  make install-gemini DEST=..."
	@echo "  make install-core DEST=...      # runtime + codex/claude/opencode/gemini"
	@echo "  make install-all DEST=...       # full installer script"
