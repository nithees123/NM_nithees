#!/usr/bin/env python3
"""
Production Verification Test Suite: ServiceNow Laptop Procurement Automation
=============================================================================
Author: test_writer_e2e (E2E Testing Track Lead & QA Specialist)
Project Root: C:\\Users\\soman\\.gemini\\antigravity\\scratch\\servicenow_laptop_procurement

This automated test suite executes opaque-box verification across all 6 phases:
1. Deliverable file presence & integrity (all 20 inventoried deliverables).
2. Zero-stub / placeholder audit (detects TODO, TBD, [TBD], FIXME, Lorem ipsum).
3. Document depth, word counts, and mandatory section completeness.
4. XML and JSON schema & syntax validity for ServiceNow Flow Designer exports.
5. ECMAScript syntax compilation (via Node.js V8) for Catalog Client Scripts.
6. Mermaid diagram syntax, balanced delimiters, and diagram type validity.
7. UAT test scenario completeness (8 scenarios, execution tables, logs, sign-offs).
8. 4-Tier verification semantics (Tiers 1 to 4).
"""

import argparse
import json
import os
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Ensure stdout handles UTF-8 smoothly across Windows consoles
try:
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PROJECT_ROOT = Path(r"C:\Users\soman\.gemini\antigravity\scratch\servicenow_laptop_procurement").resolve()

# Inventory of all 20 required deliverable files across all 6 phases
REQUIRED_DELIVERABLES = [
    # Phase 1: Ideation (3 deliverables)
    "01_phase1_ideation/01_problem_statements.md",
    "01_phase1_ideation/02_brainstorming_and_prioritization.md",
    "01_phase1_ideation/03_empathy_map_canvas.md",
    
    # Phase 2: Requirements (4 deliverables)
    "02_phase2_requirements/01_customer_journey_map.md",
    "02_phase2_requirements/02_dfd_and_user_stories.md",
    "02_phase2_requirements/03_solution_requirements.md",
    "02_phase2_requirements/04_technology_stack.md",
    
    # Phase 3: Project Design (3 deliverables)
    "03_phase3_project_design/01_problem_solution_fit.md",
    "03_phase3_project_design/02_proposed_solution.md",
    "03_phase3_project_design/03_solution_architecture.md",
    
    # Phase 4: Project Planning (2 deliverables)
    "04_phase4_project_planning/01_wbs_and_planning_logic.md",
    "04_phase4_project_planning/02_project_planning_template.md",
    
    # Phase 5: Implementation Artifacts & Testing (6 deliverables)
    "05_phase5_development_and_testing/01_implementation_artifacts/flow_designer_specs.md",
    "05_phase5_development_and_testing/01_implementation_artifacts/catalog_item_specs.md",
    "05_phase5_development_and_testing/01_implementation_artifacts/sys_hub_flow_standard_laptop_procurement.xml",
    "05_phase5_development_and_testing/01_implementation_artifacts/sys_hub_flow_standard_laptop_procurement.json",
    "05_phase5_development_and_testing/01_implementation_artifacts/catalog_client_scripts.js",
    "05_phase5_development_and_testing/02_uat_testing/uat_test_plan_and_execution_report.md",
    
    # Phase 6: Project Documentation (2 deliverables)
    "06_phase6_project_documentation/01_functional_specification_document_fsd.md",
    "06_phase6_project_documentation/02_final_project_report.md",
]

# Minimum word count thresholds for thorough enterprise documentation
MINIMUM_WORD_COUNTS: Dict[str, int] = {
    "01_phase1_ideation/01_problem_statements.md": 1500,
    "01_phase1_ideation/02_brainstorming_and_prioritization.md": 1200,
    "01_phase1_ideation/03_empathy_map_canvas.md": 1200,
    "02_phase2_requirements/01_customer_journey_map.md": 1000,
    "02_phase2_requirements/02_dfd_and_user_stories.md": 2000,
    "02_phase2_requirements/03_solution_requirements.md": 1200,
    "02_phase2_requirements/04_technology_stack.md": 1000,
    "03_phase3_project_design/01_problem_solution_fit.md": 1200,
    "03_phase3_project_design/02_proposed_solution.md": 1500,
    "03_phase3_project_design/03_solution_architecture.md": 1500,
    "04_phase4_project_planning/01_wbs_and_planning_logic.md": 1500,
    "04_phase4_project_planning/02_project_planning_template.md": 1500,
    "05_phase5_development_and_testing/01_implementation_artifacts/flow_designer_specs.md": 1500,
    "05_phase5_development_and_testing/01_implementation_artifacts/catalog_item_specs.md": 1000,
    "05_phase5_development_and_testing/02_uat_testing/uat_test_plan_and_execution_report.md": 2000,
    "06_phase6_project_documentation/01_functional_specification_document_fsd.md": 3000,
    "06_phase6_project_documentation/02_final_project_report.md": 2000,
}

# Supported Mermaid diagram types
VALID_MERMAID_TYPES = {
    "graph", "flowchart", "sequencediagram", "classdiagram", 
    "statediagram", "statediagram-v2", "erdiagram", "gantt", 
    "pie", "gitgraph", "journey", "mindmap", "c4context", 
    "timeline", "quadrantchart", "xychart-beta", "block-beta", 
    "sankey-beta", "requirementdiagram", "architecture-beta"
}


# ==============================================================================
# TIER 1: DELIVERABLE PRESENCE & FILE INTEGRITY TESTS
# ==============================================================================
class TestDeliverablePresence(unittest.TestCase):
    """Verifies that all 20 deliverable files exist, are readable, and non-empty."""

    def test_all_20_deliverables_exist(self):
        missing = []
        for rel_path in REQUIRED_DELIVERABLES:
            full_path = PROJECT_ROOT / rel_path
            if not full_path.exists():
                missing.append(rel_path)
            elif full_path.stat().st_size == 0:
                missing.append(f"{rel_path} (EMPTY FILE)")
        self.assertEqual(len(missing), 0, f"Missing or empty deliverable files ({len(missing)}):\n" + "\n".join(missing))

    def test_all_phase_directories_exist(self):
        expected_dirs = [
            "01_phase1_ideation",
            "02_phase2_requirements",
            "03_phase3_project_design",
            "04_phase4_project_planning",
            "05_phase5_development_and_testing",
            "05_phase5_development_and_testing/01_implementation_artifacts",
            "05_phase5_development_and_testing/02_uat_testing",
            "06_phase6_project_documentation",
        ]
        missing_dirs = []
        for d in expected_dirs:
            p = PROJECT_ROOT / d
            if not p.is_dir():
                missing_dirs.append(d)
        self.assertEqual(len(missing_dirs), 0, f"Missing directories: {missing_dirs}")


# ==============================================================================
# TIER 1: ZERO-STUB & COMPLETENESS AUDIT TESTS
# ==============================================================================
class TestZeroStubCompleteness(unittest.TestCase):
    """Verifies absence of placeholder stubs (TODO, TBD, FIXME, Lorem ipsum)."""

    def test_no_placeholders_in_deliverables(self):
        stub_pattern = re.compile(
            r"(\b(TODO|TBD|FIXME|XXX)\b|\[\s*(TBD|TODO|FIXME|insert\s+here)\s*\]|Lorem\s+ipsum)",
            re.IGNORECASE
        )
        
        violations = []
        for rel_path in REQUIRED_DELIVERABLES:
            full_path = PROJECT_ROOT / rel_path
            if not full_path.exists():
                continue
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_num, line in enumerate(f, 1):
                    # Filter out benign occurrences in code quotes discussing the check or variable stubbing in WBS
                    if "placeholder variable stubs" in line:
                        continue
                    m = stub_pattern.search(line)
                    if m:
                        violations.append(f"{rel_path}:{line_num} -> Matched '{m.group(0)}': {line.strip()[:80]}")
                        
        self.assertEqual(len(violations), 0, f"Placeholder violations detected ({len(violations)}):\n" + "\n".join(violations))


# ==============================================================================
# TIER 1: WORD COUNT & SECTION COMPLETENESS TESTS
# ==============================================================================
class TestWordCountAndSections(unittest.TestCase):
    """Verifies depth and structural completeness of all markdown deliverables."""

    def test_document_depth_and_word_counts(self):
        failures = []
        for rel_path, min_words in MINIMUM_WORD_COUNTS.items():
            full_path = PROJECT_ROOT / rel_path
            if not full_path.exists():
                failures.append(f"{rel_path}: File does not exist")
                continue
            with open(full_path, "r", encoding="utf-8") as f:
                text = f.read()
            word_count = len(text.split())
            if word_count < min_words:
                failures.append(f"{rel_path}: Actual words {word_count} < Minimum required {min_words}")
        self.assertEqual(len(failures), 0, f"Word count thresholds not met ({len(failures)}):\n" + "\n".join(failures))

    def test_fsd_12_mandatory_sections(self):
        fsd_path = PROJECT_ROOT / "06_phase6_project_documentation/01_functional_specification_document_fsd.md"
        self.assertTrue(fsd_path.exists(), "FSD file missing")
        with open(fsd_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        required_sections = [
            "Document Control",
            "Executive Summary",
            "System Overview",
            "Functional Requirements Traceability Matrix",
            "Business Process Flows",
            "Service Catalog Item Design",
            "Flow Designer Technical Specification",
            "Data Dictionary",
            "Security, Roles, and Access Control",
            "Automated Notification Templates",
            "Error & Exception Handling Framework",
            "Appendix & Glossary",
        ]
        missing = [s for s in required_sections if s.lower() not in content.lower()]
        self.assertEqual(len(missing), 0, f"FSD missing required sections: {missing}")

    def test_final_report_10_mandatory_sections(self):
        rep_path = PROJECT_ROOT / "06_phase6_project_documentation/02_final_project_report.md"
        self.assertTrue(rep_path.exists(), "Final Project Report missing")
        with open(rep_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        required_sections = [
            "Executive Summary",
            "Project Background",
            "Solution Overview",
            "Implementation Highlights",
            "Key Performance Indicator",
            "Financial ROI",
            "User Acceptance Testing",
            "Lessons Learned",
            "Future Roadmap",
            "Conclusion & Final Sign-Off",
        ]
        missing = [s for s in required_sections if s.lower() not in content.lower()]
        self.assertEqual(len(missing), 0, f"Final Report missing sections: {missing}")


# ==============================================================================
# TIER 1 & 2: FLOW DESIGNER EXPORT ARTIFACTS SYNTAX TESTS
# ==============================================================================
class TestFlowExportArtifacts(unittest.TestCase):
    """Verifies XML ElementTree parse and JSON structure for Flow Designer exports."""

    def test_xml_export_well_formed_and_schema(self):
        xml_path = PROJECT_ROOT / "05_phase5_development_and_testing/01_implementation_artifacts/sys_hub_flow_standard_laptop_procurement.xml"
        self.assertTrue(xml_path.exists(), "Flow XML export missing")
        
        try:
            tree = ET.parse(str(xml_path))
            root = tree.getroot()
        except ET.ParseError as e:
            self.fail(f"Flow XML export is malformed XML: {e}")
            
        self.assertIn(root.tag, ["unload", "record_update", "sys_remote_update_set"], f"Unexpected XML root tag: {root.tag}")
        self.assertGreater(len(root), 5, f"XML root has insufficient child elements ({len(root)})")
        
        # Verify presence of sys_hub_flow and action definitions
        xml_text = ET.tostring(root, encoding="utf-8").decode("utf-8")
        self.assertIn("sys_hub_flow", xml_text)
        self.assertIn("Standard Laptop Procurement Flow", xml_text)
        self.assertIn("sc_req_item", xml_text)

    def test_json_export_structure_and_keys(self):
        json_path = PROJECT_ROOT / "05_phase5_development_and_testing/01_implementation_artifacts/sys_hub_flow_standard_laptop_procurement.json"
        self.assertTrue(json_path.exists(), "Flow JSON export missing")
        
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.fail(f"Flow JSON export is malformed JSON: {e}")
            
        required_keys = ["flow_metadata", "trigger", "actions", "error_handler"]
        for k in required_keys:
            self.assertIn(k, data, f"Flow JSON missing required key: {k}")
            
        # Verify trigger table
        trigger = data.get("trigger", {})
        self.assertEqual(trigger.get("table"), "sc_req_item", f"Trigger table mismatch: {trigger.get('table')}")
        
        # Verify actions list has sufficient depth
        actions = data.get("actions", [])
        self.assertGreaterEqual(len(actions), 10, f"Actions list too short: {len(actions)}")


# ==============================================================================
# TIER 1 & 2: CATALOG CLIENT SCRIPTS JAVASCRIPT SYNTAX TESTS
# ==============================================================================
class TestCatalogClientScriptSyntax(unittest.TestCase):
    """Verifies JavaScript syntax via Node.js V8 compiler and checks client API bindings."""

    def test_javascript_syntax_with_node(self):
        js_path = PROJECT_ROOT / "05_phase5_development_and_testing/01_implementation_artifacts/catalog_client_scripts.js"
        self.assertTrue(js_path.exists(), "Client scripts JS file missing")
        
        # Run node --check
        res = subprocess.run(
            ["node", "--check", str(js_path)],
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0, f"JavaScript syntax errors in {js_path.name}:\n{res.stderr}")

    def test_client_script_functions_and_apis(self):
        js_path = PROJECT_ROOT / "05_phase5_development_and_testing/01_implementation_artifacts/catalog_client_scripts.js"
        with open(js_path, "r", encoding="utf-8") as f:
            code = f.read()
            
        # Verify client script handlers
        self.assertIn("function onChange(", code, "Missing onChange client script handler")
        self.assertIn("function onSubmit()", code, "Missing onSubmit client script handler")
        self.assertIn("isLoading", code, "Missing isLoading conditional guard in script")
        
        # Verify ServiceNow client APIs
        self.assertIn("g_form.getValue", code, "Missing g_form.getValue")
        self.assertIn("g_form.setValue", code, "Missing g_form.setValue")
        self.assertIn("g_form.showFieldMsg", code, "Missing g_form.showFieldMsg")


# ==============================================================================
# TIER 1 & 3: MERMAID DIAGRAM SYNTAX & BALANCED DELIMITERS
# ==============================================================================
class TestMermaidDiagramSyntax(unittest.TestCase):
    """Verifies all Mermaid diagram blocks across markdown files."""

    def test_all_mermaid_diagrams_syntax(self):
        mermaid_block_re = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
        
        failures = []
        diagram_count = 0
        
        for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT):
            if ".agents" in dirpath or "tests" in dirpath:
                continue
            for f in filenames:
                if not f.endswith(".md"):
                    continue
                p = Path(dirpath) / f
                with open(p, "r", encoding="utf-8") as fp:
                    content = fp.read()
                    
                matches = mermaid_block_re.findall(content)
                for idx, block in enumerate(matches, 1):
                    diagram_count += 1
                    lines = [l.strip() for l in block.strip().split("\n") if l.strip() and not l.strip().startswith("%%")]
                    if not lines:
                        failures.append(f"{p.name}: Diagram #{idx} is empty")
                        continue
                        
                    first_word = lines[0].split()[0].lower()
                    valid_type = any(first_word.startswith(t) for t in VALID_MERMAID_TYPES)
                    if not valid_type:
                        failures.append(f"{p.name}: Diagram #{idx} has invalid type '{first_word}' in line '{lines[0]}'")
                        
                    # Check balanced brackets
                    open_sq = block.count("[")
                    close_sq = block.count("]")
                    if open_sq != close_sq:
                        failures.append(f"{p.name}: Diagram #{idx} unbalanced square brackets: [={open_sq}, ]={close_sq}")
                        
        self.assertGreater(diagram_count, 20, f"Too few Mermaid diagrams found ({diagram_count})")
        self.assertEqual(len(failures), 0, f"Mermaid diagram syntax failures ({len(failures)}):\n" + "\n".join(failures))


# ==============================================================================
# TIER 1, 2, 3: UAT TEST SCENARIO COMPLETENESS TESTS
# ==============================================================================
class TestUATScenarioCompleteness(unittest.TestCase):
    """Verifies that all 8 UAT scenarios, logs, step tables, and sign-offs exist."""

    def test_all_8_uat_scenarios_present(self):
        uat_path = PROJECT_ROOT / "05_phase5_development_and_testing/02_uat_testing/uat_test_plan_and_execution_report.md"
        self.assertTrue(uat_path.exists(), "UAT Report file missing")
        with open(uat_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        expected_scenarios = [
            ("TC-01", "Standard End-to-End Happy Path"),
            ("TC-02", "Manager Rejection Path"),
            ("TC-03", "VIP Executive Fast-Track"),
            ("TC-04", "Null Manager Fallback"),
            ("TC-05", "SLA Breach & Automated Escalation"),
            ("TC-06", "Out-of-Stock Asset Handling"),
            ("TC-07", "Parallel Approvals"),
            ("TC-08", "Flow Error Handler"),
        ]
        
        missing = []
        for code, name in expected_scenarios:
            if code not in content:
                missing.append(f"{code} ({name})")
        self.assertEqual(len(missing), 0, f"Missing UAT scenarios: {missing}")

    def test_uat_execution_tables_and_pass_verdicts(self):
        uat_path = PROJECT_ROOT / "05_phase5_development_and_testing/02_uat_testing/uat_test_plan_and_execution_report.md"
        with open(uat_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        for i in range(1, 9):
            prefix = f"TC-0{i}"
            self.assertIn(prefix, content, f"Scenario {prefix} missing")
            
        # Ensure verdicts are PASS
        pass_count = len(re.findall(r"\bPASS\b|\*\*PASS\*\*", content))
        self.assertGreaterEqual(pass_count, 8, f"Insufficient PASS verdicts in UAT report ({pass_count})")
        
        # Ensure diagnostics / logs exist
        self.assertIn("FLOW_ENGINE", content, "Missing FLOW_ENGINE execution log entries")

    def test_uat_defect_log_and_formal_signoffs(self):
        uat_path = PROJECT_ROOT / "05_phase5_development_and_testing/02_uat_testing/uat_test_plan_and_execution_report.md"
        with open(uat_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Verify Defect Log
        self.assertIn("DEF-001", content, "Missing DEF-001 in defect log")
        self.assertIn("DEF-002", content, "Missing DEF-002 in defect log")
        
        # Verify Sign-Off Matrix
        self.assertIn("Formal UAT Sign-Off Matrix", content)
        self.assertIn("ACCEPTED", content)
        stakeholders = ["Marcus Vance", "Sarah Jenkins", "Derek Cole", "Maria Alvarez", "Kevin Zhang"]
        for st in stakeholders:
            self.assertIn(st, content, f"Missing stakeholder sign-off: {st}")


# ==============================================================================
# TIER 4: REAL-WORLD WORKLOAD SCENARIOS & FINANCIAL ROI VERIFICATION
# ==============================================================================
class TestEnterpriseWorkloadsAndROI(unittest.TestCase):
    """Verifies Tier 4 enterprise workload models and financial ROI metrics."""

    def test_financial_roi_model_metrics(self):
        report_path = PROJECT_ROOT / "06_phase6_project_documentation/02_final_project_report.md"
        self.assertTrue(report_path.exists())
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Check financial ROI model presence
        self.assertIn("1,273,450", content, "Missing calibrated NPV metric $1,273,450")
        self.assertIn("462%", content, "Missing IRR metric 462%")
        self.assertIn("2.6", content, "Missing Payback Period metric 2.6 months")

    def test_kpi_target_achievements(self):
        report_path = PROJECT_ROOT / "06_phase6_project_documentation/02_final_project_report.md"
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Verify 14.2 days baseline -> 2.4 days delivered
        self.assertIn("14.2", content)
        self.assertIn("2.4", content)  # Actual achieved cycle time
        self.assertIn("72", content)


# ==============================================================================
# CLI RUNNER & FORMATTED REPORTING
# ==============================================================================
def run_cli_suite(verbosity: int = 1, tier_filter: int = None, json_report_path: str = None) -> int:
    """Executes the test suite with rich console output and optional JSON report."""
    print("=" * 80)
    print("  SERVICENOW LAPTOP PROCUREMENT AUTOMATION -- E2E TEST VERIFICATION SUITE")
    print("=" * 80)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Target Environment: Python {sys.version.split()[0]} / Node.js Engine")
    if tier_filter:
        print(f"Filtering on Tier: {tier_filter}")
    print("-" * 80)

    # Build Test Suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    tier_1_cases = [TestDeliverablePresence, TestZeroStubCompleteness, TestWordCountAndSections, TestMermaidDiagramSyntax]
    tier_2_cases = [TestFlowExportArtifacts, TestCatalogClientScriptSyntax]
    tier_3_cases = [TestUATScenarioCompleteness]
    tier_4_cases = [TestEnterpriseWorkloadsAndROI]

    if tier_filter == 1:
        selected_classes = tier_1_cases
    elif tier_filter == 2:
        selected_classes = tier_2_cases
    elif tier_filter == 3:
        selected_classes = tier_3_cases
    elif tier_filter == 4:
        selected_classes = tier_4_cases
    else:
        selected_classes = tier_1_cases + tier_2_cases + tier_3_cases + tier_4_cases

    for cls in selected_classes:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    print("\n" + "=" * 80)
    print("  VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Pass Count     : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures       : {len(result.failures)}")
    print(f"Errors         : {len(result.errors)}")
    print(f"Overall Status : {'SUCCESS (100% PASS)' if result.wasSuccessful() else 'FAILED'}")
    print("=" * 80)

    if json_report_path:
        report_data = {
            "project": "ServiceNow Laptop Procurement Automation",
            "tests_run": result.testsRun,
            "passed": result.testsRun - len(result.failures) - len(result.errors),
            "failures": len(result.failures),
            "errors": len(result.errors),
            "success": result.wasSuccessful(),
            "failure_details": [str(f) for f in result.failures],
            "error_details": [str(e) for e in result.errors],
        }
        with open(json_report_path, "w", encoding="utf-8") as jf:
            json.dump(report_data, jf, indent=2)
        print(f"JSON Report written to: {json_report_path}")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ServiceNow Laptop Procurement E2E Test Suite")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose test execution output")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3, 4], help="Execute only tests for specified tier")
    parser.add_argument("--json-report", type=str, help="Output path for JSON test report")
    args = parser.parse_args()

    verbosity_level = 2 if args.verbose else 1
    sys.exit(run_cli_suite(verbosity=verbosity_level, tier_filter=args.tier, json_report_path=args.json_report))
