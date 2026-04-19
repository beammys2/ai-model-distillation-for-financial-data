# Audience Guide

The AI Model Distillation for Financial Data developer example is intended for quantitative researchers, AI developers, and enterprise data scientists. Through the flywheel we operate over a financial newsfeed dataset to generate features from unstructured data that can be used for alpha research and risk prediction. The result is a set of smaller, domain-specific, and task-optimized models that maintain high accuracy while reducing computational overhead and deployment costs. This example demonstrates how NVIDIA technology enables continuous model fine-tuning and distillation, enabling integration into financial workflows. 


> **📖 For complete implementation guide:** See [Data Logging for AI Apps](data-logging.md)

- **Implementation Approaches**:
  1. **Production (Recommended)**: Use continuous log exportation to Elasticsearch
  2. **Development/Demo**: Use provided JSONL sample data loader
  3. **Custom Integration**: Direct Elasticsearch integration with your application

> **📖 For data validation requirements:** See [Dataset Validation](dataset-validation.md)

- **Development Tools**: 
  - Use `./scripts/run-dev.sh` for development environment with Kibana (browse `log-store-*` index) and Flower for task monitoring
  - Query API endpoint `/api/jobs/{id}` for job status and results
  - Use example notebooks for interactive exploration

> **📖 For complete API documentation:** See [API Reference](07-api-reference.md)  
> **📖 For development scripts:** See [Scripts Guide](scripts.md)
> **📖 For operational best practices:** See [Limitations & Best Practices](05-limitations-best-practices.md)
