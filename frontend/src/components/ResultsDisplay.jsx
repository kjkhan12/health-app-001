import { useState } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function ResultsDisplay({ results }) {
  const { user_info, assessment, workout_plan, meal_suggestions, lifestyle_tips, weekly_goals } = results
  const [downloading, setDownloading] = useState(false)

  const getBMIColor = (category) => {
    switch (category) {
      case 'Underweight':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'Normal weight':
        return 'text-green-600 bg-green-50 border-green-200'
      case 'Overweight':
        return 'text-orange-600 bg-orange-50 border-orange-200'
      case 'Obese':
        return 'text-red-600 bg-red-50 border-red-200'
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const printResults = () => {
    window.print()
  }

  const downloadPDF = async () => {
    setDownloading(true)
    try {
      const response = await axios.post(`${API_URL}/generate-pdf`, results, {
        responseType: 'blob'
      })
      
      // Create blob link to download
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `health_report_${user_info.name.replace(/\s+/g, '_')}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.parentNode.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Error downloading PDF:', error)
      alert('Failed to generate PDF. Please try again.')
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div className="space-y-8 print:space-y-6">
      {/* Header */}
      <div className="card print:shadow-none">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Health Assessment Results
            </h2>
            <p className="text-gray-600">
              Personalized plan for <span className="font-semibold">{user_info.name}</span>
            </p>
          </div>
          <div className="flex gap-3 print:hidden">
            <button
              onClick={printResults}
              className="btn-secondary"
            >
              <svg className="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Print
            </button>
            <button
              onClick={downloadPDF}
              disabled={downloading}
              className="btn-primary"
            >
              {downloading ? (
                <>
                  <svg className="animate-spin h-5 w-5 inline-block mr-2" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Generating...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Download PDF
                </>
              )}
            </button>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid md:grid-cols-4 gap-4">
          <div className="metric-card">
            <p className="text-sm text-primary-700 font-medium mb-1">BMI</p>
            <p className="text-3xl font-bold text-primary-900">{assessment.bmi}</p>
            <p className={`text-sm font-medium mt-2 px-3 py-1 rounded-full inline-block border ${getBMIColor(assessment.bmi_category)}`}>
              {assessment.bmi_category}
            </p>
          </div>

          <div className="metric-card">
            <p className="text-sm text-primary-700 font-medium mb-1">Daily Calories</p>
            <p className="text-3xl font-bold text-primary-900">{Math.round(assessment.daily_calories)}</p>
            <p className="text-sm text-primary-700 mt-2">kcal/day</p>
          </div>

          <div className="metric-card">
            <p className="text-sm text-primary-700 font-medium mb-1">BMR</p>
            <p className="text-3xl font-bold text-primary-900">{Math.round(assessment.bmr)}</p>
            <p className="text-sm text-primary-700 mt-2">kcal/day</p>
          </div>

          <div className="metric-card">
            <p className="text-sm text-primary-700 font-medium mb-1">Water Intake</p>
            <p className="text-3xl font-bold text-primary-900">{assessment.water_liters}</p>
            <p className="text-sm text-primary-700 mt-2">liters/day</p>
          </div>
        </div>
      </div>

      {/* Macronutrients */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <svg className="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Daily Macronutrient Targets
        </h3>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <p className="text-blue-900 font-semibold mb-2">Protein</p>
            <p className="text-2xl font-bold text-blue-700">{Math.round(assessment.protein_grams)}g</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg border border-green-200">
            <p className="text-green-900 font-semibold mb-2">Carbohydrates</p>
            <p className="text-2xl font-bold text-green-700">{Math.round(assessment.carbs_grams)}g</p>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
            <p className="text-yellow-900 font-semibold mb-2">Fats</p>
            <p className="text-2xl font-bold text-yellow-700">{Math.round(assessment.fats_grams)}g</p>
          </div>
        </div>
      </div>

      {/* Ideal Weight Range */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Ideal Weight Range</h3>
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-lg border border-green-200">
          <p className="text-gray-700 mb-2">Based on your height, your healthy weight range is:</p>
          <p className="text-3xl font-bold text-green-700">
            {assessment.ideal_weight_range.min_kg} - {assessment.ideal_weight_range.max_kg} kg
          </p>
          <p className="text-sm text-gray-600 mt-2">
            Current weight: <span className="font-semibold">{user_info.weight} kg</span>
          </p>
        </div>
      </div>

      {/* Health Risks */}
      {assessment.health_risks.length > 0 && (
        <div className="card">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Health Considerations
          </h3>
          <div className="space-y-2">
            {assessment.health_risks.map((risk, index) => (
              <div key={index} className="flex items-start gap-3 p-3 bg-red-50 rounded-lg border border-red-200">
                <svg className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <p className="text-red-800 text-sm">{risk}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <svg className="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Personalized Recommendations
        </h3>
        <div className="grid md:grid-cols-2 gap-3">
          {assessment.recommendations.map((rec, index) => (
            <div key={index} className="flex items-start gap-3 p-3 bg-primary-50 rounded-lg border border-primary-200">
              <svg className="w-5 h-5 text-primary-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <p className="text-gray-700 text-sm">{rec}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Weekly Goals */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <svg className="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          Weekly Goals
        </h3>
        <div className="grid md:grid-cols-2 gap-4">
          {Object.entries(weekly_goals).map(([key, value]) => (
            <div key={key} className="flex items-start gap-3 p-4 bg-gradient-to-br from-primary-50 to-cyan-50 rounded-lg border border-primary-200">
              <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center flex-shrink-0">
                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <p className="font-semibold text-gray-900 capitalize mb-1">{key.replace('_', ' ')}</p>
                <p className="text-gray-700 text-sm">{value}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Workout Plan */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <svg className="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Weekly Workout Plan
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-primary-100 border-b border-primary-200">
                <th className="text-left p-3 font-semibold text-gray-900">Day</th>
                <th className="text-left p-3 font-semibold text-gray-900">Type</th>
                <th className="text-left p-3 font-semibold text-gray-900">Activity</th>
                <th className="text-left p-3 font-semibold text-gray-900">Duration</th>
                <th className="text-left p-3 font-semibold text-gray-900">Intensity</th>
              </tr>
            </thead>
            <tbody>
              {workout_plan.map((workout, index) => (
                <tr key={index} className="border-b border-gray-200 hover:bg-gray-50">
                  <td className="p-3 font-semibold text-gray-900">{workout.day}</td>
                  <td className="p-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      workout.type === 'Rest' ? 'bg-gray-200 text-gray-700' :
                      workout.type === 'Cardio' ? 'bg-blue-100 text-blue-700' :
                      workout.type === 'Strength' ? 'bg-purple-100 text-purple-700' :
                      'bg-green-100 text-green-700'
                    }`}>
                      {workout.type}
                    </span>
                  </td>
                  <td className="p-3 text-gray-700">{workout.activity}</td>
                  <td className="p-3 text-gray-700">{workout.duration}</td>
                  <td className="p-3">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      workout.intensity === 'Low' || workout.intensity === 'N/A' ? 'bg-green-100 text-green-700' :
                      workout.intensity === 'Moderate' || workout.intensity === 'Low-Moderate' || workout.intensity === 'Moderate-High' ? 'bg-yellow-100 text-yellow-700' :
                      workout.intensity === 'High' ? 'bg-red-100 text-red-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {workout.intensity}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Meal Suggestions */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <svg className="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          Meal Suggestions
        </h3>
        <div className="grid md:grid-cols-2 gap-6">
          {meal_suggestions.map((meal, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4 bg-gradient-to-br from-white to-gray-50">
              <div className="flex justify-between items-center mb-3">
                <h4 className="font-bold text-gray-900">{meal.meal}</h4>
                <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-semibold">
                  ~{meal.calories} kcal
                </span>
              </div>
              <ul className="space-y-2">
                {meal.suggestions.map((suggestion, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                    <svg className="w-4 h-4 text-primary-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    {suggestion}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Lifestyle Tips */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <svg className="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          Lifestyle & Wellness Tips
        </h3>
        <div className="grid md:grid-cols-2 gap-3">
          {lifestyle_tips.map((tip, index) => (
            <div key={index} className="flex items-start gap-3 p-3 bg-gradient-to-br from-cyan-50 to-blue-50 rounded-lg border border-cyan-200">
              <svg className="w-5 h-5 text-cyan-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              <p className="text-gray-700 text-sm">{tip}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Download PDF Section */}
      <div className="card bg-gradient-to-br from-primary-50 via-blue-50 to-cyan-50 border-2 border-primary-300 print:hidden">
        <div className="text-center py-8">
          <div className="w-20 h-20 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-3">
            Save Your Complete Health Report
          </h3>
          <p className="text-gray-700 mb-6 max-w-2xl mx-auto">
            Download your personalized health assessment as a beautifully formatted PDF. 
            Keep it for your records, share it with your healthcare provider, or track your progress over time.
          </p>
          <div className="flex justify-center gap-4">
            <button
              onClick={downloadPDF}
              disabled={downloading}
              className="btn-primary text-lg px-10 py-4 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
            >
              {downloading ? (
                <>
                  <svg className="animate-spin h-6 w-6 inline-block mr-3" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Generating PDF...
                </>
              ) : (
                <>
                  <svg className="w-6 h-6 inline-block mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Download PDF Report
                </>
              )}
            </button>
          </div>
          <p className="text-sm text-gray-600 mt-4">
            📄 Your report includes all metrics, recommendations, workout plans, and meal suggestions
          </p>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="card bg-yellow-50 border-yellow-200">
        <div className="flex items-start gap-3">
          <svg className="w-6 h-6 text-yellow-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <div>
            <h4 className="font-bold text-yellow-900 mb-2">Important Disclaimer</h4>
            <p className="text-yellow-800 text-sm">
              This health assessment is for informational purposes only and does not constitute medical advice. 
              Always consult with qualified healthcare professionals before making significant changes to your diet, 
              exercise routine, or lifestyle, especially if you have existing medical conditions or are taking medications.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ResultsDisplay
