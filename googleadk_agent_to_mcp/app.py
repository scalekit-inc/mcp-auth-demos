from google.adk.apps.app import App
from agent import root_agent

app = App(
    name="mcp_agent",
    root_agent=root_agent,
)

__all__ = ["app"]
