import React, { useState, useEffect } from 'react';
import { MapPin, X } from 'lucide-react';
import { resourcesService } from '../services/api';

export default function LocationSearch({ onLocationSelect, onClose }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [locations, setLocations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Suggested locations for quick access
  const suggestedCities = ['Hyderabad', 'Delhi', 'New Delhi', 'Secunderabad', 'Begumpet', 'Connaught Place'];

  useEffect(() => {
    if (searchQuery.trim().length === 0) {
      setLocations([]);
      return;
    }

    const searchLocations = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const results = await resourcesService.searchLocations(searchQuery);
        setLocations(Array.isArray(results) ? results : []);
      } catch (err) {
        setError('Failed to search locations');
        console.error('Location search error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    const timer = setTimeout(searchLocations, 300);
    return () => clearTimeout(timer);
  }, [searchQuery]);

  const handleLocationClick = (location) => {
    onLocationSelect({
      city: location.city,
      latitude: location.latitude,
      longitude: location.longitude,
      serviceCount: location.service_count
    });
    setSearchQuery('');
    setLocations([]);
  };

  const handleSuggestedCity = async (city) => {
    setSearchQuery(city);
    setIsLoading(true);
    setError(null);
    try {
      const results = await resourcesService.searchLocations(city);
      if (Array.isArray(results) && results.length > 0) {
        handleLocationClick(results[0]);
      }
    } catch (err) {
      setError('Failed to load location');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg p-8 max-w-2xl">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
          <MapPin size={28} className="text-blue-600" />
          Find Services by Location
        </h2>
        <button
          onClick={onClose}
          className="p-2 hover:bg-gray-100 rounded-full transition"
        >
          <X size={24} />
        </button>
      </div>

      {/* Search Input */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">Search for a city:</label>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="e.g., Hyderabad, Delhi, Mumbai..."
          autoFocus
          className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition"
        />
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4">
          {error}
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="flex justify-center items-center h-20">
          <div className="animate-spin">
            <MapPin size={24} className="text-blue-600" />
          </div>
        </div>
      )}

      {/* Search Results */}
      {!isLoading && locations.length > 0 && searchQuery && (
        <div className="mb-6">
          <h3 className="font-semibold text-gray-700 mb-3">Available Locations</h3>
          <div className="space-y-2">
            {locations.map((location, idx) => (
              <button
                key={idx}
                onClick={() => handleLocationClick(location)}
                className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-lg transition"
              >
                <div className="font-medium text-gray-800">{location.city}</div>
                <div className="text-sm text-gray-600">
                  {location.service_count} services available
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Suggested Cities */}
      <div>
        <h3 className="font-semibold text-gray-700 mb-3">Popular Cities</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {suggestedCities.map((city) => (
            <button
              key={city}
              onClick={() => handleSuggestedCity(city)}
              className="px-4 py-2 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded-lg transition font-medium text-sm border border-blue-300"
            >
              {city}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
