#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFD-Class Issue Creation Script - Sprint 1 Tasks (20 Issues)
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
            timeout=30,
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def create_issue(title, body, labels, assignees):
    """Create a GitHub issue using correct gh api format"""
    # Convert lists to JSON arrays for GitHub API
    labels_json = json.dumps(labels)  # ["label1","label2"]
    assignees_json = json.dumps(assignees)  # ["user1"]
    
    # Build command with separate -f flags for each field
    args = [
        "api", f"repos/{REPO}/issues",
        "-X", "POST",
        "-f", f"title={title}",
        "-f", f"body={body}",
        "-f", f"labels={labels_json}",
        "-f", f"assignees={assignees_json}"
    ]
    
    success, output = run_gh(args)
    
    if success:
        try:
            issue_info = json.loads(output)
            return True, issue_info.get('number', '?'), issue_info.get('html_url', '')
        except:
            return True, '?', 'URL parse error'
    return False, None, output

def main():
    print("\n" + "="*70)
    print("  Creating 20 Sprint 1 Task Issues")
    print("="*70 + "\n")
    
    # Check auth
    success, _ = run_gh(["auth", "status"])
    if not success:
        print("ERROR: Not authenticated. Run: gh auth login --web")
        sys.exit(1)
    
    # Issue templates (simplified for brevity)
    issues = [
        # Batch A: Infrastructure (@PM)
        {
            "title": "chore: Configure main/develop branch protection rules (#A1)",
            "body": "## Task Description\nConfigure GitHub repository branch protection rules.\n\n## Steps\n- Set main branch: require PR, 2 approvals, CI checks\n- Set develop branch: require PR, 1 approval\n\n## Acceptance Criteria\n- [ ] Main branch requires 2 reviewer approval\n- [ ] CI tests must pass before merge\n- [ ] Force push disabled",
            "labels": ["chore", "priority/critical", "module/infrastructure"],
            "assignees": ["PM"]
        },
        {
            "title": "chore: Complete label system and milestone setup (#A2)",
            "body": "## Task Description\nCreate complete label system and Sprint 1 milestone.\n\n## Labels to Create (17 total)\n- Type: kind/bug, kind/enhancement, kind/docs, kind/refactor, kind/testing\n- Priority: priority/critical, priority/high, priority/medium, priority/low\n- Module: module/core, module/ui, module/tests, module/docs, module/infrastructure\n- Status: status/in-progress, status/review, status/blocked\n\n## Milestone\n- Title: 'Sprint 1 - Core Engine & UI Framework'\n- Duration: ~4 weeks",
            "labels": ["chore", "priority/high", "module/infrastructure"],
            "assignees": ["PM"]
        },
        {
            "title": "docs: Publish team collaboration workflow guide (#A3)",
            "body": "## Task Description\nPublish comprehensive team workflow guide.\n\n## Content Structure\n1. Quick Start Guide (5 min)\n2. Daily Workflow\n3. Git Commands Cheatsheet\n4. Issue Management\n5. Code Review Process\n6. Communication Channels\n\n## Output File\nTEAM_WORKFLOW.md in repository root",
            "labels": ["docs", "priority/high", "module/docs"],
            "assignees": ["PM"]
        },
        {
            "title": "chore: Set up Projects Kanban board structure (#A4)",
            "body": "## Task Description\nSet up GitHub Projects Kanban board.\n\n## Columns\n- Backlog (Todo)\n- In Progress (WIP ≤3/person)\n- Review (Pending code review ≤5)\n- Testing (QA testing)\n- Done (Completed)\n\n## Automation\nAuto-move issues based on status labels.",
            "labels": ["chore", "priority/medium", "module/infrastructure"],
            "assignees": ["PM"]
        },
        
        # Batch B: Core Engine (@BE) - B1-B10
        {
            "title": "feat(core): Implement DamBreakConfig configuration class (#B1)",
            "body": "## Task Description\nImplement DamBreakConfig dataclass for simulation parameters.\n\n## Location\nsrc/core/config.py\n\n## Fields\n- Domain: L, nx, x_dam\n- IC: h_L, h_R, u_L, u_R\n- Physics: g\n- Time: t_end, cfl\n- Output: save_interval, output_dir\n\n## Methods\n- validate(), dx property, x property\n- Serialization (JSON)",
            "labels": ["feat", "priority/critical", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement exact Riemann solver (#B2)",
            "body": "## Task Description\nImplement exact Riemann solver for shallow water equations.\n\n## Theory\nSaint-Venant equations eigenstructure with Newton-Raphson iteration for star region.\n\n## Interface\nsolve(hL, uL, hR, uR) -> RiemannState\nsample_solution(x, t, x0) -> (h, u)\n\n## Acceptance\n- Pass Toriel test problems\n- Handle dry bed cases\n- < 1ms per solve call",
            "labels": ["feat", "priority/critical", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement HLL approximate solver (#B3)",
            "body": "## Task Description\nImplement HLL approximate Riemann solver.\n\n## Formula\nF_HLL = (S_R*F_L - S_L*F_R + S_L*S_R*(U_R-U_L)) / (S_R-S_L)\n\n## Advantages\n- Robust (no iteration needed)\n- Fast (O(1) computation)\n- Preserves positivity naturally\n\n## Wave Speed Estimates\n- Davis (1988): Two-rarefaction\n- Einfeldt (1991): PVDE-based",
            "labels": ["feat", "priority/critical", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement BaseScheme abstract class (#B4)",
            "body": "## Task Description\nCreate abstract base class for all FVM schemes.\n\n## Pattern\nTemplate Method pattern enforcing consistent structure.\n\n## Key Methods\n- compute_flux(UL, UR) [abstract]\n- compute_time_step(U) [abstract]\n- advance(dt) [template]\n- run_simulation() -> SimulationResult\n\n## Features\n- Automatic IC setup\n- Boundary conditions (transmissive)\n- Positivity preservation",
            "labels": ["feat", "priority/critical", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement First-Order Upwind scheme (#B5)",
            "body": "## Task Description\nImplement First-Order Upwind (Rusanov flux).\n\n## Characteristics\n- Order: 1st order O(Δx)\n- Very robust but highly diffusive\n- CFL ≤ 1.0\n\n## Flux Formula\nF = 0.5*(FL+FR) - 0.5*S*(UR-UL)\nwhere S = max(|u|+c)\n\n## Testing\n- Convergence test (verify 1st order)\n- Dam break vs exact solution",
            "labels": ["feat", "priority/high", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement Lax-Friedrichs scheme (#B6)",
            "body": "## Task Description\nImplement Local Lax-Friedrichs (Rusanov) scheme.\n\n## Formula\nSame as Upwind but centered diffusion.\n\n## Comparison with Upwind\n- Centered vs upwind-biased\n- More isotropic diffusion\n- Similar robustness and cost",
            "labels": ["feat", "priority/high", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement Lax-Wendroff scheme (#B7)",
            "body": "## Task Description\nImplement 2nd-order Lax-Wendroff scheme.\n\n## Two-Step Method\nPredictor: U_{i+1/2}^{n+1/2} = 0.5*(U_i^n + U_{i+1}^n) - dt/(2dx)*(F_{i+1}-F_i)\nCorrector: U_i^{n+1} = U_i^n - dt/dx*(F_{i+1/2}^{n+1/2} - F_{i-1/2}^{n+1/2})\n\n## Properties\n- 2nd order O(Δx²)\n- Oscillatory near shocks (Gibbs phenomenon)\n- Good for smooth flows",
            "labels": ["feat", "priority/high", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement MacCormack scheme (#B8)",
            "body": "## Task Description\nImplement MacCormack predictor-corrector scheme.\n\n## Algorithm\nPredictor (forward diff): U_i^* = U_i^n - dt/dx*(F_{i+1}^n - F_i^n)\nCorrector (backward diff): U_i^{n+1} = 0.5*[U_i^n + U_i^* - dt/dx*(F_i^* - F_{i-1}^*)]\n\n## Historical Note\nDeveloped by Robert MacCormack at NASA Ames (1969). Used in Space Shuttle simulations.",
            "labels": ["feat", "priority/high", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement Beam-Warming scheme (#B9)",
            "body": "## Task Description\nImplement Beam-Warming one-sided backward difference scheme.\n\n## Spatial Discretization\ndF/dx ≈ (3F_i - 4F_{i-1} + F_{i-2}) / (2dx)\n\n## Properties\n- 2nd order accuracy\n- Downwind bias (uses i, i-1, i-2)\n- More restrictive CFL than centered schemes\n- Good introduction to implicit methods concept",
            "labels": ["feat", "priority/medium", "module/core"],
            "assignees": ["BE"]
        },
        {
            "title": "feat(core): Implement Fromm scheme (#B10)",
            "body": "## Task Description\nImplement Fromm's averaged scheme (Upwind + Lax-Wendroff).\n\n## Formula\nU_Fromm = 0.5*(U_Upwind + U_LW)\n\n## Trade-offs\n- Reduced oscillations vs pure LW\n- Reduced diffusion vs pure upwind\n- Good balance for general use\n- Precedes modern flux limiters",
            "labels": ["feat", "priority/medium", "module/core"],
            "assignees": ["BE"]
        },
        
        # Batch C: Frontend UI (@FE)
        {
            "title": "feat(ui): Create Streamlit main application entry point (#C1)",
            "body": "## Task Description\nCreate Streamlit app with multi-page structure.\n\n## Pages\n- streamlit_app.py (Main dashboard)\n- pages/1_Simulation.py\n- pages/2_Comparison.py\n- pages/3_Theory.py\n\n## Layout\n- Header with project info\n- Navigation cards\n- Metrics overview\n- About section",
            "labels": ["feat", "priority/critical", "module/ui"],
            "assignees": ["FE"]
        },
        {
            "title": "feat(ui): Build parameter input panel component (#C2)",
            "body": "## Task Description\nBuild reusable parameter input panel.\n\n## Sections\n1. Domain Settings (L, nx, x_dam)\n2. Initial Conditions (h_L, h_R, u_L, u_R)\n3. Numerical Parameters (g, cfl, t_end)\n4. Scheme Selection (multi-select with metadata)\n\n## Features\n- Validation with inline errors\n- Tooltips on hover\n- Smart defaults\n- Preset configurations",
            "labels": ["feat", "priority/critical", "module/ui"],
            "assignees": ["FE"]
        },
        {
            "title": "feat(ui): Implement visualization and animation system (#C3)",
            "body": "## Task Description\nCreate visualization system for simulation results.\n\n## Components\n- Height profile plot (with fill)\n- Velocity profile plot\n- Animation system (matplotlib FuncAnimation)\n- Streamlit integration (time slider, playback controls)\n\n## Export\n- PNG/SVG export\n- CSV data export\n- Comparison overlay mode",
            "labels": ["feat", "priority/critical", "module/ui"],
            "assignees": ["FE"]
        },
        {
            "title": "feat(ui): Build scheme comparison dashboard (#C4)",
            "body": "## Task Description\nBuild dedicated comparison dashboard page.\n\n## Layout\nSidebar: Parameters + Scheme selection\nMain area:\n- Control bar (play/pause/speed)\n- Height profile comparison (overlaid)\n- Velocity profile comparison\n- Metrics table (error, CPU time, mass conservation)\n- Performance bar chart\n\n## Features\n- Multi-scheme overlay (2-6 schemes)\n- Synchronized time slider\n- Auto-computed metrics",
            "labels": ["feat", "priority/high", "module/ui"],
            "assignees": ["FE"]
        },
        
        # Batch D: Testing (@QA)
        {
            "title": "test(qa): Set up pytest framework and CI integration (#D1)",
            "body": "## Task Description\nSet up pytest framework with CI/CD.\n\n## Structure\ntests/\n├── conftest.py (fixtures)\n├── unit/ (unit tests)\n├── integration/ (integration tests)\n└── performance/ (benchmarks)\n\n## Configuration\n- pytest.ini with coverage settings\n- .github/workflows/ci.yml\n- Target: ≥80% coverage\n\n## Fixtures\ndefault_config, fine_config, dry_bed_config, classic_dambreak",
            "labels": ["test", "priority/critical", "module/tests"],
            "assignees": ["QA"]
        },
        {
            "title": "test(qa): Write core engine unit tests (#D2)",
            "body": "## Task Description\nWrite unit tests for B1-B10 modules.\n\n## Coverage Targets\n- B1 Config: ≥90% (15 tests)\n- B2 Exact Riemann: ≥85% (20 tests)\n- B3 HLL Solver: ≥85% (15 tests)\n- B4-B10 Schemes: ≥85-90% each\n\n## Test Categories\n- Validation logic\n- Property calculations\n- Core algorithms\n- Edge cases\n- Physical validity",
            "labels": ["test", "priority/high", "module/tests"],
            "assignees": ["QA"]
        },
        {
            "title": "test(qa): Create integration and regression tests (#D3)",
            "body": "## Task Description\nCreate integration and regression test suites.\n\n## Integration Tests\n- Full pipeline execution\n- Multi-scheme comparison\n- Parameter variation\n- Edge cases (dry bed, extreme params)\n\n## Regression Tests\n- Reference solutions for all 6 schemes\n- Detect unintended changes\n- scripts/generate_reference_data.py\n- Weekly CI schedule",
            "labels": ["test", "priority/medium", "module/tests"],
            "assignees": ["QA"]
        },
        
        # Batch E: Documentation (@TW)
        {
            "title": "docs(tw): Complete SRS Software Requirements Specification (#E1)",
            "body": "## Task Description\nComplete SRS document following GB/T 9385-2008 standard.\n\n## Sections\n1. Introduction (purpose, scope, definitions)\n2. Overall description (product perspective, functions)\n3. Specific requirements (functional, non-functional)\n4. External interfaces\n5. Other requirements (performance, design constraints)\n\n## Standard Compliance\nGB/T 9385-2008 structure and terminology",
            "labels": ["docs", "priority/high", "module/docs"],
            "assignees": ["TW"]
        },
        {
            "title": "docs(tw): Complete SDD Software Design Document (#E2)",
            "body": "## Task Description\nComplete Software Design Document (SDD).\n\n## Sections\n1. Introduction\n2. System architecture\n3. Detailed design (config, riemann, schemes, UI)\n4. Data structures\n5. Algorithms (pseudocode)\n6. Interface specifications\n7. Test strategy\n\n## Diagrams\n- Class hierarchy\n- Data flow\n- Component interaction",
            "labels": ["docs", "priority/high", "module/docs"],
            "assignees": ["TW"]
        },
        {
            "title": "docs(tw): Create user manual and theory guide (#E3)",
            "body": "## Task Description\nCreate user-facing documentation.\n\n## User Manual\n- Installation guide\n- Quick start tutorial\n- Feature reference\n- Troubleshooting\n- FAQ\n\n## Theory Guide\n- Shallow water equations derivation\n- Riemann problem explanation\n- Each scheme: math + properties + when to use\n- Numerical analysis concepts (CFL, convergence, TVD)\n- Comparison tables and recommendations",
            "labels": ["docs", "priority/medium", "module/docs"],
            "assignees": ["TW"]
        }
    ]
    
    # Create issues
    created = 0
    failed = 0
    
    for idx, issue in enumerate(issues, 1):
        print(f"\n[{idx}/{len(issues)}] Creating: {issue['title'][:50]}...")
        
        success, num, url = create_issue(
            issue['title'],
            issue['body'],
            issue['labels'],
            issue['assignees']
        )
        
        if success:
            print(f"  [OK] Created #{num}")
            created += 1
        else:
            print(f"  [FAIL] Error: {str(url)[:100]}")
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print(f"  COMPLETE: {created}/{len(issues)} issues created successfully")
    print(f"  FAILED: {failed} issues")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()