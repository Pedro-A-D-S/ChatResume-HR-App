# Enterprise Multi-Agent HR Platform (LLMOps & ASVS)

[![CI & Security](https://img.shields.io/badge/CI%2FCD-OIDC%20Secured-brightgreen)](.github/workflows/Deployment.yaml)
[![OWASP ASVS](https://img.shields.io/badge/OWASP-ASVS%20v4.0%20%7C%20LLM%20Top%2010-blue)](docs/security/OWASP_GOVERNANCE.md)
[![Memory Architecture](https://img.shields.io/badge/Agent%20Memory-5--Layer%20CoALA%20%26%20Mem0-9cf)](docs/security/OWASP_GOVERNANCE.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, banking-compliant (**Itaú Unibanco & NTT DATA** standard) Multi-Agent HR candidate evaluation platform built under **Clean Architecture & Domain-Driven Design (DDD)**.

The system replaces legacy monolithic scripts and unsafe `pickle` vector stores with a hardened multi-agent workflow featuring **5-Layer Cognitive Memory**, **LLM-as-a-Judge automated audit gates**, and **OWASP LLM01 / LLM06 / ASVS** sanitizers.

---

## 🏛️ Architecture Overview

```
[Candidate PDF / Resume]
           │
           ▼
┌───────────────────────────────────────┐
│ 1. Parser & PII Redactor Agent        │  <-- Strips CPFs, emails, phones (LGPD/GDPR)
│    + Prompt Injection Guard           │  <-- Defends against indirect white-text jailbreaks
└──────────────────┬────────────────────┘
                   │ Anonymized & Sanitized Text
                   ▼
┌───────────────────────────────────────┐
│ 2. Technical Evaluator Agent          │  <-- Matches competencies against Job Rubrics
└──────────────────┬────────────────────┘
                   │ Draft Verdict & Matched Competencies
                   ▼
┌───────────────────────────────────────┐
│ 3. LLM-as-a-Judge Audit Agent         │  <-- Verifies hallucination, evidence grounding & bias
└──────────────────┬────────────────────┘
                   │ Verified Output
                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 4. 5-Layer Cognitive Memory Architecture (CoALA / Mem0 pattern)       │
│    • Layer 1 (Working): 85% budget token overflow management           │
│    • Layer 2 (Episodic): Immutable JSONL audit trail                   │
│    • Layer 3 (Semantic): SQLite Knowledge Graph + Schema Validation     │
│    • Layer 4 (Procedural): Versioned YAML Screening Skills             │
│    • Layer 5 (Forgetting Engine): Automated LGPD 30-day TTL cleanup    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔒 Security & Compliance Guardrails

- **Zero Arbitrary Deserialization**: Completely removed unsafe Python `pickle.load()` vectors; all durable storage uses structured SQLite and immutable JSONL.
- **OWASP LLM01 (Prompt Injection)**: Pre-ingestion sanitizer intercepts adversarial inputs (e.g. invisible instructions demanding 100% fit scores) and rejects execution with an audit flag.
- **OWASP LLM02 / LLM06 (PII & Excessive Agency)**: Redacts tax IDs (CPF/SSN), contact coordinates, and demographic markers before inference. No candidate rejection/approval is presented without dual-agent consensus.
- **Docker Hardening**: Multi-stage, non-root execution container (`USER appuser`) with pinned base images.

---

## 🚀 Quickstart & Verification

Run the test suite and CLI platform locally without external cloud dependencies:

```bash
# Set up environment
export PYTHONPATH=src

# Run automated unit and security tests
python -m pytest tests/ -v

# Run the CLI multi-agent platform simulation
python -m hr_agent_platform.presentation.cli_app
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for details.
