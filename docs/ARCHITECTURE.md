# Architecture

## Overview

This project uses a pragmatic hexagonal architecture.

```text
HTTP / UI
  -> API layer
  -> Application services
  -> Domain models + ports
  -> Infrastructure adapters
```

The goal is to keep business workflows independent from transport and vendor choices.

## Layers

### API layer

- Flask routes live in `backend/ad_console/api.py`
- Responsible for request validation, HTTP status codes, and JSON serialization

### Application layer

- `backend/ad_console/application/services.py`
- Coordinates use cases such as account creation, password reset, and unlock approval
- Depends only on domain ports, not on boto3, ldap3, or requests

### Domain layer

- `backend/ad_console/domain/models.py`
- `backend/ad_console/domain/ports.py`
- Holds workflow data and interfaces for external capabilities

### Adapters

- `backend/ad_console/adapters/directory.py`
- `backend/ad_console/adapters/emailing.py`
- `backend/ad_console/adapters/notifications.py`
- `backend/ad_console/adapters/automation.py`
- `backend/ad_console/adapters/ai.py`
- `backend/ad_console/adapters/repositories.py`

Each adapter can be swapped without changing the core workflow code.

## Runtime Modes

### Demo mode

- Default local mode
- Uses in-memory repositories
- Uses console-based side effects instead of external systems
- Makes portfolio review and local execution easy

### Live mode

- Enabled by setting `APP_MODE=live`
- Wires AWS, LDAP, webhook, and email adapters
- Keeps the same service interfaces and API routes

## Why This Refactor Matters

The original shape mixed HTTP handlers, AWS SDK calls, LDAP verification, email templates, and notification logic in one file. That makes testing, replacement, and public sanitization harder.

The current shape improves:

- testability
- readability
- adapter replacement
- portfolio safety
- future persistence and auth extensions
