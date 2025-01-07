from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo

class MultimodalAgent:
    def __init__(self):
        self.agent = Agent(
            name="Gemini Flush",
            model=Gemini(id="gemini-2.0-flash-exp"),
            tools=[DuckDuckGo()],
            markdown=True
        )

    def run(self, prompt, images=None):
        if images is not None:
            return self.agent.run(prompt, images=images)
        else:
            return self.agent.run(prompt)