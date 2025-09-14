def analyze_diet(meals, water_intake, calories, protein, carbs, fats):
    diet_analysis = {}
    diet_analysis["current_state"] = get_diet_state(meals, water_intake, calories, protein, carbs, fats)
    diet_analysis["improvements"] = get_diet_improvements(meals, water_intake, calories, protein, carbs, fats)
    diet_analysis["consequences"] = get_diet_consequences(meals, water_intake, calories, protein, carbs, fats)
    
    return diet_analysis

def get_diet_state(meals, water_intake, calories, protein, carbs, fats):
    state = {}
    
    state["meal_count"] = len(meals)
    state["water_intake_liters"] = water_intake
    state["total_calories"] = calories
    state["macronutrients"] = {
        "protein_grams": protein,
        "carbs_grams": carbs,
        "fats_grams": fats
    }
    
    if water_intake < 2:
        state["hydration_status"] = "Dehydrated"
    elif water_intake < 3:
        state["hydration_status"] = "Adequately hydrated"
    else:
        state["hydration_status"] = "Well hydrated"
    
    if state["meal_count"] < 3:
        state["meal_frequency"] = "Below recommended"
    elif state["meal_count"] <= 5:
        state["meal_frequency"] = "Optimal"
    else:
        state["meal_frequency"] = "High frequency"
    
    protein_percentage = (protein * 4 / calories) * 100 if calories > 0 else 0
    carbs_percentage = (carbs * 4 / calories) * 100 if calories > 0 else 0
    fats_percentage = (fats * 9 / calories) * 100 if calories > 0 else 0
    
    state["macro_distribution"] = {
        "protein_percentage": round(protein_percentage, 1),
        "carbs_percentage": round(carbs_percentage, 1),
        "fats_percentage": round(fats_percentage, 1)
    }
    
    return state

def get_diet_improvements(meals, water_intake, calories, protein, carbs, fats):
    improvements = []
    
    if water_intake < 2:
        improvements.append("Increase water intake to at least 2-3 liters per day")
    
    if len(meals) < 3:
        improvements.append("Eat at least 3 balanced meals daily")
    
    protein_target = 0.8 * 70  # Assuming 70kg person
    if protein < protein_target:
        improvements.append(f"Increase protein intake to at least {protein_target}g daily")
    
    if calories < 1500:
        improvements.append("Consider increasing caloric intake if trying to maintain weight")
    elif calories > 2500:
        improvements.append("Consider moderating caloric intake if not actively building muscle or highly active")
    
    protein_percentage = (protein * 4 / calories) * 100 if calories > 0 else 0
    carbs_percentage = (carbs * 4 / calories) * 100 if calories > 0 else 0
    fats_percentage = (fats * 9 / calories) * 100 if calories > 0 else 0
    
    if protein_percentage < 15:
        improvements.append("Increase protein proportion in diet")
    if fats_percentage < 20:
        improvements.append("Ensure adequate healthy fat intake")
    if fats_percentage > 40:
        improvements.append("Reduce fat intake, focus on healthy sources")
    
    return improvements

def get_diet_consequences(meals, water_intake, calories, protein, carbs, fats):
    consequences = []
    
    if water_intake < 2:
        consequences.append("Chronic dehydration can lead to kidney problems, fatigue, and reduced cognitive function")
    
    if len(meals) < 3:
        consequences.append("Irregular eating patterns may lead to metabolic issues and energy fluctuations")
    
    if protein < 50:
        consequences.append("Insufficient protein can lead to muscle loss, weakened immune system, and slower recovery")
    
    if calories < 1200:
        consequences.append("Very low calorie intake can lead to nutrient deficiencies, metabolic slowdown, and muscle loss")
    elif calories > 3000 and fats > 100:
        consequences.append("Excessive calorie and fat intake may increase risk of obesity and cardiovascular issues")
    
    if fats < 30:
        consequences.append("Too little fat can affect hormone production and vitamin absorption")
    
    return consequences