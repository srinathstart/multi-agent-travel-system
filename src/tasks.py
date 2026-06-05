from crewai import Task
from src.agents import accommodation_agent, cuisine_agent,itinerary_agent

accommodation_task= Task(
    description=(
      "Find the best accommodations for a traveler going to Tokyo for 5 days "
      "with a total budget of ₹80,000, who is interested in food and history."
    ),
    expected_output="A list of 3 hotels, each with name, price per night, and why it fits.",
    agent=accommodation_agent
)

cuisine_task = Task(
    description=(
        "Recommend the best local dishes, street foods, and beverages to try in "
        "Tokyo for a 5-day trip, for a traveler interested in food and history with "
        "a total budget of ₹80,000. Focus on authentic, local options."
    ),
    expected_output=(
        "A list of 5 to 6 local foods and 2 to 3 local beverages. For each item, "
        "give its name, a one-line description, and roughly where or how to try it."
    ),
    agent=cuisine_agent
)

itinerary_task = Task(
      description=(
          "Using the recommended hotels and local food suggestions, create a "
          "detailed day-by-day itinerary for a 5-day trip to Tokyo for a traveler "
          "interested in food and history, within a total budget of ₹80,000."
      ),
      expected_output=(
          "A day-by-day plan (Day 1 to Day 5). For each day, suggest a base area, "
          "2-3 activities/attractions, and specific local foods to try that day, "
          "keeping nearby places grouped together."
      ),
      agent=itinerary_agent,
      context=[accommodation_task, cuisine_task]   # ← the baton!
  )
