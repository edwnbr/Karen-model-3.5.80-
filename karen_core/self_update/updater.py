import os, json
from git import Repo

class Updater:
    def __init__(self, repo_dir="."):
        self.repo_dir = repo_dir
        # safe: don't auto-init repo here; expect user to set up git or use helper
        self.proposals_file = os.path.join("karen_core", "self_update", "proposals.json")
        os.makedirs(os.path.dirname(self.proposals_file), exist_ok=True)
        if not os.path.exists(self.proposals_file):
            with open(self.proposals_file, "w") as f:
                json.dump([], f)

    def check_for_proposals(self):
        with open(self.proposals_file, "r", encoding="utf-8") as f:
            proposals = json.load(f)
        if proposals:
            return proposals[0]
        return None

    def propose_change(self, description, patch):
        with open(self.proposals_file, "r", encoding="utf-8") as f:
            proposals = json.load(f)
        proposals.append({"description": description, "patch": patch})
        with open(self.proposals_file, "w", encoding="utf-8") as f:
            json.dump(proposals, f, indent=2, ensure_ascii=False)

    def apply_change(self, proposal):
        patch = proposal.get("patch", {})
        # apply patch: map path -> new content (overwrite)
        for path, content in patch.items():
            # safety: ensure path is within repo
            abs_path = os.path.abspath(path)
            repo_root = os.path.abspath(".")
            if not abs_path.startswith(repo_root):
                raise PermissionError("Patch path outside repository root.")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        # remove applied proposal
        with open(self.proposals_file, "r", encoding="utf-8") as f:
            proposals = json.load(f)
        if proposals:
            proposals.pop(0)
        with open(self.proposals_file, "w", encoding="utf-8") as f:
            json.dump(proposals, f, indent=2, ensure_ascii=False)
