# Content Swarm

import os
from crewai import Agent, Task, Crew, Process

# --- 1. DEFINE THE PERSONAS (The Team) ---

# Agent A: The Analyst
# "Scrapes the transcript and extracts 3 viral hooks."
analyst = Agent(
    role='Lead Viral Analyst',
    goal='Analyze video transcripts to find viral hooks',
    backstory="""You are an expert data analyst who studies the YouTube algorithm.
    You do not care about "feelings". You care about Retention Rate.
    You extract the 3 specific moments in a script that will grab attention.""",
    verbose=True,
    allow_delegation=False,
    # tools=[YouTubeScraperTool()] # TODO: Connect your tool here
)

# Agent B: The Ghostwriter
# "Takes hooks and formats them into a LinkedIn post."
ghostwriter = Agent(
    role='LinkedIn Ghostwriter',
    goal='Write high-engagement LinkedIn posts',
    backstory="""You are a ghostwriter for top Silicon Valley founders.
    Your writing style is punchy and direct.
    RULES:
    - Sentences must be under 15 words.
    - No hashtags.
    - No emojis.
    - One line per paragraph.""",
    verbose=True
)

# Agent C: The Editor
# "Takes the post and reformats it for a Newsletter."
editor = Agent(
    role='Newsletter Editor',
    goal='Convert social posts into educational emails',
    backstory="""You are the Chief Editor of a Substack with 100k subscribers.
    You take the raw energy of a social post and add structure, intro, and nuance.
    You write in a professional, slightly academic tone.""",
    verbose=True
)

# --- 2. DEFINE THE TASKS ---
task_analyze = Task(
    description='Analyze the following transcript: {transcript}',
    expected_output='A report with 3 distinct viral hooks.',
    agent=analyst
)

task_write = Task(
    description='Create a LinkedIn post based on the viral hooks.',
    expected_output='A text file with the LinkedIn post.',
    agent=ghostwriter
)

task_edit = Task(
    description='Convert the LinkedIn post into a newsletter draft.',
    expected_output='A markdown file formatted for email.',
    agent=editor
)

# --- 3. THE MANAGER (Orchestration) ---
content_crew = Crew(
    agents=[analyst, ghostwriter, editor],
    tasks=[task_analyze, task_write, task_edit],
    process=Process.sequential, # Data flows strictly Left to Right
    verbose=2
)

# --- THE CHALLENGE FOR YOU ---
if __name__ == "__main__":
    # TODO: WRAP THIS IN FASTAPI
    # Right now, this runs in the terminal.
    # If you want to sell this as a SaaS, you need to:
    # 1. Create a `main.py` with FastAPI
    # 2. Create a POST endpoint `/generate-content`
    # 3. Accept a YouTube URL, scrape it, and pass it here.
    
    print("Starting the Content Swarm...")
    result = content_crew.kickoff(inputs={'transcript': '...insert scraped text here...'})
    print(result)