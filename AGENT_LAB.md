# Open Deep Research Agent Lab

This fork is set up as a local learning lab for Open Deep Research, LangGraph, and Raindrop Workshop.

## What Is Already Set Up

- Fork: https://github.com/crux311/open_deep_research
- Upstream: https://github.com/langchain-ai/open_deep_research
- Local Python: `.venv` managed by `uv` with Python 3.11
- Local debugger: Raindrop Workshop at `http://localhost:5899`
- Agent UI/API: LangGraph dev server at `http://127.0.0.1:2024`
- Basic Raindrop visibility: each Open Deep Research run creates a top-level Workshop interaction

## First Run

Add keys to `.env`:

```bash
OPENAI_API_KEY=...
SEARCH_API=openai
RAINDROP_LOCAL_DEBUGGER=http://localhost:5899/v1/
```

Then start everything:

```bash
./scripts/start_lab.sh
```

Open:

- Raindrop Workshop: `http://localhost:5899`
- LangGraph API docs: `http://127.0.0.1:2024/docs`
- LangGraph Studio: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`

In Studio, invoke `Deep Researcher` with:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Research the current state of local-first AI observability tools for agent developers. Focus on open source and developer experience."
    }
  ]
}
```

## Learning Path

1. Run the default agent once and inspect the graph in LangGraph Studio.
2. Watch the top-level run appear in Raindrop Workshop.
3. Lower or raise `MAX_RESEARCHER_ITERATIONS`, `MAX_REACT_TOOL_CALLS`, and `MAX_CONCURRENT_RESEARCH_UNITS` in `.env`.
4. Compare `SEARCH_API=openai` with `SEARCH_API=tavily` after adding `TAVILY_API_KEY`.
5. Change one prompt in `src/open_deep_research/prompts.py` and rerun the same research question.
6. Add a focused MCP tool or custom search tool, then inspect how it changes the research trace.

## Notes

The basic local Workshop integration does not require a Raindrop cloud write key. If you add `RAINDROP_WRITE_KEY`, the SDK also enables provider auto-instrumentation for richer model/tool spans where supported.
