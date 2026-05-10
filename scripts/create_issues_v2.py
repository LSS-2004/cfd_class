#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFD-Class Issue Creation Script - Using gh issue create (simpler API)
"""

import subprocess
import json
import sys
import os

REPO = "kaklos-cyber/cfd_class"
GH = r"C:\Program Files\GitHub CLI\gh.exe"

def run_gh(args):
    """Run gh command with UTF-8 encoding"""
    cmd = [GH] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60,
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def create_issue(title, body, labels, assignees):
    """Create a GitHub issue using gh issue create command"""
    # Build command arguments for gh issue create
    args = [
        "issue", "create",
        "--repo", REPO,
        "--title", title,
        "--body", body,
    ]
    
    # Add labels (multiple --label flags) - skip if label doesn't exist yet
    # We'll add labels later after creating them
    # for label in labels:
    #     args.extend(["--label", label])
    
    # Add assignees (multiple --assignee flags)
    for assignee in assignees:
        args.extend(["--assignee", assignee])
    
    success, output = run_gh(args)
    
    if success:
        # Parse output to extract issue number and URL
        # Output format: "https://github.com/.../issues/NUMBER"
        if "issues/" in output:
            parts = output.split("issues/")
            if len(parts) > 1:
                num = parts[1].strip()
                return True, num, output
        return True, "?", output
    return False, None, output

def main():
    print("\n" + "="*70)
    print("  Creating Sprint 1 Task Issues (using gh issue create)")
    print("="*70 + "\n")
    
    # Check auth
    success, _ = run_gh(["auth", "status"])
    if not success:
        print("ERROR: Not authenticated. Run: gh auth login --web")
        sys.exit(1)
    
    # Issue templates (24 issues total for complete coverage)
    issues = [
        # Batch A: Infrastructure (@PM) - 4 tasks
        {
            "title": "chore: Configure main/develop branch protection rules (#A1)",
            "body": """## Task Description
Configure GitHub repository branch protection rules.

## Steps
- Set main branch: require PR, 2 approvals, CI checks
- Set develop branch: require PR, 1 approval

## Acceptance Criteria
- [ ] Main branch requires 2 reviewer approval
- [ ] CI tests must pass before merge
- [ ] Force push disabled""",
            "labels": ["chore", "priority/critical", "module/infrastructure"],
            "assignees": ["PM"]
        },
        {
            "title": "chore: Complete label system and milestone setup (#A2)",
            "body": """## Task Description
Create complete label system and Sprint 1 milestone.

## Labels (17 total)
- Type: kind/bug, kind/enhancement, kind/docs, kind/refactor, kind/testing
- Priority: priority/critical, priority/high, priority/medium, priority/low
- Module: module/core, module/ui, module/tests, module/docs, module/infrastructure
- Status: status/in-progress, status/review, status/blocked

## Milestone
- Title: 'Sprint 1 - Core Engine & UI Framework'
- Duration: ~4 weeks""",
            "labels": ["chore", "priority/high", "module/infrastructure"],
            "assignees": ["PM"]
        },
        {
            "title": "docs: Publish team collaboration workflow guide (#A3)",
            "body": """## Task Description
Publish comprehensive team workflow guide.

## Content
1. Quick Start Guide (5 min)
2. Daily Workflow
3. Git Commands Cheatsheet
4. Issue Management
5. Code Review Process

## Output
TEAM_WORKFLOW.md in repository root""",
            "labels": ["docs", "priority/high", "module/docs"],
            "assignees": ["PM"]
        },
        {
            "title": "chore: Set up Projects Kanban board structure (#A4)",
            "body": """## Task Description
Set up GitHub Projects Kanban board.

## Columns
- Backlog (Todo)
- In Progress (WIP <=3/person)
- Review (Pending code review)
- Testing (QA testing)
- Done (Completed)

## Automation
Auto-move issues based on status labels.""",
            "labels": ["chore", "priority/medium", "module/infrastructure"],
            "assignees": ["PM"]
        },
        
        # Batch B: Core Engine (@BE) - 10 tasks
        {
            "title": "feat(core): Implement DamBreakConfig configuration class (#B1)",
            "body": """## Task Description
Implement DamBreakConfig dataclass for simulation parameters.

## Location
src/core/config.py

## Fields
- Domain: L, nx, x_dam
- IC: h_L, h_R, u_L, u_R
- Physics: g
- Time: t_end, cfl

## Methods
validate(), dx property, x property, JSON serialization""",
            "labels": ["feat", "priority/critical", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement exact Riemann solver (#B2)",
            "body": """## Task Description
Implement exact Riemann solver for shallow water equations.

## Interface
solve(hL, uL, hR, uR) -> RiemannState
sample_solution(x, t, x0) -> (h, u)

## Acceptance
- Pass Toriel test problems
- Handle dry bed cases
- < 1ms per solve call""",
            "labels": ["feat", "priority/critical", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement HLL approximate solver (#B3)",
            "body": """## Task Description
Implement HLL approximate Riemann solver.

## Formula
F_HLL = (S_R*F_L - S_L*F_R + S_L*S_R*(U_R-U_L)) / (S_R-S_L)

## Advantages
- Robust (no iteration needed)
- Fast (O(1) computation)
- Preserves positivity naturally""",
            "labels": ["feat", "priority/critical", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement BaseScheme abstract class (#B4)",
            "body": """## Task Description
Create abstract base class for all FVM schemes.

## Pattern
Template Method pattern enforcing consistent structure.

## Key Methods
- compute_flux(UL, UR) [abstract]
- compute_time_step(U) [abstract]
- advance(dt) [template]
- run_simulation() -> SimulationResult""",
            "labels": ["feat", "priority/critical", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement First-Order Upwind scheme (#B5)",
            "body": """## Task Description
Implement First-Order Upwind (Rusanov flux).

## Characteristics
- Order: 1st order O(dx)
- Very robust but highly diffusive
- CFL <= 1.0

## Testing
- Convergence test (verify 1st order)
- Dam break vs exact solution""",
            "labels": ["feat", "priority/high", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement Lax-Friedrichs scheme (#B6)",
            "body": """## Task Description
Implement Local Lax-Friedrichs (Rusanov) scheme.

## Formula
Same as Upwind but centered diffusion.

## Comparison with Upwind
- Centered vs upwind-biased
- More isotropic diffusion""",
            "labels": ["feat", "priority/high", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement Lax-Wendroff scheme (#B7)",
            "body": """## Task Description
Implement 2nd-order Lax-Wendroff scheme.

## Two-Step Method
Predictor + Corrector formula

## Properties
- 2nd order O(dx^2)
- Oscillatory near shocks
- Good for smooth flows""",
            "labels": ["feat", "priority/high", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement MacCormack scheme (#B8)",
            "body": """## Task Description
Implement MacCormack predictor-corrector scheme.

## Algorithm
Predictor (forward diff) + Corrector (backward diff)

## Historical Note
Developed by Robert MacCormack at NASA Ames (1969). Used in Space Shuttle simulations.""",
            "labels": ["feat", "priority/high", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement Beam-Warming scheme (#B9)",
            "body": """## Task Description
Implement Beam-Warming one-sided backward difference scheme.

## Spatial Discretization
dF/dx ~ (3F_i - 4F_{i-1} + F_{i-2}) / (2dx)

## Properties
- 2nd order accuracy
- Downwind bias
- Good introduction to implicit methods""",
            "labels": ["feat", "priority/medium", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement Fromm scheme (#B10)",
            "body": """## Task Description
Implement Fromm's averaged scheme (Upwind + Lax-Wendroff).

## Formula
U_Fromm = 0.5*(U_Upwind + U_LW)

## Trade-offs
- Reduced oscillations vs pure LW
- Reduced diffusion vs pure upwind
- Precedes modern flux limiters""",
            "labels": ["feat", "priority/medium", "module/core"],
            "assignees": ["BE"]
        },
        
        # Batch C: Frontend UI (@FE) - 4 tasks
        {
            "title": "feat(ui): Create Streamlit main application entry point (#C1)",
            "body": """## Task Description
Create Streamlit app with multi-page structure.

## Pages
- streamlit_app.py (Main dashboard)
- pages/1_Simulation.py
- pages/2_Comparison.py
- pages/3_Theory.py

## Layout
Header, Navigation cards, Metrics overview, About section""",
            "labels": ["feat", "priority/critical", "module/ui"],
            "assignees": ["FE"]
        },
        {
            "title": "feat(ui): Build parameter input panel component (#C2)",
            "body": """## Task Description
Build reusable parameter input panel.

## Sections
1. Domain Settings (L, nx, x_dam)
2. Initial Conditions (h_L, h_R, u_L, u_R)
3. Numerical Parameters (g, cfl, t_end)
4. Scheme Selection (multi-select)

## Features
Validation, Tooltips, Smart defaults, Presets""",
            "labels": ["feat", "priority/critical", "module/ui"],
            "assignees": ["FE"]
        },
        {
            "title": "feat(ui): Implement visualization and animation system (#C3)",
            "body": """## Task Description
Create visualization system for simulation results.

## Components
- Height profile plot (with fill)
- Velocity profile plot
- Animation system (matplotlib)
- Streamlit integration (time slider, playback)

## Export
PNG/SVG, CSV data, Comparison overlay""",
            "labels": ["feat", "priority/critical", "module/ui"],
            "assignees": ["FE"]
        },
        {
            "title": "feat(ui): Build scheme comparison dashboard (#C4)",
            "body": """## Task Description
Build dedicated comparison dashboard page.

## Layout
Sidebar: Parameters + Scheme selection
Main area: Control bar, Height comparison, Velocity comparison, Metrics table, Performance chart

## Features
Multi-scheme overlay (2-6), Synchronized time slider, Auto-computed metrics""",
            "labels": ["feat", "priority/high", "module/ui"],
            "assignees": ["FE"]
        },
        
        # Batch D: Testing (@QA) - 3 tasks
        {
            "title": "test(qa): Set up pytest framework and CI integration (#D1)",
            "body": """## Task Description
Set up pytest framework with CI/CD.

## Structure
tests/
- conftest.py (fixtures)
- unit/ (unit tests)
- integration/ (integration tests)
- performance/ (benchmarks)

## Configuration
pytest.ini, .github/workflows/ci.yml
Target: >=80% coverage""",
            "labels": ["test", "priority/critical", "module/tests"],
            "assignees": ["QA"]
        },
        {
            "title": "test(qa): Write core engine unit tests (#D2)",
            "body": """## Task Description
Write unit tests for B1-B10 modules.

## Coverage Targets
- B1 Config: >=90% (15 tests)
- B2 Exact Riemann: >=85% (20 tests)
- B3 HLL Solver: >=85% (15 tests)
- B4-B10 Schemes: >=85-90% each

## Test Categories
Validation logic, Properties, Algorithms, Edge cases, Physical validity""",
            "labels": ["test", "priority/high", "module/tests"],
            "assignees": ["QA"]
        },
        {
            "title": "test(qa): Create integration and regression tests (#D3)",
            "body": """## Task Description
Create integration and regression test suites.

## Integration Tests
Full pipeline execution, Multi-scheme comparison, Parameter variation, Edge cases

## Regression Tests
Reference solutions for all 6 schemes, Detect unintended changes, Weekly CI schedule""",
            "labels": ["test", "priority/medium", "module/tests"],
            "assignees": ["QA"]
        },
        
        # Batch E: Documentation (@TW) - 3 tasks
        {
            "title": "docs(tw): Complete SRS Software Requirements Specification (#E1)",
            "body": """## Task Description
Complete SRS document following GB/T 9385-2008 standard.

## Sections
1. Introduction (purpose, scope, definitions)
2. Overall description (product perspective, functions)
3. Specific requirements (functional, non-functional)
4. External interfaces
5. Other requirements (performance, design constraints)

## Standard Compliance
GB/T 9385-2008 structure and terminology""",
            "labels": ["docs", "priority/high", "module/docs"],
            "assignees": ["TW"]
        },
        {
            "title": "docs(tw): Complete SDD Software Design Document (#E2)",
            "body": """## Task Description
Complete Software Design Document (SDD).

## Sections
1. Introduction
2. System architecture
3. Detailed design (config, riemann, schemes, UI)
4. Data structures
5. Algorithms (pseudocode)
6. Interface specifications
7. Test strategy

## Diagrams
Class hierarchy, Data flow, Component interaction""",
            "labels": ["docs", "priority/high", "module/docs"],
            "assignees": ["TW"]
        },
        {
            "title": "docs(tw): Create user manual and theory guide (#E3)",
            "body": """## Task Description
Create user-facing documentation.

## User Manual
Installation guide, Quick start tutorial, Feature reference, Troubleshooting, FAQ

## Theory Guide
Shallow water equations derivation, Riemann problem explanation, Each scheme math+properties, Numerical analysis concepts, Comparison tables""",
            "labels": ["docs", "priority/medium", "module/docs"],
            "assignees": ["TW"]
        }
    ]
    
    # Create issues
    created = 0
    failed = 0
    
    for idx, issue in enumerate(issues, 1):
        print(f"\n[{idx}/{len(issues)}] Creating: {issue['title'][:60]}...")
        
        success, num, url = create_issue(
            issue['title'],
            issue['body'],
            issue['labels'],
            issue['assignees']
        )
        
        if success:
            print(f"  [OK] Created #{num}")
            created += 1
            # Small delay to avoid rate limiting
            import time
            time.sleep(0.5)
        else:
            print(f"  [FAIL] Error: {str(url)[:120]}")
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print(f"  COMPLETE: {created}/{len(issues)} issues created successfully")
    print(f"  FAILED: {failed} issues")
    print("="*70 + "\n")
    
    if created > 0:
        print(f"  View all issues at: https://github.com/{REPO}/issues")
        print("\n  Next step: Notify team members to start working on their assigned issues!")
    else:
        print("\n  ERROR: No issues were created. Please check the error messages above.")

if __name__ == "__main__":
    main()