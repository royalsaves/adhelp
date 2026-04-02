# Project Guide

Use this repository as a portfolio demo for:

- backend modularization with hexagonal architecture
- adapter-driven integrations
- local demo execution without cloud credentials
- lightweight operations UI for support workflows

Start with:

1. [README.md](../README.md)
2. [ARCHITECTURE.md](./ARCHITECTURE.md)
3. `backend/ad_console/application/services.py`

If you want to present the project in an interview, focus on:

- how the original all-in-one backend was separated by responsibility
- how demo and live adapters share the same service contracts
- how the public version avoids exposing private infrastructure details
