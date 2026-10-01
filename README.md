# Agentic AI — Class 3 Demos

Small, standalone demos of LangChain agents and tools, used to practice:
tool-calling agents, prompt templates, and raw LLM API calls across
Groq and OpenAI.

## Files

| File | What it is |
| --- | --- |
| `agent-demo1.py` | Tool-calling agent (Groq LLM) exposing `add_numbers`, `discount`, `weather` as tools, with an interactive REPL and a call-counting tracker. Full scenario docs in [`SCENARIOS.md`](SCENARIOS.md). |
| `agent-demo2.py` | Minimal `ChatPromptTemplate` example: system + human prompt, no tools, one-shot `chain.invoke(...)` explaining a topic. |
| `openai_demo.py` | Raw OpenAI API call (`client.responses.create`) with no agent/tooling — simplest possible example. |
| `business_function.py` | Shared business logic used by `agent-demo1.py`: `sum`, `calculate_discount`, `get_weather` (the latter calls the OpenWeatherMap API). |
| `requirements.txt` | Python dependencies for all demos. |
| `SCENARIOS.md` | Detailed test scenarios, expected results, and a result log for `agent-demo1.py`. |

## Prerequisites

- Python 3.10+
- API keys for the services you want to run:
  - [Groq](https://console.groq.com/) — required for `agent-demo1.py`, `agent-demo2.py`
  - [OpenAI](https://platform.openai.com/) — required for `openai_demo.py`
  - [OpenWeatherMap](https://openweathermap.org/api) — required for the `weather` tool in `agent-demo1.py`

## Setup

### Windows (PowerShell)

```powershell
C:\path\to\python.exe -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

All scripts load configuration from a `.env` file in the repo root (already
gitignored — never commit it). Create one with:

```dotenv
GROQ_API_KEY=your-groq-key
AGENT_MODEL=openai/gpt-oss-120b
OPENWEATHER_API_KEY=your-openweathermap-key
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=your-openai-model-id
```

| Variable | Used by | Notes |
| --- | --- | --- |
| `GROQ_API_KEY` | `agent-demo1.py`, `agent-demo2.py` | Groq console API key |
| `AGENT_MODEL` | `agent-demo1.py`, `agent-demo2.py` | Groq model id, e.g. `openai/gpt-oss-120b` — must not be empty or the first LLM call 404s |
| `OPENWEATHER_API_KEY` | `business_function.py` (`get_weather`) | Free tier key from OpenWeatherMap |
| `OPENAI_API_KEY` | `openai_demo.py` | OpenAI platform API key |
| `OPENAI_MODEL` | `openai_demo.py` | Model id passed to `client.responses.create` — confirm it's a model your account actually has access to before relying on it |

## Running the demos

```bash
python agent-demo1.py   # interactive REPL, see Test scenarios below
python agent-demo2.py   # one-shot: explains "What is RAG" and exits
python openai_demo.py   # one-shot: prints a short bedtime story
```

`agent-demo1.py` can also be driven non-interactively by piping prompts in,
one per line, ending in `exit`:

```bash
printf "Calculate a 10%% discount on a price of 1000.\nexit\n" | python agent-demo1.py
```

## Test scenarios

For `agent-demo1.py`, try the following one at a time (or piped in as above).
Full expected tool calls, pass criteria, and a result log are in
[`SCENARIOS.md`](SCENARIOS.md).

1. **Discount calculation**
   Calculate a 10% discount on a price of 1000.
   Expected: final price `900.0`.

2. **Discount with different values**
   What is the final price for 2500 after a 20% discount?
   Expected: final price `2000.0`.

3. **Addition**
   What is 125 plus 75?
   Expected: `200`.

4. **Addition with negative numbers**
   Add -15 and 27.
   Expected: `12`.

5. **Weather lookup**
   What is the current weather in Boston?
   Expected: current conditions for Boston, or a lookup error if
   OpenWeatherMap is unavailable — the only scenario with a live external
   dependency.

6. **Exit the program**
   `exit` (also accepts `quit` / `q`, case-insensitive) — stops the session
   and prints the LLM/tool call totals.

## Known issues / notes

- `openai_demo.py`'s `OPENAI_MODEL` value is read from `.env` as-is and not
  validated — if it names a model your account can't access, the call fails
  with an API error rather than a clearer local message.
- `get_weather` in `business_function.py` is the only tool with a live
  external dependency (OpenWeatherMap); failures there are expected to
  surface as `"Weather lookup failed"` rather than a crash.
- `.env` is gitignored by design — if a real key is ever pasted into chat,
  a screenshot, or a shared terminal, rotate it.
