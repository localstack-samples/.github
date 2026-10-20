#!/usr/bin/env python3
"""Write STATUS.md: every public, unarchived repository in the organization, with its
description and a CI badge for the workflow that deploys and tests the sample.

Uses the GitHub REST API. Set GITHUB_TOKEN (or GH_TOKEN) to avoid the unauthenticated
rate limit. Exceptions to the rules below go in status.toml.
"""
import json
import os
import re
import sys
import tomllib
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORG = "localstack-samples"
API = "https://api.github.com"

# Workflows that do not test the sample never get the badge
NON_TEST = re.compile(r"keep ?alive|preview|sync|lint|pre-commit|release|dependabot|dependency|codeql|inject state|create cloud pod on", re.I)
# Skipped when a repository has another test workflow
SECONDARY = re.compile(r"cloud pod|snapshot", re.I)

# Sections in page order; a repository goes into the first one whose rule matches its name or topics
# (Kubernetes samples that run on LocalStack for AWS stay in AWS; status.toml places the exceptions)
SECTIONS = [
    ("Snowflake", re.compile(r"snowflake|polaris")),
    ("Azure", re.compile(r"azure|^aks")),
    ("LocalStack features", re.compile(r"cloud-pods|chaos|replicator|init-hooks|snapshot|extension")),
]
DEFAULT_SECTION = "AWS"
PAGE_ORDER = ["AWS", "Snowflake", "Azure", "Kubernetes", "LocalStack features"]


def request(url):
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as response:
        return json.load(response), response.headers.get("Link", "")


def get_object(path):
    return request(f"{API}{path}")[0]


def get_list(path):
    """GET a list endpoint and follow its pagination."""
    url, items = f"{API}{path}", []
    while url:
        body, links = request(url)
        items += body
        url = next((part.split(";")[0].strip(" <>") for part in links.split(",") if 'rel="next"' in part), None)
    return items


def section(repo, overrides):
    if repo["name"] in overrides:
        return overrides[repo["name"]]
    for name, rule in SECTIONS:
        if rule.search(repo["name"].lower()) or any(rule.search(topic) for topic in repo.get("topics", [])):
            return name
    return DEFAULT_SECTION


def main_workflow(repo, overrides):
    """The workflow file that gets the badge and whether it is active, or (None, False) without a test workflow."""
    workflows = get_object(f"/repos/{ORG}/{repo['name']}/actions/workflows?per_page=100")["workflows"]
    workflows = [w for w in workflows if w["path"].startswith(".github/workflows/")]
    by_file = {Path(w["path"]).name: w for w in workflows}
    if repo["name"] in overrides:
        chosen = by_file.get(overrides[repo["name"]])
        if not chosen:
            sys.exit(f"status.toml: {repo['name']} has no workflow {overrides[repo['name']]}")
        return Path(chosen["path"]).name, chosen["state"] == "active"
    tests = sorted((w for w in workflows if not NON_TEST.search(w["name"])), key=lambda w: w["path"])
    # GitHub disables scheduled workflows after 60 days without activity; such a workflow is only picked
    # when the repository has no active test workflow, and then shows as disabled
    tests = [w for w in tests if w["state"] == "active"] or tests
    tests = [w for w in tests if not SECONDARY.search(w["name"])] or tests
    tests = [w for w in tests if "integration" in w["name"].lower()] or tests
    if not tests:
        return None, False
    return Path(tests[0]["path"]).name, tests[0]["state"] == "active"


def badge(repo, workflow, active):
    if not workflow:
        return "No CI"
    runs = f"https://github.com/{ORG}/{repo['name']}/actions/workflows/{workflow}"
    if not active:
        return f"[![CI: disabled](https://img.shields.io/badge/CI-disabled-lightgrey)]({runs})"
    branch = urllib.parse.quote(repo["default_branch"], safe="")
    image = f"https://img.shields.io/github/actions/workflow/status/{ORG}/{repo['name']}/{workflow}?branch={branch}&label=CI"
    return f"[![CI]({image})]({runs})"


def cell(text):
    return " ".join((text or "").split()).replace("|", "\\|")


def main():
    config = tomllib.loads((ROOT / "status.toml").read_text())
    exclude = set(config.get("exclude", []))
    repos = [r for r in get_list(f"/orgs/{ORG}/repos?type=public&per_page=100")
             if not r["archived"] and not r["private"] and r["name"] not in exclude]
    rows = {}
    for repo in sorted(repos, key=lambda r: r["name"].lower()):
        workflow, active = main_workflow(repo, config.get("workflow", {}))
        rows.setdefault(section(repo, config.get("area", {})), []).append(
            f"| [{repo['name']}](https://github.com/{ORG}/{repo['name']}) | {cell(repo['description'])} | {badge(repo, workflow, active)} |")

    lines = [
        "# Sample status",
        "",
        "<!-- Generated by scripts/generate_status.py. Edit status.toml or the script, not this file. -->",
        "",
        f"This is the status of the public sample applications in the [{ORG}](https://github.com/{ORG}) organization. "
        "Each badge shows the latest run of the sample's smoke test workflow on its default branch; select it to see the runs. "
        "\"CI disabled\" means GitHub turned the workflow off after 60 days without activity. "
        "A workflow regenerates this page every week.",
    ]
    for name in PAGE_ORDER + sorted(set(rows) - set(PAGE_ORDER)):
        if name not in rows:
            continue
        lines += ["", f"## {name}", "", "| Sample | Description | CI |", "|---|---|---|", *rows[name]]
    (ROOT / "STATUS.md").write_text("\n".join(lines) + "\n")
    print(f"STATUS.md: {len(repos)} repositories in {len(rows)} sections")


if __name__ == "__main__":
    main()
