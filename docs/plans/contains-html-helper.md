# Implementation Plan — HTML-detection helper function

**Ticket:** Create helper function
**Description:** Create a helper function that returns `True` if a string contains HTML.
**Branch:** `ai/task_123` → `main`

---

## 1. Goal

Add a small, well-tested, reusable helper that answers a single question:

> Does this string contain HTML markup?

```python
contains_html("hello world")            # -> False
contains_html("<p>hello</p>")           # -> True
contains_html("a < b and c > d")        # -> False  (bare comparison operators)
contains_html("click &amp; go")         # -> True   (HTML entity)
```

The function is a pure utility with no I/O and no framework coupling, so it can
be used by services, routes, and validation layers alike.

## 2. Context

This is a **Python 3.12 / FastAPI** project (`zws` package). Current structure:

```
zws/
  app.py
  dependencies.py
  routes/          (api.py, blocked_info.py)
  services/        (blocked_hostnames_service.py)
  schemas/         (blocked_info_schema.py)
  database/        (models, repositories)
```

There is currently **no `utils` package and no test suite**. This plan
introduces both.

> Note on tooling: the state instructions reference a `fastapi-expert` skill and
> a `node-programmer` agent. Neither is available in this environment, and this
> repository is a Python project (no Node.js), so the plan follows idiomatic
> FastAPI/Python practices instead. API-design guidance below reflects FastAPI
> conventions.

## 3. Proposed design

### 3.1 Location

Create a new utilities package:

```
zws/utils/__init__.py
zws/utils/html_detection.py     # contains_html()
```

### 3.2 Signature

```python
def contains_html(value: str) -> bool:
    """Return True if the given string appears to contain HTML markup."""
```

- Accepts a `str`. Non-string / `None` input returns `False` (defensive) rather
  than raising, so callers can pass request data safely.
- Empty or whitespace-only strings return `False`.

### 3.3 Detection strategy

Use Python's standard-library `html.parser.HTMLParser` as the primary detector —
it is robust and dependency-free. A lightweight `HTMLParser` subclass flags a
match when it encounters a start tag, end tag, or start-end (self-closing) tag:

```python
from html.parser import HTMLParser

class _HTMLDetector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.found = False

    def handle_starttag(self, tag, attrs): self.found = True
    def handle_endtag(self, tag):          self.found = True
    def handle_startendtag(self, tag, attrs): self.found = True
```

To reduce false positives from bare comparison operators (`a < b`), gate the
parser with a quick pre-check regex that looks for a plausible tag
(`<[a-zA-Z!/][^>]*>`). Also detect HTML entities (e.g. `&amp;`, `&#39;`) via a
secondary regex `&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);`.

Final result = tag detected **or** entity detected.

Rationale for stdlib over a regex-only approach: a naïve regex both over-matches
(`3 < 5`) and under-matches (attributes with `>` inside quotes). `HTMLParser`
handles real markup correctly; the regex pre-check keeps common plaintext from
being misclassified.

### 3.4 Edge cases to cover

| Input | Expected |
|-------|----------|
| `""`, `"   "` | `False` |
| `None`, non-str | `False` |
| `"plain text"` | `False` |
| `"1 < 2 and 3 > 2"` | `False` |
| `"<p>hi</p>"`, `"<br/>"`, `"<img src='x'>"` | `True` |
| `"<DIV>"` (uppercase) | `True` |
| `"a &amp; b"`, `"&#39;"` | `True` |
| `"<not a tag"` (unclosed, no `>`) | `False` |

## 4. Testing

Add `tests/` package with `tests/utils/test_html_detection.py` using
`pytest`, covering every row in the table above plus a couple of realistic
mixed strings. Add `pytest` to `Pipfile` `[dev-packages]`.

## 5. Optional follow-up (out of scope for this ticket)

If the team wants this surfaced over the API, a thin FastAPI endpoint could wrap
it (e.g. `GET /api/util/contains-html?text=...` returning a Pydantic
`{"contains_html": bool}` response). Not implemented here — kept as a pure
helper until there is a concrete consumer.

## 6. Work breakdown

1. Create `zws/utils/__init__.py` and `zws/utils/html_detection.py` with
   `contains_html`.
2. Add `tests/` with unit tests covering the edge-case table.
3. Add `pytest` to `Pipfile` dev-packages.
4. Run the test suite and confirm green.

## 7. Files touched

- `zws/utils/__init__.py` (new)
- `zws/utils/html_detection.py` (new)
- `tests/__init__.py`, `tests/utils/test_html_detection.py` (new)
- `Pipfile` (add `pytest` dev dependency)
