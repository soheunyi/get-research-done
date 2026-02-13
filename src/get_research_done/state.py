import os
import yaml
from datetime import datetime

class ResearchState:
    def __init__(self, root_dir=None):
        self.root_dir = root_dir or os.getcwd()
        self.grd_dir = os.path.join(self.root_dir, '.grd')
        self.state_path = os.path.join(self.grd_dir, 'state.md')
        self.journal_path = os.path.join(self.grd_dir, 'journal.md')
        self.experiments_path = os.path.join(self.grd_dir, 'experiments.md')

    def load(self):
        """Loads frontmatter from state.md"""
        if not os.path.exists(self.state_path):
            return {}
        with open(self.state_path, 'r') as f:
            content = f.read()
            # Basic frontmatter parsing
            if content.startswith('---'):
                parts = content.split('---')
                if len(parts) >= 3:
                    return yaml.safe_load(parts[1])
        return {}

    def update(self, patches):
        """Updates fields in state.md frontmatter"""
        state = self.load()
        state.update(patches)
        state['last_update'] = datetime.now().strftime('%Y-%m-%d')
        
        with open(self.state_path, 'r') as f:
            content = f.read()
        
        body = ""
        if content.startswith('---'):
            parts = content.split('---')
            if len(parts) >= 3:
                body = '---'.join(parts[2:])
        else:
            body = content

        with open(self.state_path, 'w') as f:
            f.write('---\n')
            f.write(yaml.dump(state, default_flow_style=False))
            f.write('---\n')
            f.write(body)
        return state

    def append_journal(self, entry):
        """Appends an entry to journal.md"""
        with open(self.journal_path, 'a') as f:
            f.write(f'\n## {datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
            f.write(entry + '\n')

    def append_experiment(self, entry):
        """Appends an entry to experiments.md"""
        with open(self.experiments_path, 'a') as f:
            f.write(f'\n## {datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
            f.write(entry + '\n')
