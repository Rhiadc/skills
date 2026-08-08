# Scanning Go microservices (targeted)

Open this only when bootstrapping or refreshing a card/edge. Goal: **evidence for the brain**, not a full code tour.

## Per folder (budget)

1. `README*` / top-level docs — stated purpose
2. `go.mod` — module path, major deps (HTTP router, gRPC, kafka/nats/rabbit, AWS SDK…)
3. `cmd/` — what binaries exist
4. Config samples: `.env*`, `config*`, `deploy/`, helm/charts — **URLs and neighbor hostnames**
5. Inbound: `http.Handle`, router registrations, gRPC `Register*Server`, OpenAPI/proto if present
6. Outbound: client packages, `http.Client` wrappers, generated gRPC clients, publish helpers — note target service + env key
7. Events: topic/queue constants, publisher/subscriber types

Stop when the service card + relevant map edges are fillable. Do not inventory every internal package.

## Infra folders

- Pipelines, terraform/pulumi, helm, compose: which services they deploy/wire
- Record as `kind: infra` edges (`infra → service`) when release coupling matters

## Evidence quality

| Signal | Confidence |
|--------|------------|
| Client + env key + concrete path/proto in repo | high |
| Env key name only / commented URL | medium |
| Name similarity only | low — mark unknown or ask |

## Refresh triggers

Re-scan a service (targeted) when:

- Handlers/clients/proto/events/config URLs changed in this job
- Plan depends on an edge last verified long ago or `confidence: low`
- Drift suspected
