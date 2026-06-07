from crewai import Crew, Process
from src.agents import accommodation_agent, cuisine_agent, itinerary_agent, attractions_agent, transport_agent
from src.tasks import accommodation_task, cuisine_task, itinerary_task, attractions_task, transport_task

travel_crew = Crew(
    agents=[accommodation_agent, cuisine_agent, itinerary_agent, attractions_agent, transport_agent],
    tasks=[accommodation_task, cuisine_task, attractions_task, transport_task, itinerary_task],
    process=Process.sequential,
    verbose=True
)

destination = input("Where do you want to travel? ")
duration    = input("How many days is your trip? ")
budget      = input("What is your total budget? ")
currency    = input("In what currency? (e.g. INR, USD, EUR) ")
interests   = input("What are your interests? (e.g. food, history) ")

result = travel_crew.kickoff(inputs={
      "destination": destination,
      "duration":    duration,
      "budget":      budget,
      "currency":    currency,
      "interests":   interests,
})

print("\n\n========= FINAL RESULT =========\n")
print(result)