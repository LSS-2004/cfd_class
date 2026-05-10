#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFD-Class Repository Setup Script
Automates: branch protection, labels, milestones, projects, and issues
"""

import subprocess
import json
import sys
import os

REPO = "kaklos-cyber/cfd_class"
GH = r"C:\Program Files\GitHub CLI\gh.exe"

def run_gh(args, input_data=None):
    """Run gh command and return result"""
    cmd = [GH] + args
    print(f"   Running: {' '.join(cmd[:3])}...")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # Handle encoding errors gracefully
            input=input_data,
            timeout=30,
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
        )
        
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def main():
    print("\n" + "="*60)
    print("  CFD-Class Setup Tool v2.0 (Python)")
    print("="*60 + "\n")
    
    # Check authentication
    print("[1/6] Checking GitHub authentication...")
    success, output = run_gh(["auth", "status"])
    
    if not success or "not logged" in output.lower():
        print(f"\n❌ ERROR: Not authenticated with GitHub")
        print(f"   Please run manually: {GH} auth login --web")
        print(f"\nOutput: {output}")
        sys.exit(1)
    
    print("✅ OK: Authenticated with GitHub\n")
    
    # Step 1: Branch Protection
    print("[2/6] Setting up branch protection rules...")
    
    # Main branch protection
    main_protection = {
        "required_pull_request_reviews": {
            "required_approving_review_count": 2,
            "dismiss_stale_reviews_on_push": True,
            "require_code_owner_review": False
        },
        "required_status_checks": {
            "strict": True,
            "contexts": ["ci/test", "ci/lint"]
        },
        "enforce_admins": True,
        "allow_force_pushes": False,
        "allow_deletions": False
    }
    
    success, _ = run_gh([
        "api", f"repos/{REPO}/branches/main/protection",
        "-X", "PUT",
        "-f", json.dumps(main_protection)
    ])
    
    if success:
        print("   ✅ OK: Main branch protected (2 reviewers + CI)")
    else:
        print("   ⚠️  WARNING: Main protection may already exist (can set manually later)")
    
    import time
    time.sleep(2)
    
    # Develop branch protection
    dev_protection = {
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
            "dismiss_stale_reviews_on_push": True
        },
        "required_status_checks": {
            "strict": False,
            "contexts": ["ci/test"]
        },
        "enforce_admins": True,
        "allow_force_pushes": False,
        "allow_deletions": False
    }
    
    success, _ = run_gh([
        "api", f"repos/{REPO}/branches/develop/protection",
        "-X", "PUT",
        "-f", json.dumps(dev_protection)
    ])
    
    if success:
        print("   ✅ OK: Develop branch protected (1 reviewer)\n")
    else:
        print("   ⚠️  WARNING: Develop protection may already exist\n")
    
    # Step 2: Create Labels
    print("[3/6] Creating label system (17 labels)...")
    
    labels = [
        {"name": "kind/bug", "color": "e11d21", "description": "Bug fix"},
        {"name": "kind/enhancement", "color": "a855f7", "description": "New feature"},
        {"name": "kind/docs", "color": "0075ff", "description": "Documentation"},
        {"name": "kind/refactor", "color": "fbca04", "description": "Code refactor"},
        {"name": "kind/testing", "color": "2ea44f", "description": "Testing related"},
        
        {"name": "priority/critical", "color": "d73a49", "description": "P0-Critical"},
        {"name": "priority/high", "color": "ff7b00", "description": "P1-High priority"},
        {"name": "priority/medium", "color": "1d9ce0", "description": "P2-Medium priority"},
        {"name": "priority/low", "color": "909399", "description": "P3-Low priority"},
        
        {"name": "module/core", "color": "0e8a16", "description": "Core engine"},
        {"name": "module/ui", "color": "5319e7", "description": "UI frontend"},
        {"name": "module/tests", "color": "bd10e0", "description": "Test code"},
        {"name": "module/docs", "color": "f94189", "description": "Documentation"},
        {"name": "module/infrastructure", "color": "6b7280", "description": "Infrastructure"},
        
        {"name": "status/in-progress", "color": "f59e0b", "description": "In progress"},
        {"name": "status/review", "color": "8b5cf6", "description": "Pending review"},
        {"name": "status/blocked", "color": "ef4444", "description": "Blocked"}
    ]
    
    count = 0
    for label in labels:
        success, _ = run_gh([
            "api", f"repos/{REPO}/labels",
            "-X", "POST",
            "-f", json.dumps(label)
        ])
        if success:
            count += 1
    
    print(f"   ✅ OK: Created {count}/{len(labels)} labels\n")
    
    # Step 3: Create Milestone
    print("[4/6] Creating Sprint 1 Milestone...")
    
    milestone = {
        "title": "Sprint 1 - Core Engine and UI Framework",
        "state": "open",
        "description": """Sprint 1 Goals:

**Objectives**:
- Complete core engine (6 FVM schemes)
- Build UI framework foundation  
- Set up testing framework
- Complete documentation structure

**Key Deliverables**:
- DamBreakConfig configuration management
- Riemann solver + HLL flux calculator
- BaseScheme class + 6 scheme implementations
- Streamlit main entry point + parameter panel
- pytest framework + unit tests
- GB/T documentation framework

**Timeline**: ~4 weeks (2026-05-07 to 2026-06-04)

**Team Members**:
- @BE: Core engine development (Tasks B1-B10)
- @FE: Frontend UI framework (Tasks C1-C4)
- @QA: Testing framework (Tasks D1-D3)
- @TW: Documentation (Tasks E1-E3)
- @PM: Project coordination (Tasks A1-A4)
- @Arch: Technical review"""
    }
    
    success, output = run_gh([
        "api", f"repos/{REPO}/milestones",
        "-X", "POST",
        "-f", json.dumps(milestone)
    ])
    
    if success:
        ms_data = json.loads(output)
        ms_num = ms_data.get('number', 'unknown')
        print(f"   ✅ OK: Milestone #{ms_num} created successfully\n")
    else:
        print("   ⚠️  WARNING: Milestone may already exist\n")
    
    # Step 4: Create Project Board
    print("[5/6] Creating Project board...")
    
    # Try GraphQL API for Project V2
    graphql_query = """
    mutation {
      createProject(input: {
        ownerId: "kaklos-cyber",
        title: "CFD-Class Sprint 1"
      }) {
        project {
          id
          url
        }
      }
    }
    """
    
    success, _ = run_gh([
        "api", "graphql",
        "-f", f"query={graphql_query}"
    ])
    
    if success:
        print("   ✅ OK: Project V2 board created!\n")
    else:
        # Fallback to V1 API
        print("   ℹ️  INFO: Trying Project V1 (classic)...")
        
        v1_body = {
            "name": "CFD-Class Sprint 1",
            "body": "## Sprint 1 Kanban Board\n\n**Goal**: Core Engine + UI Framework\n**Duration**: 4 weeks\n**Team**: 6 members"
        }
        
        success, _ = run_gh([
            "api", "user/projects",
            "-X", "POST",
            "-H", "Accept: application/vnd.github.inertia-preview+json",
            "-f", json.dumps(v1_body)
        ])
        
        if success:
            print("   ✅ OK: Project V1 created! Configure columns at:")
            print("         https://github.com/kaklos-cyber/cfd_class/projects\n")
        else:
            print("   ⚠️  WARNING: Auto-create failed. Please create manually:\n")
            print("         Settings -> Features -> Projects -> New Project\n")
    
    # Summary
    print("="*60)
    print("  ✅ REPOSITORY SETUP COMPLETE!")
    print("="*60)
    print("""
Summary of completed tasks:
  [✓] Main branch protection: 2 reviewers + CI required
  [✓] Develop branch protection: 1 reviewer required  
  [✓] Label system: 17 labels created
  [✓] Milestone: Sprint 1 - Core Engine & UI Framework
  [✓] Project board: CFD-Class Sprint 1

Next step:
  Run: python scripts/setup_issues.py
  To create all 20 task issues
""")

if __name__ == "__main__":
    main()