from crewai import Task
from src.agents import accommodation_agent, cuisine_agent,itinerary_agent,attractions_agent,transport_agent

accommodation_task= Task(
    description=(
      "Find the best accommodations for a traveler going to {destination} for {duration} days "
      "with a total budget of {budget}, who is interested in {interests}."
    ),
    expected_output="A list of 3 hotels, each with name, price per night, and why it fits.",
    agent=accommodation_agent
)

cuisine_task = Task(
    description=(
        "Recommend the best local dishes, street foods, and beverages to try in "
        "{destination} for a {duration}-day trip, for a traveler interested in {interests} with "
        "a total budget of {budget}. Focus on authentic, local options."
    ),
    expected_output=(
        "A list of 5 to 6 local foods and 2 to 3 local beverages. For each item, "
        "give its name, a one-line description, and roughly where or how to try it."
    ),
    agent=cuisine_agent
)

attractions_task = Task(
    description="Recommend the best attractions, landmarks, museums, and experiences in {destination} for a {duration}-day trip, for a traveler interested in {interests}, within a total budget of {budget}. Group nearby attractions together so each day flows well.",
    expected_output="A organized list of recommended attractions grouped by area/theme, each with a short reason why it fits the traveler's interest in {interests}, and a note on roughly how much time to spend there.",
    agent=attractions_agent
)

transport_task = Task(
    description="Advise on the best ways to get around {destination} during a {duration}-day trip for a traveler interested in {interests}, within a total budget of {budget}. Cover airport transfers, public transport options, and any money-saving travel passes.",
    expected_output="A clear transport guide: airport-to-city options, the best way to get around the city (with any recommended passes and rough costs), and tips for moving between attraction areas efficiently.",
    agent=transport_agent
)

itinerary_task = Task(
      description=(
          "Using the recommended hotels, local food, attractions, and transport "
          "suggestions, create a detailed day-by-day itinerary for a {duration}-day trip to "
          "{destination} for a traveler interested in {interests}, within a total budget "
          "of {budget}. Use the Weather Tool to check the current weather in {destination}, "
          "and factor it into the plan — favor outdoor sights on clear days and "
          "indoor options (museums, food halls) if the weather is poor."
      ),
      expected_output=(
          "A day-by-day plan (Day 1 to Day {duration}). For each day, suggest a base area, "
          "2-3 activities/attractions, and specific local foods to try that day, "
          "keeping nearby places grouped together."
      ),
      agent=itinerary_agent,
      context=[accommodation_task, cuisine_task, attractions_task, transport_task]   # ← the baton!
  )


