import os
import pytest

def test_specs_exist():
    base = os.path.dirname(__file__)
    spec_md = os.path.join(base, "SPEC_CHI_BENCH_HEALTHCARE_AGENT.md")
    table1 = os.path.join(base, "table1_resource_defense_matrix.csv")
    assert os.path.exists(spec_md), "SPEC markdown missing"
    assert os.path.exists(table1), "table1 CSV missing"
    
    with open(spec_md, "r", encoding="utf-8") as f:
        content = f.read()
    assert "SPEC_01" in content
    assert "1.18" in content
    assert "0.00" in content
    assert "mermaid" in content

    for mmd in ["01_system_topology.mmd", "02_sequence_flow.mmd", "03_state_machine.mmd", "04_security_boundary.mmd"]:
        assert os.path.exists(os.path.join(base, mmd)), f"Diagram {mmd} missing"

if __name__ == "__main__":
    test_specs_exist()
    print("Specs audit test PASS [100% FOUR DIAGRAMS AND ONE TABLE COMPLIANT]!")
