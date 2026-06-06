from crewai import Crew, Process
from src.agents import accommodation_agent, cuisine_agent, itinerary_agent, attractions_agent, transport_agent
from src.tasks import accommodation_task, cuisine_task, itinerary_task, attractions_task, transport_task

travel_crew = Crew(
    agents=[accommodation_agent, cuisine_agent, itinerary_agent, attractions_agent, transport_agent],
    tasks=[accommodation_task, cuisine_task, attractions_task, transport_task, itinerary_task],
    process=Process.sequential,
    verbose=True
)

result = travel_crew.kickoff()

print("\n\n========= FINAL RESULT =========\n")
print(result)