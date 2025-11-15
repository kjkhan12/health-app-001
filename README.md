# Health Assessment Application

A comprehensive health assessment tool that provides personalized fitness and nutrition plans based on scientifically-backed formulas and guidelines.

## Features

- **Evidence-Based Calculations**: Uses WHO standards for BMI and Mifflin-St Jeor equation for BMR
- **Personalized Plans**: Customized workout routines and meal suggestions based on your goals
- **Comprehensive Assessment**: Evaluates BMI, BMR, daily calorie needs, and macronutrient distribution
- **Health Risk Analysis**: Identifies potential health risks based on your metrics
- **Beautiful UI**: Professional, responsive design with Tailwind CSS
- **Dietary Preferences**: Support for vegetarian, vegan, keto, and paleo diets

## Technology Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server

### Frontend
- **React 18** - Modern UI library
- **Vite** - Next-generation frontend tooling
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - Promise-based HTTP client

## Scientific Foundation

This application uses evidence-based formulas:

1. **BMI Calculation**: `weight(kg) / height(m)²` - WHO standards
2. **BMR Calculation**: Mifflin-St Jeor Equation
   - Male: `(10 × weight) + (6.25 × height) - (5 × age) + 5`
   - Female: `(10 × weight) + (6.25 × height) - (5 × age) - 161`
3. **TDEE**: BMR × Activity Level Multiplier
4. **Macronutrient Distribution**: Based on fitness goals and latest nutritional science

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```powershell
cd backend
```

2. Create a virtual environment:
```powershell
python -m venv venv
```

3. Activate the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```

4. Install dependencies:
```powershell
pip install -r requirements.txt
```

5. Run the FastAPI server:
```powershell
python main.py
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```powershell
cd frontend
```

2. Install dependencies:
```powershell
npm install
```

3. Start the development server:
```powershell
npm run dev
```

The application will be available at `http://localhost:3000`

## Usage

1. **Start the Backend**: Ensure the FastAPI server is running on port 8000
2. **Start the Frontend**: Launch the React development server on port 3000
3. **Fill the Form**: Enter your health information including:
   - Personal details (name, age, gender)
   - Physical measurements (height, weight)
   - Activity level and fitness goals
   - Dietary preferences
   - Any medical conditions (optional)
4. **Get Your Plan**: Click "Get My Personalized Plan" to receive:
   - Health metrics (BMI, BMR, daily calorie needs)
   - Macronutrient breakdown
   - Weekly workout schedule
   - Meal suggestions
   - Lifestyle recommendations
   - Weekly goals

## API Endpoints

### `GET /`
Returns API information and available endpoints

### `POST /assess`
Submit health information and receive personalized plan

**Request Body:**
```json
{
  "name": "John Doe",
  "age": 30,
  "gender": "male",
  "height": 175,
  "weight": 80,
  "activity_level": "moderately_active",
  "goal": "lose_weight",
  "dietary_preference": "none",
  "medical_conditions": []
}
```

**Response:** Comprehensive health assessment and personalized plan

### `GET /health`
Health check endpoint

## Project Structure

```
health-app/
├── backend/
│   ├── main.py              # FastAPI application with all logic
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── HealthForm.jsx       # User input form
│   │   │   └── ResultsDisplay.jsx   # Results display
│   │   ├── App.jsx          # Main application component
│   │   ├── main.jsx         # Application entry point
│   │   └── index.css        # Tailwind CSS styles
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── tailwind.config.js   # Tailwind configuration
│   └── postcss.config.js    # PostCSS configuration
│
└── README.md
```

## Health Information Sources

The calculations and recommendations in this application are based on:

- World Health Organization (WHO) BMI standards
- Mifflin-St Jeor equation for BMR (most accurate for modern populations)
- American College of Sports Medicine (ACSM) activity level guidelines
- Dietary Guidelines for Americans for macronutrient distribution
- Evidence-based nutrition and exercise science research

## Disclaimer

⚠️ **Important**: This tool provides general health information only and does not constitute medical advice. Always consult with qualified healthcare professionals before making significant changes to your diet, exercise routine, or lifestyle, especially if you have existing medical conditions or are taking medications.

## Development

### Backend Development
- The backend uses FastAPI with automatic API documentation
- Visit `/docs` for interactive Swagger UI
- All health calculations are in `main.py` with detailed comments

### Frontend Development
- React components are in `src/components/`
- Tailwind CSS classes are used for styling
- The app is fully responsive and print-friendly

### Building for Production

**Backend:**
```powershell
# The FastAPI app is production-ready
# Deploy with: uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```powershell
cd frontend
npm run build
# Dist folder will contain production-ready files
```

## Future Enhancements

- User authentication and profile management
- Progress tracking over time
- Integration with fitness trackers
- Meal planning with recipes
- Exercise demonstration videos
- Social features and community support
- Mobile app version

## License

This project is for educational and informational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Built with ❤️ using FastAPI and React**
