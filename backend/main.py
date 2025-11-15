from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import math
from weasyprint import HTML, CSS
from jinja2 import Template
import io

app = FastAPI(title="Health Assessment API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class UserHealthInfo(BaseModel):
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=1, le=120)
    gender: str = Field(..., pattern="^(male|female|other)$")
    height: float = Field(..., gt=0, description="Height in cm")
    weight: float = Field(..., gt=0, description="Weight in kg")
    activity_level: str = Field(..., pattern="^(sedentary|lightly_active|moderately_active|very_active|extra_active)$")
    goal: str = Field(..., pattern="^(lose_weight|maintain|gain_muscle|improve_fitness)$")
    dietary_preference: Optional[str] = Field(None, pattern="^(none|vegetarian|vegan|keto|paleo)$")
    medical_conditions: Optional[List[str]] = None

class HealthAssessment(BaseModel):
    bmi: float
    bmi_category: str
    bmr: float
    daily_calories: float
    protein_grams: float
    carbs_grams: float
    fats_grams: float
    water_liters: float
    ideal_weight_range: dict
    health_risks: List[str]
    recommendations: List[str]

class PersonalizedPlan(BaseModel):
    user_info: UserHealthInfo
    assessment: HealthAssessment
    workout_plan: List[dict]
    meal_suggestions: List[dict]
    lifestyle_tips: List[str]
    weekly_goals: dict

# Health Calculations
def calculate_bmi(weight: float, height: float) -> float:
    """Calculate BMI: weight(kg) / (height(m))^2"""
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)

def get_bmi_category(bmi: float) -> str:
    """Categorize BMI according to WHO standards"""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender.lower() == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    return round(bmr, 2)

def calculate_daily_calories(bmr: float, activity_level: str, goal: str) -> float:
    """Calculate daily calorie needs based on activity level and goals"""
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "extra_active": 1.9
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)
    
    # Adjust based on goal
    if goal == "lose_weight":
        return round(tdee - 500, 2)  # 500 cal deficit for ~0.5kg/week loss
    elif goal == "gain_muscle":
        return round(tdee + 300, 2)  # 300 cal surplus for muscle gain
    else:
        return round(tdee, 2)

def calculate_macros(daily_calories: float, goal: str) -> dict:
    """Calculate macronutrient distribution"""
    if goal == "lose_weight":
        protein_percent = 0.35
        carbs_percent = 0.35
        fats_percent = 0.30
    elif goal == "gain_muscle":
        protein_percent = 0.30
        carbs_percent = 0.45
        fats_percent = 0.25
    else:
        protein_percent = 0.25
        carbs_percent = 0.50
        fats_percent = 0.25
    
    return {
        "protein": round((daily_calories * protein_percent) / 4, 2),
        "carbs": round((daily_calories * carbs_percent) / 4, 2),
        "fats": round((daily_calories * fats_percent) / 9, 2)
    }

def calculate_ideal_weight(height: float, gender: str) -> dict:
    """Calculate ideal weight range using multiple formulas"""
    height_m = height / 100
    
    # Using BMI range 18.5-24.9 for normal weight
    min_weight = round(18.5 * (height_m ** 2), 1)
    max_weight = round(24.9 * (height_m ** 2), 1)
    
    return {
        "min_kg": min_weight,
        "max_kg": max_weight,
        "range": f"{min_weight}-{max_weight} kg"
    }

def assess_health_risks(bmi: float, age: int, medical_conditions: Optional[List[str]]) -> List[str]:
    """Identify potential health risks"""
    risks = []
    
    if bmi < 18.5:
        risks.append("Increased risk of nutritional deficiencies and weakened immune system")
        risks.append("Potential bone density issues")
    elif bmi >= 25 and bmi < 30:
        risks.append("Moderate risk of cardiovascular disease")
        risks.append("Increased risk of type 2 diabetes")
    elif bmi >= 30:
        risks.append("High risk of cardiovascular disease")
        risks.append("Significantly increased risk of type 2 diabetes")
        risks.append("Risk of sleep apnea and joint problems")
        risks.append("Increased risk of certain cancers")
    
    if age > 40 and bmi >= 25:
        risks.append("Age-related metabolic slowdown combined with excess weight")
    
    if medical_conditions:
        risks.append(f"Existing conditions require medical supervision: {', '.join(medical_conditions)}")
    
    return risks if risks else ["No significant health risks identified"]

def generate_recommendations(user: UserHealthInfo, bmi: float, bmi_category: str) -> List[str]:
    """Generate personalized health recommendations"""
    recommendations = []
    
    # BMI-based recommendations
    if bmi < 18.5:
        recommendations.extend([
            "Focus on nutrient-dense, calorie-rich foods",
            "Incorporate strength training to build muscle mass",
            "Eat 5-6 smaller meals throughout the day",
            "Consider protein shakes as supplements"
        ])
    elif bmi >= 25:
        recommendations.extend([
            "Create a sustainable calorie deficit through balanced eating",
            "Increase physical activity gradually",
            "Focus on whole foods and reduce processed foods",
            "Practice portion control and mindful eating"
        ])
    
    # Goal-specific recommendations
    if user.goal == "lose_weight":
        recommendations.extend([
            "Aim for 0.5-1 kg weight loss per week for sustainable results",
            "Combine cardio exercises with strength training",
            "Stay hydrated - drink water before meals",
            "Get 7-9 hours of quality sleep per night"
        ])
    elif user.goal == "gain_muscle":
        recommendations.extend([
            "Prioritize progressive overload in strength training",
            "Ensure adequate protein intake (1.6-2.2g per kg body weight)",
            "Allow proper recovery time between workouts",
            "Consider creatine supplementation (consult a professional)"
        ])
    elif user.goal == "improve_fitness":
        recommendations.extend([
            "Include a mix of cardio, strength, and flexibility training",
            "Set specific, measurable fitness goals",
            "Track your progress weekly",
            "Gradually increase workout intensity"
        ])
    
    # Activity level recommendations
    if user.activity_level == "sedentary":
        recommendations.append("Start with 10-15 minute walks daily and gradually increase")
        recommendations.append("Take regular breaks from sitting every hour")
    
    # Age-specific recommendations
    if user.age > 50:
        recommendations.extend([
            "Include balance and flexibility exercises to prevent falls",
            "Focus on bone-strengthening activities",
            "Consider vitamin D and calcium supplementation (consult doctor)"
        ])
    
    # General health recommendations
    recommendations.extend([
        "Regular health check-ups and blood work annually",
        "Manage stress through meditation or yoga",
        "Limit alcohol consumption and avoid smoking",
        "Build a support system for accountability"
    ])
    
    return recommendations[:12]  # Return top 12 recommendations

def generate_workout_plan(user: UserHealthInfo, bmi_category: str) -> List[dict]:
    """Generate a weekly workout plan"""
    base_cardio_duration = 30 if user.activity_level in ["sedentary", "lightly_active"] else 45
    
    if user.goal == "lose_weight":
        return [
            {"day": "Monday", "type": "Cardio", "activity": "Brisk walking or jogging", "duration": f"{base_cardio_duration} min", "intensity": "Moderate"},
            {"day": "Tuesday", "type": "Strength", "activity": "Upper body strength training", "duration": "30 min", "intensity": "Moderate"},
            {"day": "Wednesday", "type": "Cardio", "activity": "Cycling or swimming", "duration": f"{base_cardio_duration} min", "intensity": "Moderate-High"},
            {"day": "Thursday", "type": "Strength", "activity": "Lower body strength training", "duration": "30 min", "intensity": "Moderate"},
            {"day": "Friday", "type": "Cardio", "activity": "HIIT workout", "duration": "20-25 min", "intensity": "High"},
            {"day": "Saturday", "type": "Active Recovery", "activity": "Yoga or light stretching", "duration": "30 min", "intensity": "Low"},
            {"day": "Sunday", "type": "Rest", "activity": "Rest or gentle walk", "duration": "Optional", "intensity": "Low"}
        ]
    elif user.goal == "gain_muscle":
        return [
            {"day": "Monday", "type": "Strength", "activity": "Chest and triceps", "duration": "45-60 min", "intensity": "High"},
            {"day": "Tuesday", "type": "Strength", "activity": "Back and biceps", "duration": "45-60 min", "intensity": "High"},
            {"day": "Wednesday", "type": "Cardio", "activity": "Light cardio", "duration": "20 min", "intensity": "Low-Moderate"},
            {"day": "Thursday", "type": "Strength", "activity": "Legs and core", "duration": "45-60 min", "intensity": "High"},
            {"day": "Friday", "type": "Strength", "activity": "Shoulders and abs", "duration": "45-60 min", "intensity": "High"},
            {"day": "Saturday", "type": "Active Recovery", "activity": "Stretching or yoga", "duration": "30 min", "intensity": "Low"},
            {"day": "Sunday", "type": "Rest", "activity": "Complete rest", "duration": "N/A", "intensity": "N/A"}
        ]
    else:  # maintain or improve_fitness
        return [
            {"day": "Monday", "type": "Cardio", "activity": "Running or cycling", "duration": "30 min", "intensity": "Moderate"},
            {"day": "Tuesday", "type": "Strength", "activity": "Full body workout", "duration": "40 min", "intensity": "Moderate"},
            {"day": "Wednesday", "type": "Flexibility", "activity": "Yoga or Pilates", "duration": "45 min", "intensity": "Low-Moderate"},
            {"day": "Thursday", "type": "Cardio", "activity": "Swimming or elliptical", "duration": "30 min", "intensity": "Moderate"},
            {"day": "Friday", "type": "Strength", "activity": "Circuit training", "duration": "40 min", "intensity": "Moderate-High"},
            {"day": "Saturday", "type": "Recreation", "activity": "Sports or hiking", "duration": "60 min", "intensity": "Variable"},
            {"day": "Sunday", "type": "Rest", "activity": "Light walk or rest", "duration": "Optional", "intensity": "Low"}
        ]

def generate_meal_suggestions(daily_calories: float, macros: dict, dietary_preference: Optional[str]) -> List[dict]:
    """Generate meal suggestions based on calorie needs and dietary preferences"""
    meals = []
    
    breakfast_cals = round(daily_calories * 0.25)
    lunch_cals = round(daily_calories * 0.35)
    dinner_cals = round(daily_calories * 0.30)
    snack_cals = round(daily_calories * 0.10)
    
    if dietary_preference == "vegetarian":
        meals = [
            {
                "meal": "Breakfast",
                "calories": breakfast_cals,
                "suggestions": [
                    "Oatmeal with berries, nuts, and honey",
                    "Greek yogurt parfait with granola and fruit",
                    "Whole grain toast with avocado and eggs"
                ]
            },
            {
                "meal": "Lunch",
                "calories": lunch_cals,
                "suggestions": [
                    "Quinoa bowl with roasted vegetables and chickpeas",
                    "Lentil soup with whole grain bread and salad",
                    "Vegetable stir-fry with tofu and brown rice"
                ]
            },
            {
                "meal": "Dinner",
                "calories": dinner_cals,
                "suggestions": [
                    "Grilled portobello mushroom with sweet potato and greens",
                    "Vegetable curry with paneer and quinoa",
                    "Pasta primavera with olive oil and parmesan"
                ]
            },
            {
                "meal": "Snacks",
                "calories": snack_cals,
                "suggestions": [
                    "Hummus with vegetable sticks",
                    "Mixed nuts and dried fruit",
                    "Apple slices with almond butter"
                ]
            }
        ]
    elif dietary_preference == "vegan":
        meals = [
            {
                "meal": "Breakfast",
                "calories": breakfast_cals,
                "suggestions": [
                    "Smoothie bowl with plant-based protein, fruits, and seeds",
                    "Overnight oats with plant milk, chia seeds, and berries",
                    "Whole grain toast with peanut butter and banana"
                ]
            },
            {
                "meal": "Lunch",
                "calories": lunch_cals,
                "suggestions": [
                    "Buddha bowl with quinoa, chickpeas, and tahini dressing",
                    "Black bean and sweet potato burrito bowl",
                    "Lentil and vegetable soup with whole grain crackers"
                ]
            },
            {
                "meal": "Dinner",
                "calories": dinner_cals,
                "suggestions": [
                    "Tofu stir-fry with vegetables and brown rice",
                    "Vegan chili with cornbread",
                    "Pasta with marinara sauce and nutritional yeast"
                ]
            },
            {
                "meal": "Snacks",
                "calories": snack_cals,
                "suggestions": [
                    "Roasted chickpeas",
                    "Energy balls with dates and nuts",
                    "Vegetable chips with guacamole"
                ]
            }
        ]
    else:  # none, keto, paleo, or default
        meals = [
            {
                "meal": "Breakfast",
                "calories": breakfast_cals,
                "suggestions": [
                    "Scrambled eggs with spinach and whole grain toast",
                    "Protein smoothie with banana, berries, and oats",
                    "Greek yogurt with granola, nuts, and honey"
                ]
            },
            {
                "meal": "Lunch",
                "calories": lunch_cals,
                "suggestions": [
                    "Grilled chicken salad with mixed greens and vinaigrette",
                    "Turkey and avocado wrap with vegetables",
                    "Salmon with quinoa and roasted vegetables"
                ]
            },
            {
                "meal": "Dinner",
                "calories": dinner_cals,
                "suggestions": [
                    "Lean beef or chicken with sweet potato and broccoli",
                    "Baked fish with brown rice and asparagus",
                    "Turkey meatballs with whole wheat pasta and vegetables"
                ]
            },
            {
                "meal": "Snacks",
                "calories": snack_cals,
                "suggestions": [
                    "Protein bar or shake",
                    "Cottage cheese with fruit",
                    "Hard-boiled eggs with cherry tomatoes"
                ]
            }
        ]
    
    return meals

def generate_lifestyle_tips(user: UserHealthInfo) -> List[str]:
    """Generate lifestyle and wellness tips"""
    return [
        "Prioritize 7-9 hours of quality sleep each night",
        "Stay hydrated: drink at least 8 glasses of water daily",
        "Practice stress management techniques (meditation, deep breathing)",
        "Limit screen time, especially before bed",
        "Meal prep on weekends to stay on track during busy weekdays",
        "Find an accountability partner or join a fitness community",
        "Take progress photos and measurements monthly",
        "Celebrate small victories along your journey",
        "Be patient and consistent - sustainable change takes time",
        "Listen to your body and rest when needed"
    ]

def generate_weekly_goals(user: UserHealthInfo, daily_calories: float) -> dict:
    """Generate achievable weekly goals"""
    if user.goal == "lose_weight":
        return {
            "weight": "Aim for 0.5-1 kg weight loss",
            "exercise": "Complete 4-5 workout sessions",
            "nutrition": f"Stay within {daily_calories} calories daily",
            "hydration": "Drink 2-3 liters of water daily",
            "sleep": "Get 7-9 hours of sleep each night",
            "tracking": "Log meals and workouts daily"
        }
    elif user.goal == "gain_muscle":
        return {
            "weight": "Aim for 0.25-0.5 kg muscle gain",
            "exercise": "Complete all scheduled strength training sessions",
            "nutrition": f"Consume {daily_calories} calories with focus on protein",
            "hydration": "Drink 3-4 liters of water daily",
            "sleep": "Get 8-9 hours of sleep for recovery",
            "tracking": "Track workout progress and weights lifted"
        }
    else:
        return {
            "fitness": "Improve endurance or strength by 5%",
            "exercise": "Complete 4-5 diverse workout sessions",
            "nutrition": f"Maintain balanced diet around {daily_calories} calories",
            "hydration": "Drink 2-3 liters of water daily",
            "sleep": "Maintain consistent sleep schedule",
            "tracking": "Monitor energy levels and performance"
        }

# API Endpoints
@app.get("/")
def read_root():
    return {
        "message": "Health Assessment API",
        "version": "1.0.0",
        "endpoints": {
            "/assess": "POST - Submit health information for assessment",
            "/docs": "GET - API documentation"
        }
    }

@app.post("/assess", response_model=PersonalizedPlan)
def assess_health(user_info: UserHealthInfo):
    """
    Assess user health and generate personalized plan
    
    Based on scientifically-backed formulas:
    - BMI calculation (WHO standards)
    - BMR using Mifflin-St Jeor Equation
    - TDEE based on activity levels
    - Macronutrient distribution based on goals
    """
    try:
        # Calculate health metrics
        bmi = calculate_bmi(user_info.weight, user_info.height)
        bmi_category = get_bmi_category(bmi)
        bmr = calculate_bmr(user_info.weight, user_info.height, user_info.age, user_info.gender)
        daily_calories = calculate_daily_calories(bmr, user_info.activity_level, user_info.goal)
        macros = calculate_macros(daily_calories, user_info.goal)
        ideal_weight = calculate_ideal_weight(user_info.height, user_info.gender)
        water_liters = round(user_info.weight * 0.033, 1)  # 33ml per kg body weight
        
        # Generate assessment
        assessment = HealthAssessment(
            bmi=bmi,
            bmi_category=bmi_category,
            bmr=bmr,
            daily_calories=daily_calories,
            protein_grams=macros["protein"],
            carbs_grams=macros["carbs"],
            fats_grams=macros["fats"],
            water_liters=water_liters,
            ideal_weight_range=ideal_weight,
            health_risks=assess_health_risks(bmi, user_info.age, user_info.medical_conditions),
            recommendations=generate_recommendations(user_info, bmi, bmi_category)
        )
        
        # Generate personalized plan
        plan = PersonalizedPlan(
            user_info=user_info,
            assessment=assessment,
            workout_plan=generate_workout_plan(user_info, bmi_category),
            meal_suggestions=generate_meal_suggestions(daily_calories, macros, user_info.dietary_preference),
            lifestyle_tips=generate_lifestyle_tips(user_info),
            weekly_goals=generate_weekly_goals(user_info, daily_calories)
        )
        
        return plan
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing health assessment: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/generate-pdf")
def generate_pdf(plan: PersonalizedPlan):
    """
    Generate a beautiful PDF report from the personalized health plan
    """
    try:
        # HTML template for the PDF
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Health Assessment Report - {{ user_info.name }}</title>
            <style>
                @page {
                    size: A4;
                    margin: 1.5cm;
                }
                
                body {
                    font-family: 'Arial', 'Helvetica', sans-serif;
                    color: #1f2937;
                    line-height: 1.6;
                    margin: 0;
                    padding: 0;
                }
                
                .header {
                    background: linear-gradient(135deg, #0ea5e9 0%, #0369a1 100%);
                    color: white;
                    padding: 30px;
                    margin-bottom: 30px;
                    border-radius: 8px;
                }
                
                .header h1 {
                    margin: 0 0 10px 0;
                    font-size: 32px;
                    font-weight: bold;
                }
                
                .header p {
                    margin: 5px 0;
                    font-size: 14px;
                    opacity: 0.95;
                }
                
                .section {
                    margin-bottom: 25px;
                    page-break-inside: avoid;
                }
                
                .section-title {
                    font-size: 20px;
                    font-weight: bold;
                    color: #0369a1;
                    margin-bottom: 15px;
                    padding-bottom: 8px;
                    border-bottom: 3px solid #0ea5e9;
                }
                
                .metrics-grid {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 15px;
                    margin-bottom: 20px;
                }
                
                .metric-card {
                    background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
                    padding: 15px;
                    border-radius: 8px;
                    border: 2px solid #0ea5e9;
                    text-align: center;
                }
                
                .metric-label {
                    font-size: 11px;
                    color: #075985;
                    font-weight: 600;
                    margin-bottom: 5px;
                    text-transform: uppercase;
                }
                
                .metric-value {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0c4a6e;
                    margin: 5px 0;
                }
                
                .metric-unit {
                    font-size: 11px;
                    color: #075985;
                }
                
                .bmi-badge {
                    display: inline-block;
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-size: 11px;
                    font-weight: bold;
                    margin-top: 5px;
                }
                
                .bmi-normal { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
                .bmi-underweight { background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }
                .bmi-overweight { background: #fed7aa; color: #9a3412; border: 1px solid #fb923c; }
                .bmi-obese { background: #fecaca; color: #991b1b; border: 1px solid #f87171; }
                
                .macros-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 15px;
                    margin-bottom: 20px;
                }
                
                .macro-card {
                    padding: 15px;
                    border-radius: 8px;
                    border: 2px solid;
                    text-align: center;
                }
                
                .macro-protein { background: #dbeafe; border-color: #3b82f6; }
                .macro-carbs { background: #dcfce7; border-color: #22c55e; }
                .macro-fats { background: #fef3c7; border-color: #eab308; }
                
                .macro-card h4 {
                    margin: 0 0 8px 0;
                    font-size: 14px;
                }
                
                .macro-card .value {
                    font-size: 22px;
                    font-weight: bold;
                }
                
                .table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                    font-size: 12px;
                }
                
                .table th {
                    background: #e0f2fe;
                    color: #0c4a6e;
                    padding: 10px;
                    text-align: left;
                    font-weight: bold;
                    border-bottom: 2px solid #0ea5e9;
                }
                
                .table td {
                    padding: 10px;
                    border-bottom: 1px solid #e5e7eb;
                }
                
                .table tr:hover {
                    background: #f9fafb;
                }
                
                .badge {
                    display: inline-block;
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-size: 10px;
                    font-weight: 600;
                }
                
                .badge-cardio { background: #dbeafe; color: #1e40af; }
                .badge-strength { background: #e9d5ff; color: #6b21a8; }
                .badge-rest { background: #e5e7eb; color: #374151; }
                .badge-flexibility { background: #d1fae5; color: #065f46; }
                .badge-active { background: #fef3c7; color: #92400e; }
                .badge-recreation { background: #fce7f3; color: #9f1239; }
                
                .intensity-low { background: #dcfce7; color: #166534; }
                .intensity-moderate { background: #fef3c7; color: #92400e; }
                .intensity-high { background: #fecaca; color: #991b1b; }
                
                .list {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }
                
                .list-item {
                    padding: 10px 10px 10px 35px;
                    margin-bottom: 8px;
                    background: #f0f9ff;
                    border-left: 4px solid #0ea5e9;
                    border-radius: 4px;
                    position: relative;
                    font-size: 13px;
                }
                
                .list-item:before {
                    content: "✓";
                    position: absolute;
                    left: 12px;
                    color: #0ea5e9;
                    font-weight: bold;
                    font-size: 14px;
                }
                
                .risk-item {
                    background: #fef2f2;
                    border-left-color: #ef4444;
                }
                
                .risk-item:before {
                    content: "⚠";
                }
                
                .two-column {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin: 15px 0;
                }
                
                .meal-card {
                    background: #fafafa;
                    padding: 15px;
                    border-radius: 8px;
                    border: 1px solid #e5e7eb;
                    margin-bottom: 15px;
                }
                
                .meal-card h4 {
                    margin: 0 0 10px 0;
                    color: #0369a1;
                    font-size: 14px;
                }
                
                .meal-cal {
                    display: inline-block;
                    background: #e0f2fe;
                    color: #075985;
                    padding: 3px 10px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: bold;
                    margin-left: 10px;
                }
                
                .meal-card ul {
                    margin: 10px 0 0 0;
                    padding-left: 20px;
                    font-size: 12px;
                }
                
                .meal-card li {
                    margin-bottom: 5px;
                    line-height: 1.5;
                }
                
                .goals-grid {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 12px;
                    margin: 15px 0;
                }
                
                .goal-card {
                    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                    padding: 12px;
                    border-radius: 6px;
                    border: 1px solid #bae6fd;
                }
                
                .goal-card h5 {
                    margin: 0 0 5px 0;
                    color: #0c4a6e;
                    font-size: 12px;
                    text-transform: uppercase;
                    font-weight: bold;
                }
                
                .goal-card p {
                    margin: 0;
                    color: #374151;
                    font-size: 12px;
                }
                
                .disclaimer {
                    background: #fef3c7;
                    border: 2px solid #eab308;
                    border-radius: 8px;
                    padding: 15px;
                    margin-top: 30px;
                    font-size: 11px;
                    page-break-inside: avoid;
                }
                
                .disclaimer h4 {
                    margin: 0 0 8px 0;
                    color: #92400e;
                    font-size: 13px;
                }
                
                .disclaimer p {
                    margin: 0;
                    color: #78350f;
                    line-height: 1.5;
                }
                
                .footer {
                    margin-top: 30px;
                    text-align: center;
                    font-size: 11px;
                    color: #6b7280;
                    padding-top: 20px;
                    border-top: 2px solid #e5e7eb;
                }
                
                .ideal-weight {
                    background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
                    padding: 20px;
                    border-radius: 8px;
                    border: 2px solid #22c55e;
                    text-align: center;
                    margin: 15px 0;
                }
                
                .ideal-weight h4 {
                    margin: 0 0 10px 0;
                    color: #166534;
                    font-size: 16px;
                }
                
                .ideal-weight .range {
                    font-size: 28px;
                    font-weight: bold;
                    color: #15803d;
                    margin: 10px 0;
                }
                
                .ideal-weight .current {
                    font-size: 12px;
                    color: #166534;
                }
            </style>
        </head>
        <body>
            <!-- Header -->
            <div class="header">
                <h1>🏥 Health Assessment Report</h1>
                <p><strong>Prepared for:</strong> {{ user_info.name }}</p>
                <p><strong>Date:</strong> {{ report_date }}</p>
                <p><strong>Age:</strong> {{ user_info.age }} years | <strong>Gender:</strong> {{ user_info.gender|capitalize }} | <strong>Goal:</strong> {{ user_info.goal|replace('_', ' ')|title }}</p>
            </div>
            
            <!-- Key Metrics -->
            <div class="section">
                <h2 class="section-title">📊 Key Health Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">BMI</div>
                        <div class="metric-value">{{ "%.1f"|format(assessment.bmi) }}</div>
                        <span class="bmi-badge bmi-{{ assessment.bmi_category|replace(' ', '-')|lower }}">
                            {{ assessment.bmi_category }}
                        </span>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Daily Calories</div>
                        <div class="metric-value">{{ assessment.daily_calories|round|int }}</div>
                        <div class="metric-unit">kcal/day</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">BMR</div>
                        <div class="metric-value">{{ assessment.bmr|round|int }}</div>
                        <div class="metric-unit">kcal/day</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Water Intake</div>
                        <div class="metric-value">{{ "%.1f"|format(assessment.water_liters) }}</div>
                        <div class="metric-unit">liters/day</div>
                    </div>
                </div>
            </div>
            
            <!-- Macronutrients -->
            <div class="section">
                <h2 class="section-title">🥗 Daily Macronutrient Targets</h2>
                <div class="macros-grid">
                    <div class="macro-card macro-protein">
                        <h4>Protein</h4>
                        <div class="value">{{ assessment.protein_grams|round|int }}g</div>
                    </div>
                    <div class="macro-card macro-carbs">
                        <h4>Carbohydrates</h4>
                        <div class="value">{{ assessment.carbs_grams|round|int }}g</div>
                    </div>
                    <div class="macro-card macro-fats">
                        <h4>Fats</h4>
                        <div class="value">{{ assessment.fats_grams|round|int }}g</div>
                    </div>
                </div>
            </div>
            
            <!-- Ideal Weight -->
            <div class="section">
                <h2 class="section-title">⚖️ Ideal Weight Range</h2>
                <div class="ideal-weight">
                    <h4>Healthy Weight Range for Your Height</h4>
                    <div class="range">{{ assessment.ideal_weight_range.min_kg }} - {{ assessment.ideal_weight_range.max_kg }} kg</div>
                    <div class="current">Current Weight: <strong>{{ user_info.weight }} kg</strong></div>
                </div>
            </div>
            
            {% if assessment.health_risks %}
            <!-- Health Risks -->
            <div class="section">
                <h2 class="section-title">⚠️ Health Considerations</h2>
                <ul class="list">
                    {% for risk in assessment.health_risks %}
                    <li class="list-item risk-item">{{ risk }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
            
            <!-- Recommendations -->
            <div class="section">
                <h2 class="section-title">✅ Personalized Recommendations</h2>
                <div class="two-column">
                    {% for rec in assessment.recommendations %}
                    <div class="list-item">{{ rec }}</div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Weekly Goals -->
            <div class="section">
                <h2 class="section-title">🎯 Weekly Goals</h2>
                <div class="goals-grid">
                    {% for key, value in weekly_goals.items() %}
                    <div class="goal-card">
                        <h5>{{ key|replace('_', ' ')|title }}</h5>
                        <p>{{ value }}</p>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Workout Plan -->
            <div class="section">
                <h2 class="section-title">💪 Weekly Workout Plan</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Day</th>
                            <th>Type</th>
                            <th>Activity</th>
                            <th>Duration</th>
                            <th>Intensity</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for workout in workout_plan %}
                        <tr>
                            <td><strong>{{ workout.day }}</strong></td>
                            <td>
                                <span class="badge badge-{{ workout.type|lower|replace(' ', '-') }}">
                                    {{ workout.type }}
                                </span>
                            </td>
                            <td>{{ workout.activity }}</td>
                            <td>{{ workout.duration }}</td>
                            <td>
                                <span class="badge intensity-{{ workout.intensity|lower|replace('-', '')|replace('/', '')|split(' ')|first }}">
                                    {{ workout.intensity }}
                                </span>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            
            <!-- Meal Suggestions -->
            <div class="section">
                <h2 class="section-title">🍽️ Meal Suggestions</h2>
                {% for meal in meal_suggestions %}
                <div class="meal-card">
                    <h4>{{ meal.meal }}<span class="meal-cal">~{{ meal.calories }} kcal</span></h4>
                    <ul>
                        {% for suggestion in meal.suggestions %}
                        <li>{{ suggestion }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% endfor %}
            </div>
            
            <!-- Lifestyle Tips -->
            <div class="section">
                <h2 class="section-title">💡 Lifestyle & Wellness Tips</h2>
                <div class="two-column">
                    {% for tip in lifestyle_tips %}
                    <div class="list-item">{{ tip }}</div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Disclaimer -->
            <div class="disclaimer">
                <h4>⚠️ Important Disclaimer</h4>
                <p>
                    This health assessment is for informational purposes only and does not constitute medical advice. 
                    Always consult with qualified healthcare professionals before making significant changes to your diet, 
                    exercise routine, or lifestyle, especially if you have existing medical conditions or are taking medications.
                </p>
            </div>
            
            <!-- Footer -->
            <div class="footer">
                <p><strong>Health Assessment Application</strong> | Based on WHO standards and evidence-based research</p>
                <p>© 2025 Health Assessment App | Report generated on {{ report_date }}</p>
            </div>
        </body>
        </html>
        """
        
        # Prepare data for template
        template = Template(html_template)
        html_content = template.render(
            user_info=plan.user_info,
            assessment=plan.assessment,
            workout_plan=plan.workout_plan,
            meal_suggestions=plan.meal_suggestions,
            lifestyle_tips=plan.lifestyle_tips,
            weekly_goals=plan.weekly_goals,
            report_date=datetime.now().strftime("%B %d, %Y")
        )
        
        # Generate PDF
        pdf_file = io.BytesIO()
        HTML(string=html_content).write_pdf(pdf_file)
        pdf_file.seek(0)
        
        # Return PDF as response
        return Response(
            content=pdf_file.getvalue(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=health_report_{plan.user_info.name.replace(' ', '_')}.pdf"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
