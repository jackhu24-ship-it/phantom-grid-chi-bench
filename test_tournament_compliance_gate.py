import os
from pathlib import Path
import sys
import json
import yaml
import pytest

base_dir = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.join(base_dir, "02_SourceCode"))
from chi_bench_healthcare_agent_core import SovereignHealthcareAgent, HealthcareAnomalyDetector

def test_manifest_validity():
    manifest_path = os.path.join(base_dir, "match_manifest.yaml")
    assert os.path.exists(manifest_path), "match_manifest.yaml missing"
    with open(manifest_path, "r", encoding="utf-8") as f:
        mf = yaml.safe_load(f)
    assert mf["tournament_id"] == "202611_IEEE_BigData_CHI_Bench"
    assert "CHI-Bench" in mf["title"]

def test_10_drawers_exist():
    drawers = [
        "01_Specs", "02_SourceCode", "03_CoverImage_16x9", "04_Slides_PDF",
        "05_DemoVideo_1440P", "06_Notebooks_and_Models", "07_SubmissionPackage",
        "08_AuditReceipts", "09_ChaosReports", "10_Releases"
    ]
    for d in drawers:
        p = os.path.join(base_dir, d)
        assert os.path.exists(p) and os.path.isdir(p), f"Drawer {d} missing"

def test_specs_first_compliance():
    spec_path = os.path.join(base_dir, "01_Specs", "SPEC_CHI_BENCH_HEALTHCARE_AGENT.md")
    assert os.path.exists(spec_path)
    with open(spec_path, "r", encoding="utf-8") as f:
        text = f.read()
    assert "SPEC-CHI-BENCH-01" in text
    assert "1.18" in text

def test_agent_execution_and_safety_closure():
    agent = SovereignHealthcareAgent()
    pa = agent.run_prior_authorization_workflow({"cpt_code": "93458"})
    assert pa["terminal_state"] == "AUTHORIZED"
    
    um = agent.run_utilization_management_workflow({"case_id": "UM-100"})
    assert um["terminal_state"] == "DETERMINATION_ISSUED"
    
    care = agent.run_care_management_workflow({"patient_id": "P-99"})
    assert care["terminal_state"] == "CARE_PLAN_ACTIVATED"
    
    residue = agent.close_and_purge()
    assert residue == 0.000000

def test_submission_package_zero_cjk():
    sub_path = os.path.join(base_dir, "07_SubmissionPackage", "Official_Submission_Copy_Package.md")
    assert os.path.exists(sub_path)
    with open(sub_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Check for CJK characters
    import re
    cjk = re.findall(r'[\u4e00-\u9fff]', text)
    assert len(cjk) == 0, f"Found {len(cjk)} CJK characters in submission package"

if __name__ == "__main__":
    test_manifest_validity()
    test_10_drawers_exist()
    test_specs_first_compliance()
    test_agent_execution_and_safety_closure()
    test_submission_package_zero_cjk()
    print("ALL TOURNAMENT COMPLIANCE TESTS PASS [100% GREEN]!")