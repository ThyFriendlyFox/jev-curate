# Clients

A client answers a rubric's questions about one row's state. jev-curate has 2
clients. Select one with the `--mock` flag: absent means live.

## live

`LiveJevClient` calls `POST /v1/systemone` through `typesafe-sdk`. It is the
default and the only client for real runs. It needs `TYPESAFE_API_KEY`. The
SDK retries HTTP 408, 429, and 5xx twice with backoff inside a 30 second
budget. An authentication error propagates and stops the run.

```sh
export TYPESAFE_API_KEY="sk-..."
jev-curate run --rubric R --input I --output O
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
  `CONFIGURATION.md`, and a test in `tests/test_pipeline.py`.
