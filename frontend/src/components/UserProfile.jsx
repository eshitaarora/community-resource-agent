import React from 'react';
import { useUserStore } from '../store/index';
import { MapPin, AlertCircle, Accessibility } from 'lucide-react';

export default function UserProfile() {
  const { location, needs, eligibilityInfo, accessibilityNeeds, setLocation, setNeeds, setEligibilityInfo, setAccessibilityNeeds } =
    useUserStore();

  const handleLocationChange = (e) => {
    setLocation(e.target.value);
  };

  const handleNeedToggle = (need) => {
    const updated = needs.includes(need) ? needs.filter((n) => n !== need) : [...needs, need];
    setNeeds(updated);
  };

  const handleIncomeChange = (e) => {
    setEligibilityInfo({
      ...eligibilityInfo,
      income_level: e.target.value,
    });
  };

  const handleAccessibilityToggle = (need) => {
    const updated = accessibilityNeeds.includes(need) ? accessibilityNeeds.filter((n) => n !== need) : [...accessibilityNeeds, need];
    setAccessibilityNeeds(updated);
  };

  const commonNeeds = ['shelter', 'food', 'health', 'employment', 'mental_health', 'legal', 'substance_abuse', 'childcare'];
  const incomeOptions = ['very_low', 'low', 'moderate', 'medium', 'moderate_high', 'high'];
  const accessibilityOptions = ['mobility', 'visual', 'hearing', 'cognitive', 'language_barrier'];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Your Profile</h2>

      <div className="space-y-6">
        {/* Location */}
        <div>
          <label className="flex items-center gap-2 text-lg font-semibold text-gray-700 mb-3">
            <MapPin size={20} />
            Location
          </label>
          <input
            type="text"
            value={location || ''}
            onChange={handleLocationChange}
            placeholder="Enter your location or address"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p className="text-sm text-gray-500 mt-2">This helps us find resources near you</p>
        </div>

        {/* Needs */}
        <div>
          <label className="block text-lg font-semibold text-gray-700 mb-3">What services do you need?</label>
          <div className="grid grid-cols-2 gap-3">
            {commonNeeds.map((need) => (
              <label key={need} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={needs.includes(need)}
                  onChange={() => handleNeedToggle(need)}
                  className="w-4 h-4 rounded"
                />
                <span className="text-gray-700 capitalize">{need.replace('_', ' ')}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Income Level */}
        <div>
          <label className="block text-lg font-semibold text-gray-700 mb-3">Income Level</label>
          <select
            value={eligibilityInfo?.income_level || ''}
            onChange={handleIncomeChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select income level</option>
            {incomeOptions.map((option) => (
              <option key={option} value={option}>
                {option.replace('_', ' ').toUpperCase()}
              </option>
            ))}
          </select>
          <p className="text-sm text-gray-500 mt-2">This helps determine eligibility for services</p>
        </div>

        {/* Accessibility Needs */}
        <div>
          <label className="flex items-center gap-2 text-lg font-semibold text-gray-700 mb-3">
            <Accessibility size={20} />
            Accessibility Needs
          </label>
          <div className="grid grid-cols-2 gap-3">
            {accessibilityOptions.map((need) => (
              <label key={need} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={accessibilityNeeds.includes(need)}
                  onChange={() => handleAccessibilityToggle(need)}
                  className="w-4 h-4 rounded"
                />
                <span className="text-gray-700 capitalize">{need.replace('_', ' ')}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Info Box */}
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg flex items-start gap-3">
          <AlertCircle size={20} className="text-blue-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-blue-700">
            <p className="font-semibold mb-1">Privacy Notice</p>
            <p>Your information is only used to help match you with relevant services. It's never shared without your consent.</p>
          </div>
        </div>

        {/* Summary */}
        <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-800 mb-3">Your Profile Summary</h3>
          <dl className="space-y-2 text-sm">
            <div>
              <dt className="font-medium text-gray-700">Location:</dt>
              <dd className="text-gray-600">{location || 'Not set'}</dd>
            </div>
            <div>
              <dt className="font-medium text-gray-700">Needs:</dt>
              <dd className="text-gray-600">{needs.length > 0 ? needs.join(', ') : 'Not specified'}</dd>
            </div>
            <div>
              <dt className="font-medium text-gray-700">Income Level:</dt>
              <dd className="text-gray-600 capitalize">{eligibilityInfo?.income_level || 'Not specified'}</dd>
            </div>
            <div>
              <dt className="font-medium text-gray-700">Accessibility Needs:</dt>
              <dd className="text-gray-600">{accessibilityNeeds.length > 0 ? accessibilityNeeds.join(', ') : 'None'}</dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  );
}
