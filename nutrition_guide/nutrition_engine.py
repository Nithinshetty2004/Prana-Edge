import pandas as pd
import yaml
import json
import os
import math
import random

class NutritionEngine:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.foods_data = pd.read_csv(os.path.join(current_dir, 'data/foods.csv'))
        self.recipes_data = pd.read_csv(os.path.join(current_dir, 'data/recipes.csv'))
        
        with open(os.path.join(current_dir, 'data/disease_recommendations.yaml'), 'r') as file:
            self.disease_recommendations = yaml.safe_load(file)
    
    def calculate_health_metrics(self, height_cm, weight_kg):
        if height_cm <= 0 or weight_kg <= 0:
            return {"error": "Height and weight must be positive values"}
        
        height_m = height_cm / 100
        bmi = weight_kg / (height_m * height_m)
        
        if bmi < 18.5:
            weight_status = "Underweight"
            recommendation = "Consider increasing caloric intake with nutrient-dense foods"
        elif bmi < 25:
            weight_status = "Normal weight"
            recommendation = "Maintain a balanced diet with adequate nutrients"
        elif bmi < 30:
            weight_status = "Overweight"
            recommendation = "Consider moderating caloric intake and increasing physical activity"
        else:
            weight_status = "Obese"
            recommendation = "Consider a structured nutrition plan focused on caloric deficit and regular exercise"
        
        return {
            "bmi": round(bmi, 2),
            "weight_status": weight_status,
            "general_recommendation": recommendation
        }
    
    def calculate_caloric_needs(self, weight_kg, height_cm, age, gender, activity_level):
        if gender.lower() == 'male':
            bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
        
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
        
        return math.floor(bmr * multiplier)
    
    def get_recommendations(self, height, weight, age, gender, activity_level, diseases):
        health_metrics = self.calculate_health_metrics(height, weight)
        caloric_needs = self.calculate_caloric_needs(weight, height, age, gender, activity_level)
        
        weight_status = health_metrics["weight_status"]
        
        if weight_status == "Underweight":
            macro_split = {"protein": 25, "carbs": 55, "fats": 20}
            caloric_adjustment = 300
        elif weight_status == "Normal weight":
            macro_split = {"protein": 30, "carbs": 45, "fats": 25}
            caloric_adjustment = 0
        elif weight_status == "Overweight":
            macro_split = {"protein": 35, "carbs": 40, "fats": 25}
            caloric_adjustment = -250
        else:  # Obese
            macro_split = {"protein": 40, "carbs": 30, "fats": 30}
            caloric_adjustment = -500
        
        adjusted_calories = caloric_needs + caloric_adjustment
        
        # Get food recommendations
        recommended_foods = self._get_food_recommendations(weight_status, diseases)
        
        # Get recipe recommendations
        recommended_recipes = self._get_recipe_recommendations(weight_status, diseases)
        
        # Additional disease-specific advice
        disease_advice = self._get_disease_specific_advice(diseases)
        
        return {
            "health_metrics": health_metrics,
            "nutrition_plan": {
                "daily_calories": adjusted_calories,
                "macronutrient_split": macro_split,
                "protein_grams": math.floor((adjusted_calories * (macro_split["protein"] / 100)) / 4),
                "carbs_grams": math.floor((adjusted_calories * (macro_split["carbs"] / 100)) / 4),
                "fats_grams": math.floor((adjusted_calories * (macro_split["fats"] / 100)) / 9)
            },
            "recommended_foods": recommended_foods,
            "recommended_recipes": recommended_recipes,
            "disease_specific_advice": disease_advice
        }
    
    def _get_food_recommendations(self, weight_status, diseases):
        # Filter foods based on weight status and diseases
        filtered_foods = self.foods_data.copy()
        
        # Apply weight status filters
        if weight_status == "Underweight":
            filtered_foods = filtered_foods[filtered_foods['calorie_density'] >= 'medium']
        elif weight_status == "Overweight" or weight_status == "Obese":
            filtered_foods = filtered_foods[filtered_foods['calorie_density'] <= 'medium']
        
        # Apply disease filters
        for disease in diseases:
            if disease.lower() in self.disease_recommendations:
                avoid_foods = self.disease_recommendations[disease.lower()]["avoid_foods"]
                filtered_foods = filtered_foods[~filtered_foods['food_name'].isin(avoid_foods)]
        
        # Select top foods for each category
        protein_foods = filtered_foods[filtered_foods['category'] == 'protein'].nlargest(5, 'protein_per_serving')
        vegetable_foods = filtered_foods[filtered_foods['category'] == 'vegetable'].nlargest(5, 'fiber_per_serving')
        fruit_foods = filtered_foods[filtered_foods['category'] == 'fruit'].nlargest(5, 'vitamins_score')
        grain_foods = filtered_foods[filtered_foods['category'] == 'grain'].nlargest(5, 'fiber_per_serving')
        dairy_foods = filtered_foods[filtered_foods['category'] == 'dairy'].nlargest(3, 'calcium_per_serving')
        
        # Combine recommendations
        recommendations = {
            "protein_sources": protein_foods['food_name'].tolist(),
            "vegetables": vegetable_foods['food_name'].tolist(),
            "fruits": fruit_foods['food_name'].tolist(),
            "grains": grain_foods['food_name'].tolist(),
            "dairy": dairy_foods['food_name'].tolist()
        }
        
        return recommendations
    
    def _get_recipe_recommendations(self, weight_status, diseases):
        # Filter recipes based on weight status and diseases
        filtered_recipes = self.recipes_data.copy()
        
        # Apply weight status filters
        if weight_status == "Underweight":
            filtered_recipes = filtered_recipes[filtered_recipes['calorie_level'] >= 'medium']
        elif weight_status == "Overweight" or weight_status == "Obese":
            filtered_recipes = filtered_recipes[filtered_recipes['calorie_level'] <= 'medium']
        
        # Apply disease filters
        for disease in diseases:
            if disease.lower() in self.disease_recommendations:
                avoid_ingredients = self.disease_recommendations[disease.lower()]["avoid_foods"]
                for ingredient in avoid_ingredients:
                    filtered_recipes = filtered_recipes[~filtered_recipes['ingredients'].str.contains(ingredient, case=False, na=False)]
        
        # Select random recipes
        if len(filtered_recipes) > 10:
            recommended_recipes = filtered_recipes.sample(10)
        else:
            recommended_recipes = filtered_recipes
        
        return recommended_recipes[['recipe_name', 'meal_type', 'prep_time', 'calories_per_serving']].to_dict('records')
    
    def _get_disease_specific_advice(self, diseases):
        advice = {}
        
        for disease in diseases:
            if disease.lower() in self.disease_recommendations:
                advice[disease] = {
                    "recommendation": self.disease_recommendations[disease.lower()]["general_advice"],
                    "recommended_foods": self.disease_recommendations[disease.lower()]["recommended_foods"]
                }
            else:
                advice[disease] = {
                    "recommendation": "No specific recommendations available for this condition. Consider consulting with a healthcare professional."
                }
        
        return advice