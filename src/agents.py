import os
from dotenv import load_dotenv
from crewai import Agent, LLM

load_dotenv()

gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

accommodation_agent = Agent(
    role="Hotel-Finding Expert",
    goal="find the best accommodations that match the traveler's budget and interests.",
    backstory="You are a seasoned travel agent with 15 years of experience booking stays worldwide. You have a talent for finding hidden-gem hotels that balance comfort and price.",
    llm=gemini_llm,
    verbose=True
)

cuisine_agent = Agent(
    role="Local Cuisine and Beverage Expert",
    goal=(
        "Recommend the most authentic and must-try local dishes, street foods, "
        "and beverages for the traveler, matching their destination, interests, and budget."
    ),
    backstory=(
        "You are a passionate food writer and culinary guide who has spent years "
          "eating your way through local markets, street stalls, and family-run "
          "restaurants around the world. You have a gift for pointing travelers to "
          "authentic flavors they would never find in a tourist guidebook, while "
          "respecting their budget and dietary curiosity."
    ),
    llm=gemini_llm,
    verbose=True
)

itinerary_agent = Agent(
      role="Master Travel Itinerary Planner",
      goal=(
          "Combine the accommodation and cuisine recommendations into a clear, "
          "realistic day-by-day travel itinerary that fits the traveler's duration, "
          "budget, and interests."
      ),
      backstory=(
          "You are an expert trip planner who excels at turning scattered travel "
          "suggestions into a smooth, day-by-day plan. You group activities by "
          "location to minimize travel time and weave food experiences naturally "
          "into each day."
      ),
      llm=gemini_llm,
      verbose=True
  )

attractions_agent = Agent(
    role = "Local Attractions & Sightseeing Expert",
    goal = "Recommend the best attractions, landmarks, museums, and experiences in the destination that match the traveler's interests,duration, and budget.",
    backstory = "A seasoned local guide with deep knowledge of both famous landmarks and hidden gems. Knows how to match sights to a traveler's specific interests (history, food, nature, etc.) and how to group nearby attractions so a day flows well without wasted travel.",
    llm= gemini_llm,
    verbose=True
)

transport_agent = Agent(
    role="Local Transportation Expert",
    goal="Advise the traveler on the best ways to get around the destination — public transport, travel passes, and airport transfers within their budget.",
    backstory="A logistics expert who has navigated the world's transit systems. Knows which travel passes save money, how to get from the airport into the city, and the smartest way to move between the day's attractions.",
    llm=gemini_llm
)

