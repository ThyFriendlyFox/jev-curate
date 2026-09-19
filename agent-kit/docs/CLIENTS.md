# Clients

A client answers a rubric's questions about one row's state. jev-curate has 3
clients. No flag means live. `--gateway` and `--mock` select the other 2.

## live

`LiveJevClient` calls `POST /v1/systemone` through `typesafe-sdk`. It is the
default. It needs `TYPESAFE_API_KEY`. The
SDK retries HTTP 408, 429, and 5xx twice with backoff inside a 30 second
budget. An authentication error propagates and stops the run.

```sh
export TYPESAFE_API_KEY="sk-..."
jev-curate run --rubric R --input I --output O
```

## gateway

`GatewayJevClient` calls the same live Jev through Vercel AI Gateway, for an
account that holds a gateway key and no TypeSafe key. It needs
`AI_GATEWAY_API_KEY`. The gateway has its own protocol
(`POST /v4/ai/evaluation-model`), so `GatewayTransport` rewrites each
`typesafe-sdk` request and reply. Retries, timeouts, and error types stay the
SDK's. An authentication error propagates and stops the run.

| Native | Gateway |
|---|---|
| question `type: noul` | `type: boolean` |
| answer `noul` | `probability` |
| answer `confidence` | `providerMetadata.typesafe.confidence.<gate>` |
| score `legend` | rebuilt from the gate's `criteria` |
| model `jev-latest` | `typesafe-ai/jev`; a model with `/` is sent as is |

A choice or score reply with no confidence is an error row, not a guess. The
gateway's free tier returns HTTP 429 after about 4 requests. Those rows land in
`errors.jsonl`; run again later with `--retry-errors`.

Free-tier behavior observed on 2026-09-19 with `examples/trec/rubric.yaml`.
Vercel and TypeSafe document none of it, and no reply carries a `Retry-After`
header. The causes are not proven; the observations are.

| Observed | Times |
|---|---|
| A request of 25, 60, 70, or 75 rows passed (75 rows: 150 questions, 15,609 input tokens, 0.9 s) | 8 |
| A request of 100, 125, 300, or 1,000 rows got HTTP 503 | 4 of 4 |
| A request of 60 to 87 rows got 503 when it came seconds after a large request | 3 |
| A 60-row request got 503 as the first request after 10 quiet minutes. The 3 attempts before the wait were refused 100-row requests | 1 |
| 3 requests of 60 rows, 90 seconds apart, passed; the 4th got HTTP 429 | 1 |
| 4 small requests passed, then 429 | 2 |
| 429 cleared after 10 quiet minutes. It did not clear after 3 minutes, or under a retry every 75 seconds | 5, 1, 1 |

The pattern fits a token budget that refills slowly and that refused requests
also drain, with a separate request count behind the 429. Jev counts the
shared state once and about 100 tokens for each question. The SDK retries a
503 or a 429 twice, so 1 refused batch costs 3 attempts. What worked:
`--batch-size 60`, 3 requests 90 seconds apart, then 10 quiet minutes.

```sh
export AI_GATEWAY_API_KEY="vck_..."
jev-curate run --gateway --rubric R --input I --output O
```

## mock

`MockJevClient` answers from regular expressions and a hash of the text. It
exists so tests and the verify gates run without a key or network. Its
probabilities mean nothing outside tests; never tune a threshold against it.

```sh
jev-curate run --mock --rubric R --input I --output O
```

## Writing a new client

Implement `jev_curate.client.JevClient`:

```python
class JevClient(ABC):
    def evaluate(self, state, questions: dict[str, Question], *, model: str) -> SystemOneResponse
```

- `state` is text or a JSON object. `questions` are `typesafe_sdk` question
  objects built by `CurationRubric.to_jev_questions()`.
- Return a `SystemOneResponse` whose `answers` are keyed by gate name. A gate
  with no answer fails closed.
- Raise `TypeSafeAuthenticationError` for a rejected credential. Any other
  exception becomes 1 line in `errors.jsonl` for that row.
- `evaluate` may be called from several threads at once when `--concurrency`
  is above 1. Do not share mutable state without a lock.
- Register it in `make_client`, add its section here, its flag in
  `CONFIGURATION.md`, and a test that runs it through `CurationPipeline`.
