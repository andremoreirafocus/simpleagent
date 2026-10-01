# Test Scenarios — `agent-demo1.py`

Business-function agent demo. The agent exposes three tools backed by
`business_function.py` and is driven by a Groq-hosted LLM
(`openai/gpt-oss-120b`).

## Components

| Piece | Location | Purpose |
| --- | --- | --- |
| Agent entry point | `agent-demo1.py` | Interactive REPL (`You:` / `Agent:`), wires tools to the LLM |
| Business logic | `business_function.py` | `sum`, `calculate_discount`, `get_weather` |
| Tool wrappers | `agent-demo1.py:56-70` | `add_numbers`, `discount`, `weather` (`@tool`) |
| Call tracker | `agent-demo1.py:18` | Counts LLM + tool calls per turn and for the session |
| Scenario input | `scenarios.txt` | The six prompts below, one per line, ending in `exit` |

## Tool mapping

| Tool | Delegates to | Returns |
| --- | --- | --- |
| `add_numbers(a, b)` | `sum(a, b)` | `int` |
| `discount(price, percentage)` | `calculate_discount(price, percentage)` | `dict` with `original_price`, `discount`, `final_price` |
| `weather(city)` | `get_weather(city)` | `str` like `Boston: overcast clouds, 16.34°C`, or `Weather lookup failed` |

Note: `discount` returns a dict, not a bare number, so the expected value shows
up as `final_price` in the tool output and in the agent's prose answer.

## How to run

Interactive:

```powershell
.\venv\Scripts\activate
python agent-demo1.py
```

Non-interactive (pipe the scenario file in):

```powershell
Get-Content scenarios.txt | .\venv\Scripts\python.exe agent-demo1.py
```

Run one scenario at a time by typing it at the `You:` prompt instead. Press
`Ctrl+C` to abort mid-run.

## Scenarios

### 1. Discount calculation

- **Prompt:** `Calculate a 10% discount on a price of 1000.`
- **Expected tool:** `discount(price=1000, percentage=10)`
- **Expected result:** `final_price` is `900.0`
- **Pass:** the agent states a final price of 900

### 2. Discount with different values

- **Prompt:** `What is the final price for 2500 after a 20% discount?`
- **Expected tool:** `discount(price=2500, percentage=20)`
- **Expected result:** `final_price` is `2000.0`
- **Pass:** the agent states a final price of 2000

### 3. Addition

- **Prompt:** `What is 125 plus 75?`
- **Expected tool:** `add_numbers(a=125, b=75)`
- **Expected result:** `200`
- **Pass:** the agent states 200

### 4. Addition with negative numbers

- **Prompt:** `Add -15 and 27.`
- **Expected tool:** `add_numbers(a=-15, b=27)`
- **Expected result:** `12`
- **Pass:** the agent states 12

### 5. Weather lookup

- **Prompt:** `What is the current weather in Boston?`
- **Expected tool:** `weather(city="Boston")`
- **Expected result:** current conditions for Boston, e.g. `Boston: overcast clouds, 16.34°C`
- **Pass:** the agent reports Boston conditions, or reports a lookup failure if
  the OpenWeatherMap service is unavailable or rate-limited
- **Note:** this is the only scenario with a live external dependency, so it is
  the only one that can fail for reasons outside the code

### 6. Exit the program

- **Prompt:** `exit`
- **Expected result:** the agent prints `Goodbye!`, stops the session, and prints
  session totals
- **Pass:** the process exits cleanly without another LLM or tool call
- **Note:** `exit`, `quit`, and `q` are all accepted, case-insensitively

## Expected run shape

Each of scenarios 1-5 costs 2 LLM calls and 1 tool call: one LLM call to decide,
one tool execution, one LLM call to phrase the answer. The per-turn line reads:

```
   >> this turn: LLM calls: 2 | Tool calls: 1 (discount=1)
```

A full `scenarios.txt` run therefore ends with:

```
Goodbye!

Session totals: LLM calls: 10 | Tool calls: 5
```

## Result log

Observed on 2026-09-29 with `langchain 1.4.3`, `langchain-groq 1.1.3`,
Python 3.14.6:

| # | Scenario | Tool called | Result | Status |
| --- | --- | --- | --- | --- |
| 1 | Discount 10% of 1000 | `discount` | `final_price: 900.0` | PASS |
| 2 | Discount 20% of 2500 | `discount` | `final_price: 2000.0` | PASS |
| 3 | 125 + 75 | `add_numbers` | `200` | PASS |
| 4 | -15 + 27 | `add_numbers` | `12` | PASS |
| 5 | Weather in Boston | `weather` | `overcast clouds, 16.34°C` | PASS |
| 6 | `exit` | none | `Goodbye!` + totals | PASS |

All six scenarios pass. Session totals: 10 LLM calls, 5 tool calls.

## Known issue fixed during this test

The first run crashed on scenario 1 with
`UnicodeEncodeError: 'charmap' codec can't encode character '\u202f'`. The model
replies using U+202F (narrow no-break space) before units such as `%`, and the
Windows console defaults to cp1252. `main()` now calls
`sys.stdout.reconfigure(encoding="utf-8", errors="replace")` before the REPL
starts, so agent output prints regardless of console codepage.

If you see the same error when running other demos in this folder, the same
fix applies, or run with `PYTHONUTF8=1` in the environment.

## Security note

`agent-demo1.py:11` and `business_function.py:15` contain live API keys in
plaintext, committed alongside the source. They are left as-is for this training
demo. Before any real use, rotate both keys and move them to environment
variables (`.env` is already in `.gitignore`).
