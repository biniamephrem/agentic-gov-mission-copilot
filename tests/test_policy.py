from app.services.policy import requires_human_approval


def test_high_impact_resource_allocation_requires_approval():
    assert requires_human_approval("request_resource_allocation", {"resource": "mobile communications unit"})
