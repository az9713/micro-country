"""
Deployer Specialist - Operations Ministry

Responsible for deployment and release management.
"""

from dataclasses import dataclass, field
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class DeploymentPlan:
    """A deployment plan."""

    service: str
    environment: str
    version: str
    strategy: str
    steps: list[str] = field(default_factory=list)
    rollback_steps: list[str] = field(default_factory=list)
    health_checks: list[str] = field(default_factory=list)


class DeployerSpecialist:
    """
    The Deployer Specialist manages deployments safely.

    Capabilities:
    - Plan deployments
    - Execute with verification
    - Rollback on failure
    - Monitor health
    """

    DEPLOYMENT_STRATEGIES = {
        "rolling": {
            "description": "Update instances one at a time",
            "risk": "low",
            "downtime": "minimal",
        },
        "blue-green": {
            "description": "Switch traffic between two environments",
            "risk": "low",
            "downtime": "zero",
        },
        "canary": {
            "description": "Gradual rollout to subset of users",
            "risk": "very low",
            "downtime": "zero",
        },
    }

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "deployer"

    def get_system_prompt(self) -> str:
        """Get the deployer specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def create_deployment_plan(
        self,
        service: str,
        environment: str,
        version: str = "latest",
        strategy: str = "rolling",
    ) -> DeploymentPlan:
        """Create a deployment plan."""
        steps = [
            "Verify pre-deployment checks",
            "Create deployment snapshot",
            f"Deploy using {strategy} strategy",
            "Run health checks",
            "Monitor metrics for 5 minutes",
            "Mark deployment complete",
        ]

        rollback_steps = [
            "Identify rollback trigger",
            "Switch to previous version",
            "Verify rollback success",
            "Investigate failure cause",
        ]

        health_checks = [
            "Service responds to /health",
            "Error rate below threshold",
            "Latency within SLA",
        ]

        return DeploymentPlan(
            service=service,
            environment=environment,
            version=version,
            strategy=strategy,
            steps=steps,
            rollback_steps=rollback_steps,
            health_checks=health_checks,
        )


def create_specialist() -> DeployerSpecialist:
    """Factory function to create the specialist."""
    return DeployerSpecialist()
