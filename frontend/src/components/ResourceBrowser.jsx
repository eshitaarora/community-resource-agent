import React, { useState, useEffect } from 'react';
import { resourcesService } from '../services/api';
import { useResourceStore } from '../store/index';
import { MapPin, Phone, Globe, Clock, AlertCircle, Loader } from 'lucide-react';

export default function ResourceBrowser() {
  const { resources, selectedResource, isLoading, error, setResources, setSelectedResource, setLoading, setError } =
    useResourceStore();
  const [filter, setFilter] = useState('all');
  const [searchLocation, setSearchLocation] = useState({ latitude: null, longitude: null });

  useEffect(() => {
    loadResources();
  }, []);

  const loadResources = async (category = null) => {
    setLoading(true);
    setError(null);
    try {
      const data = await resourcesService.listResources(category);
      setResources(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load resources');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (category) => {
    setFilter(category);
    loadResources(category === 'all' ? null : category);
  };

  const handleSearchNearby = async () => {
    if (!navigator.geolocation) {
      setError('Geolocation not supported in your browser');
      return;
    }

    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const data = await resourcesService.searchNearby(
            position.coords.latitude,
            position.coords.longitude,
            5
          );
          setSearchLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
          setResources(data);
          setError(null);
        } catch (err) {
          setError(err.response?.data?.detail || 'Failed to search nearby resources');
        } finally {
          setLoading(false);
        }
      },
      () => {
        setError('Unable to access your location. Please enable location services.');
        setLoading(false);
      }
    );
  };

  const categories = ['all', 'shelter', 'food', 'health', 'employment', 'mental_health', 'legal', 'substance_abuse', 'youth'];

  return (
    <div className="flex h-full gap-4 bg-gray-50 rounded-lg overflow-hidden shadow-lg">
      {/* Sidebar - Filters */}
      <div className="w-64 bg-white border-r border-gray-200 p-4 overflow-y-auto">
        <h2 className="text-lg font-bold text-gray-800 mb-4">Filters</h2>

        {/* Location Button */}
        <button
          onClick={handleSearchNearby}
          disabled={isLoading}
          className="w-full mb-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition"
        >
          {isLoading ? 'Loading...' : 'Search Nearby'}
        </button>

        {searchLocation.latitude && (
          <div className="mb-4 p-2 bg-blue-100 rounded text-sm text-blue-700">
            Searching near you
          </div>
        )}

        {/* Category Filter */}
        <div className="space-y-2">
          <h3 className="font-semibold text-gray-700 mb-3">Category</h3>
          {categories.map((cat) => (
            <label key={cat} className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="category"
                value={cat}
                checked={filter === cat}
                onChange={(e) => handleFilterChange(e.target.value)}
                className="rounded"
              />
              <span className="text-gray-600 capitalize">{cat.replace('_', ' ')}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Main Content - Resource List and Details */}
      <div className="flex-1 flex gap-4 p-4 overflow-hidden">
        {/* Resource List */}
        <div className="flex-1 flex flex-col bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div className="p-4 border-b border-gray-200">
            <h2 className="text-lg font-bold text-gray-800">Available Resources</h2>
            <p className="text-sm text-gray-600">{resources.length} services found</p>
          </div>

          {error && (
            <div className="m-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg flex items-start gap-2">
              <AlertCircle size={20} className="flex-shrink-0 mt-0.5" />
              <div>{error}</div>
            </div>
          )}

          {isLoading ? (
            <div className="flex-1 flex items-center justify-center">
              <Loader size={40} className="text-blue-600 animate-spin" />
            </div>
          ) : resources.length === 0 ? (
            <div className="flex-1 flex items-center justify-center text-gray-500">
              <p>No resources found. Try adjusting your filters.</p>
            </div>
          ) : (
            <div className="overflow-y-auto flex-1">
              {resources.map((resource) => (
                <div
                  key={resource.id}
                  onClick={() => setSelectedResource(resource)}
                  className={`p-4 border-b border-gray-100 cursor-pointer transition hover:bg-blue-50 ${
                    selectedResource?.id === resource.id ? 'bg-blue-100' : ''
                  }`}
                >
                  <h3 className="font-semibold text-gray-800">{resource.name}</h3>
                  <p className="text-sm text-gray-600 line-clamp-2">{resource.description}</p>
                  <div className="mt-2 flex items-center gap-4 text-xs text-gray-500">
                    <span className="bg-gray-200 px-2 py-1 rounded capitalize">{resource.category}</span>
                    {resource.distance_miles && (
                      <span className="flex items-center gap-1">
                        <MapPin size={14} />
                        {resource.distance_miles} mi
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Resource Details */}
        {selectedResource && (
          <div className="w-96 bg-white rounded-lg border border-gray-200 p-4 overflow-y-auto shadow">
            <h2 className="text-xl font-bold text-gray-800 mb-4">{selectedResource.name}</h2>

            <p className="text-gray-700 mb-4">{selectedResource.description}</p>

            {/* Category */}
            <div className="mb-4">
              <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium capitalize">
                {selectedResource.category}
              </span>
            </div>

            {/* Address */}
            {selectedResource.address && (
              <div className="mb-4 p-3 bg-gray-50 rounded">
                <div className="flex items-start gap-2 text-gray-700">
                  <MapPin size={18} className="flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-medium">Address</p>
                    <p className="text-sm">{selectedResource.address}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Phone */}
            {selectedResource.phone && (
              <div className="mb-4 p-3 bg-gray-50 rounded">
                <div className="flex items-center gap-2 text-gray-700">
                  <Phone size={18} />
                  <div>
                    <p className="font-medium">Phone</p>
                    <a href={`tel:${selectedResource.phone}`} className="text-blue-600 hover:underline text-sm">
                      {selectedResource.phone}
                    </a>
                  </div>
                </div>
              </div>
            )}

            {/* Website */}
            {selectedResource.website && (
              <div className="mb-4 p-3 bg-gray-50 rounded">
                <div className="flex items-center gap-2 text-gray-700">
                  <Globe size={18} />
                  <div>
                    <p className="font-medium">Website</p>
                    <a href={selectedResource.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline text-sm">
                      Visit Website
                    </a>
                  </div>
                </div>
              </div>
            )}

            {/* Operating Hours */}
            {selectedResource.operating_hours && (
              <div className="mb-4 p-3 bg-gray-50 rounded">
                <div className="flex items-start gap-2 text-gray-700">
                  <Clock size={18} className="flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-medium">Hours</p>
                    <div className="text-sm space-y-1">
                      {Object.entries(selectedResource.operating_hours).map(([day, hours]) => (
                        <div key={day} className="flex justify-between gap-4">
                          <span className="capitalize font-medium">{day}:</span>
                          <span>{hours}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Eligibility */}
            {selectedResource.eligibility_criteria && Object.keys(selectedResource.eligibility_criteria).length > 0 && (
              <div className="mb-4 p-3 bg-yellow-50 rounded">
                <p className="font-medium text-gray-800 mb-2">Eligibility Requirements</p>
                <ul className="text-sm text-gray-700 space-y-1">
                  {Object.entries(selectedResource.eligibility_criteria).map(([key, value]) => (
                    <li key={key}>
                      <span className="font-medium capitalize">{key.replace('_', ' ')}:</span> {String(value)}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Services */}
            {selectedResource.services_provided && selectedResource.services_provided.length > 0 && (
              <div className="mb-4 p-3 bg-green-50 rounded">
                <p className="font-medium text-gray-800 mb-2">Services</p>
                <div className="flex flex-wrap gap-2">
                  {selectedResource.services_provided.map((service, idx) => (
                    <span key={idx} className="bg-green-200 text-green-800 px-2 py-1 rounded text-xs">
                      {service.replace('_', ' ')}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
