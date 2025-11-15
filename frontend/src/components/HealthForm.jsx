import { useState } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function HealthForm({ setResults, loading, setLoading }) {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    gender: 'male',
    height: '',
    weight: '',
    activity_level: 'moderately_active',
    goal: 'maintain',
    dietary_preference: 'none',
    medical_conditions: []
  })

  const [errors, setErrors] = useState({})
  const [medicalConditionInput, setMedicalConditionInput] = useState('')

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const addMedicalCondition = () => {
    if (medicalConditionInput.trim()) {
      setFormData(prev => ({
        ...prev,
        medical_conditions: [...prev.medical_conditions, medicalConditionInput.trim()]
      }))
      setMedicalConditionInput('')
    }
  }

  const removeMedicalCondition = (index) => {
    setFormData(prev => ({
      ...prev,
      medical_conditions: prev.medical_conditions.filter((_, i) => i !== index)
    }))
  }

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.name.trim()) newErrors.name = 'Name is required'
    if (!formData.age || formData.age < 1 || formData.age > 120) {
      newErrors.age = 'Age must be between 1 and 120'
    }
    if (!formData.height || formData.height <= 0) {
      newErrors.height = 'Please enter a valid height'
    }
    if (!formData.weight || formData.weight <= 0) {
      newErrors.weight = 'Please enter a valid weight'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    setLoading(true)
    
    try {
      const submitData = {
        ...formData,
        age: parseInt(formData.age),
        height: parseFloat(formData.height),
        weight: parseFloat(formData.weight),
        medical_conditions: formData.medical_conditions.length > 0 ? formData.medical_conditions : null
      }

      const response = await axios.post(`${API_URL}/assess`, submitData)
      setResults(response.data)
    } catch (error) {
      console.error('Error submitting form:', error)
      alert('An error occurred while processing your request. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="card max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Health Information</h2>
      
      {/* Basic Information */}
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <label className="label-text">
            Full Name <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className={`input-field ${errors.name ? 'border-red-500' : ''}`}
            placeholder="John Doe"
          />
          {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
        </div>

        <div>
          <label className="label-text">
            Age (years) <span className="text-red-500">*</span>
          </label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            className={`input-field ${errors.age ? 'border-red-500' : ''}`}
            placeholder="30"
            min="1"
            max="120"
          />
          {errors.age && <p className="text-red-500 text-sm mt-1">{errors.age}</p>}
        </div>
      </div>

      {/* Physical Measurements */}
      <div className="grid md:grid-cols-3 gap-6 mb-6">
        <div>
          <label className="label-text">
            Gender <span className="text-red-500">*</span>
          </label>
          <select
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            className="input-field"
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div>
          <label className="label-text">
            Height (cm) <span className="text-red-500">*</span>
          </label>
          <input
            type="number"
            name="height"
            value={formData.height}
            onChange={handleChange}
            className={`input-field ${errors.height ? 'border-red-500' : ''}`}
            placeholder="170"
            step="0.1"
          />
          {errors.height && <p className="text-red-500 text-sm mt-1">{errors.height}</p>}
        </div>

        <div>
          <label className="label-text">
            Weight (kg) <span className="text-red-500">*</span>
          </label>
          <input
            type="number"
            name="weight"
            value={formData.weight}
            onChange={handleChange}
            className={`input-field ${errors.weight ? 'border-red-500' : ''}`}
            placeholder="70"
            step="0.1"
          />
          {errors.weight && <p className="text-red-500 text-sm mt-1">{errors.weight}</p>}
        </div>
      </div>

      {/* Activity and Goals */}
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <label className="label-text">
            Activity Level <span className="text-red-500">*</span>
          </label>
          <select
            name="activity_level"
            value={formData.activity_level}
            onChange={handleChange}
            className="input-field"
          >
            <option value="sedentary">Sedentary (little or no exercise)</option>
            <option value="lightly_active">Lightly Active (1-3 days/week)</option>
            <option value="moderately_active">Moderately Active (3-5 days/week)</option>
            <option value="very_active">Very Active (6-7 days/week)</option>
            <option value="extra_active">Extra Active (athlete/physical job)</option>
          </select>
        </div>

        <div>
          <label className="label-text">
            Primary Goal <span className="text-red-500">*</span>
          </label>
          <select
            name="goal"
            value={formData.goal}
            onChange={handleChange}
            className="input-field"
          >
            <option value="lose_weight">Lose Weight</option>
            <option value="maintain">Maintain Current Weight</option>
            <option value="gain_muscle">Gain Muscle</option>
            <option value="improve_fitness">Improve Overall Fitness</option>
          </select>
        </div>
      </div>

      {/* Dietary Preference */}
      <div className="mb-6">
        <label className="label-text">Dietary Preference</label>
        <select
          name="dietary_preference"
          value={formData.dietary_preference}
          onChange={handleChange}
          className="input-field"
        >
          <option value="none">No Specific Preference</option>
          <option value="vegetarian">Vegetarian</option>
          <option value="vegan">Vegan</option>
          <option value="keto">Keto</option>
          <option value="paleo">Paleo</option>
        </select>
      </div>

      {/* Medical Conditions */}
      <div className="mb-6">
        <label className="label-text">Medical Conditions (Optional)</label>
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={medicalConditionInput}
            onChange={(e) => setMedicalConditionInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addMedicalCondition())}
            className="input-field"
            placeholder="e.g., Diabetes, Hypertension"
          />
          <button
            type="button"
            onClick={addMedicalCondition}
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg font-medium transition-colors"
          >
            Add
          </button>
        </div>
        {formData.medical_conditions.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {formData.medical_conditions.map((condition, index) => (
              <span
                key={index}
                className="inline-flex items-center gap-2 bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm"
              >
                {condition}
                <button
                  type="button"
                  onClick={() => removeMedicalCondition(index)}
                  className="text-red-600 hover:text-red-800"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Submit Button */}
      <div className="flex justify-center">
        <button
          type="submit"
          disabled={loading}
          className="btn-primary text-lg px-12 py-4"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Analyzing...
            </span>
          ) : (
            'Get My Personalized Plan'
          )}
        </button>
      </div>

      <p className="text-center text-gray-500 text-sm mt-4">
        All fields marked with <span className="text-red-500">*</span> are required
      </p>
    </form>
  )
}

export default HealthForm
