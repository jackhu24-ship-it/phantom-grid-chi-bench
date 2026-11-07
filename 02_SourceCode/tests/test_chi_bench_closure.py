import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from chi_bench_healthcare_agent_core import (
    HealthcareAnomalyDetector,
    MCPHealthcareToolGateway,
    SafetyAndZDRPurge,
    SovereignHealthcareAgent
)

def test_anomaly_detector_latency():
    det = HealthcareAnomalyDetector()
    res = det.detect_anomalies({"heart_rate": 140.0, "spo2": 88.0, "systolic_bp": 195.0})
    assert res["is_anomaly"] is True
    assert len(res["anomaly_flags"]) == 3
    assert res["latency_us"] <= 100.0  # Safe buffer in test container
    print(f"Anomaly detector latency: {res['latency_us']} us")

def test_mcp_tool_gateway():
    gw = MCPHealthcareToolGateway()
    res = gw.call_tool("test_prior_auth", {"patient_id": "123"})
    assert res["status"] == "SUCCESS"
    assert "coverage_status" in res
    assert len(gw.invocations) == 1

def test_full_agent_workflow_closure():
    agent = SovereignHealthcareAgent()
    pa = agent.run_prior_authorization_workflow({"cpt_code": "93458"})
    assert pa["terminal_state"] == "AUTHORIZED"
    assert pa["policy_compliant"] is True
    
    um = agent.run_utilization_management_workflow({"case_id": "UM-01"})
    assert um["terminal_state"] == "DETERMINATION_ISSUED"
    
    care = agent.run_care_management_workflow({"patient_id": "P-01"})
    assert care["terminal_state"] == "CARE_PLAN_ACTIVATED"
    
    residue = agent.close_and_purge()
    assert residue == 0.000000

if __name__ == "__main__":
    test_anomaly_detector_latency()
    test_mcp_tool_gateway()
    test_full_agent_workflow_closure()
    print("All CHI-Bench closure tests PASS!")
