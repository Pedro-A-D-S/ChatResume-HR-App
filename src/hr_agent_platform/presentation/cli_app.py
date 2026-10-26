"""CLI and presentation layer for HR Multi-Agent Platform."""

import sys
from pathlib import Path
from hr_agent_platform.domain.models import EvaluationRubric
from hr_agent_platform.infrastructure.memory.agent_memory import FiveLayerAgentMemory
from hr_agent_platform.application.orchestrator import MultiAgentHROrchestrator

def main():
    print("=" * 60)
    print("  Enterprise Multi-Agent HR Platform (LLMOps & ASVS)")
    print("=" * 60)

    memory_dir = Path("./data/memory")
    memory = FiveLayerAgentMemory(base_dir=memory_dir)
    orchestrator = MultiAgentHROrchestrator(memory)

    rubric = EvaluationRubric(
        role_title="Senior MLOps & LLMOps Engineer",
        seniority="Senior",
        required_skills=["AWS", "Terraform", "Docker", "MLflow", "Step Functions", "Batch", "Datadog"],
        nice_to_have_skills=["Kubernetes", "OpenSAMM"],
        min_years_experience=5
    )

    sample_resume = """
    Candidate: Alex Rivers
    Experience: 6 years in MLOps and Distributed Cloud Engineering.
    Skills: Proficient in AWS, Terraform, Docker, MLflow, Step Functions, Batch, and Datadog.
    Contact: alex.rivers@example.com | CPF: 000.111.222-33
    """

    print("\n[1/3] Parsing & Sanitizing Resume with Security Guardrails...")
    resume = orchestrator.parse_and_sanitize("cand-prod-01", sample_resume)
    print(f"  Sanitized Text:\n{resume.sanitized_text.strip()}")
    print(f"  PII Entities Redacted: {len(resume.detected_pii)}")
    print(f"  Adversarial Injection Detected: {resume.has_injection_risk}")

    print("\n[2/3] Executing Multi-Agent Evaluation & LLM-as-a-Judge Audit...")
    evaluation = orchestrator.evaluate_candidate(resume, rubric)
    print(f"  Candidate Fit Score: {evaluation.fit_score}%")
    print(f"  Matched Skills: {evaluation.matched_skills}")
    print(f"  Missing Skills: {evaluation.missing_skills}")
    print(f"  Judge Verdict: {evaluation.judge_verdict.verdict_summary}")

    print("\n[3/3] 5-Layer Cognitive Memory State:")
    episodes = memory.retrieve_recent_episodes(limit=1)
    facts = memory.query_facts("cand-prod-01")
    print(f"  Active Episodic Records: {len(episodes)}")
    print(f"  Durable Semantic Facts in SQLite: {len(facts)}")
    print("\n[DONE] Execution completed successfully under zero-cloud-cost simulation.")

if __name__ == "__main__":
    main()
