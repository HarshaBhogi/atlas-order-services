# Secure Coding Standard

This concise standard is intended for code review exercises and local development. It complements, rather than replaces, organization-specific engineering policy.

## Identity and access

- Authenticate requests before reaching protected business operations.
- Make authorization decisions server-side and close to the protected action.
- Reuse centralized policy helpers where they exist; do not rely on UI controls or caller claims alone.
- Include tests for the expected role, account, and ownership boundaries.

## Input and data access

- Validate request shape, length, type, and allowed values at service boundaries.
- Bind values passed to database statements; select identifiers and ordering expressions from fixed choices.
- Treat file names, object keys, redirect targets, and callback destinations as untrusted input.
- Resolve file locations before access and require them to remain under the configured storage root.

## Integrations and configuration

- Use approved destination policies for outbound integrations.
- Keep operational credentials in managed configuration, not source files.
- Use least-privilege policies for cloud and local infrastructure definitions.
- Pin and inventory deployed dependencies; review advisories against the actual runtime environment.

## Observability and error handling

- Use correlation identifiers and structured events that support incident review.
- Record the minimum necessary request context; do not store credentials, session values, or unrelated headers.
- Return stable client errors while retaining enough server-side detail for diagnosis.
- Define ownership and network exposure for health and readiness endpoints.

## Verification

- Add business-oriented tests for expected access, validation, and failure behavior.
- Run formatting, type checking, dependency review, and application tests before release.
- Reassess controls whenever a change modifies an input boundary, identity decision, storage operation, or integration target.
