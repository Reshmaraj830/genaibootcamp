import streamlit as st

def generate_meal_plan(dietary_preference, goal):
    """
    This is a placeholder function. In a real application, this would:
    1. Query a recipe database/API based on preferences and goals.
    2. Select appropriate recipes for a week.
    3. Construct a meal plan structure.
    4. Extract ingredients for a shopping list.
    """
    meal_plan_output = f"## Weekly Meal Plan for {goal} ({dietary_preference})\n\n"
    shopping_list_output = "## Shopping List\n\n"

    if dietary_preference == "Vegan" and goal == "Weight Loss":
        meal_plan_output += """
        **Monday:**
        * Breakfast: Oatmeal with berries and nuts
        * Lunch: Large salad with chickpeas and vinaigrette
        * Dinner: Lentil soup with whole-grain bread

        **Tuesday:**
        * Breakfast: Smoothie with spinach, banana, and plant-based protein
        * Lunch: Quinoa bowl with roasted vegetables
        * Dinner: Tofu scramble with sweet potatoes

        ... (continue for 7 days with specific vegan, weight-loss focused recipes)
        """
        shopping_list_output += """
        * Oats
        * Mixed berries
        * Almonds
        * Chickpeas (canned)
        * Leafy greens (spinach, kale, lettuce)
        * Lentils
        * Whole-grain bread
        * Bananas
        * Plant-based protein powder
        * Quinoa
        * Assorted vegetables (bell peppers, zucchini, broccoli)
        * Firm Tofu
        * Sweet potatoes
        ... (list all ingredients from the 7-day plan)
        """
    elif dietary_preference == "Keto" and goal == "Muscle Gain":
        meal_plan_output += """
        **Monday:**
        * Breakfast: Scrambled eggs with bacon and avocado
        * Lunch: Grilled chicken salad with olive oil dressing
        * Dinner: Steak with buttered broccoli

        **Tuesday:**
        * Breakfast: Keto pancakes with sugar-free syrup
        * Lunch: Salmon and asparagus
        * Dinner: Ground beef stir-fry with low-carb vegetables

        ... (continue for 7 days with specific keto, muscle-gain focused recipes)
        """
        shopping_list_output += """
        * Eggs
        * Bacon
        * Avocados
        * Chicken breast
        * Lettuce
        * Olive oil
        * Steak (ribeye/sirloin)
        * Broccoli
        * Butter
        * Almond flour (for pancakes)
        * Sugar-free syrup
        * Salmon fillets
        * Asparagus
        * Ground beef
        * Low-carb vegetables (cabbage, green beans)
        ... (list all ingredients from the 7-day plan)
        """
    else:
        meal_plan_output += f"""
        **Coming Soon!** We are still developing meal plans for
        your specific combination of '{dietary_preference}' and '{goal}'.
        Please try another combination or check back later!
        """
        shopping_list_output = "" # No shopping list if no plan generated

    return meal_plan_output, shopping_list_output

st.set_page_config(page_title="Meal Plan Generator", layout="wide")

st.title("🍽️ Meal Plan Generator")
st.markdown("Enter your dietary preferences and goals to get a personalized weekly meal plan and shopping list!")

# User Inputs