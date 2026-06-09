from pydantic import BaseModel, Field


class CostBreakdown(BaseModel):
    accommodation: int = Field(description="Total accommodation cost for the whole trip")
    transport: int = Field(description="Total transport cost for the whole trip")
    food: int = Field(description="Total food cost for the whole trip")
    entry_fees: int = Field(description="Total attraction entry fees for the whole trip")


class DayPlan(BaseModel):
    day: int = Field(description="Day number, e.g. 1")
    base_area: str = Field(description="The area to base the day around, e.g. Koti")
    activities: list[str] = Field(description="2-3 attractions/activities for the day")
    foods: list[str] = Field(description="Local foods to try that day")


class Itinerary(BaseModel):
    days: list[DayPlan] = Field(description="The day-by-day plan, one entry per day")
    cost_breakdown: CostBreakdown = Field(description="Cost split by category")
    total: int = Field(description="The sum of all costs for the trip")
    currency: str = Field(description="Currency code, e.g. INR")
    fits_budget: bool = Field(description="True if total is within the traveler's budget")
