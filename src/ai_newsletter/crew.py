from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
import os

from ai_newsletter.tools.search_tool import search_tool, news_search_tool
from ai_newsletter.tools.arxiv_tool import arxiv_tool

# ✅ Define Groq LLM once, reuse across all agents
groq_llm = LLM(
    model=os.environ.get("MODEL", "groq/llama-3.3-70b-versatile"),
    temperature=0.3,      # lower = more factual, less hallucination
    max_tokens=1024,
)

@CrewBase
class AiNewsletter():
    """AI Newsletter Generator Crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],  # type: ignore[index]
            llm=groq_llm,
            tools=[search_tool, news_search_tool, arxiv_tool],
            verbose=True,
            max_rpm=3,
            respect_context_window=True,
        )

    @agent
    def summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer'],  # type: ignore[index]
            llm=groq_llm,
            verbose=True,
            max_rpm=3,
            respect_context_window=True,
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],  # type: ignore[index]
            llm=groq_llm,
            verbose=True,
            max_rpm=3,
            respect_context_window=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],  # type: ignore[index]
        )

    @task
    def summarization_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarization_task'],  # type: ignore[index]
            context=[self.research_task()],
        )

    @task
    def newsletter_task(self) -> Task:
        return Task(
            config=self.tasks_config['newsletter_task'],  # type: ignore[index]
            context=[self.summarization_task()],
            output_file='outputs/newsletter.md',
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=False,   # ⚠️ keep False for Groq — memory needs OpenAI embeddings
            verbose=True,
            max_rpm=3,
        )