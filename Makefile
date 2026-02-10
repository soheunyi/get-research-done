PYTHON ?= python3

.PHONY: sync-skills check-skills

sync-skills:
	$(PYTHON) scripts/sync_skill_boilerplate.py --fix

check-skills:
	$(PYTHON) scripts/sync_skill_boilerplate.py --check
