import React, { useEffect, useState } from 'react';
import { analyticsService } from '../services/api';
import { BarChart, LineChart, Users, Activity, Target, TrendingUp, AlertCircle, Loader } from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [userImpact, setUserImpact] = useState(null);
  const [serviceImpact, setServiceImpact] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [daysFilter, setDaysFilter] = useState(30);

  useEffect(() => {
    loadAnalytics();
  }, [daysFilter]);

  const loadAnalytics = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [statsData, userImpactData, serviceImpactData] = await Promise.all([
        analyticsService.getDashboardStats(daysFilter),
        analyticsService.getUserImpact(daysFilter),
        analyticsService.getServiceImpact(daysFilter),
      ]);
      setStats(statsData);
      setUserImpact(userImpactData);
      setServiceImpact(serviceImpactData);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load analytics');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-100">
        <Loader size={50} className="text-blue-600 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-100 border border-red-400 text-red-700 rounded-lg flex items-start gap-3">
        <AlertCircle size={24} className="flex-shrink-0 mt-1" />
        <div>
          <h3 className="font-bold mb-1">Error Loading Analytics</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Impact Dashboard</h1>
          <p className="text-gray-600">Track our community resource navigation impact</p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-gray-700 font-medium">Time Period:</label>
          <select
            value={daysFilter}
            onChange={(e) => setDaysFilter(Number(e.target.value))}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
            <option value={365}>Last year</option>
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Users */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Total Users</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total_users}</p>
              </div>
              <Users size={40} className="text-blue-500" />
            </div>
          </div>

          {/* Conversations */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Total Conversations</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total_conversations}</p>
              </div>
              <Activity size={40} className="text-green-500" />
            </div>
          </div>

          {/* Service Accesses */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Services Accessed</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total_services_accessed}</p>
              </div>
              <Target size={40} className="text-orange-500" />
            </div>
          </div>

          {/* Helpful Rate */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Helpful Response Rate</p>
                <p className="text-3xl font-bold text-gray-900">{stats.helpful_response_rate}%</p>
              </div>
              <TrendingUp size={40} className="text-purple-500" />
            </div>
          </div>
        </div>
      )}

      {/* Main Stats */}
      {stats && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Most Accessed Services */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <BarChart size={24} />
              Top Services
            </h2>
            {stats.most_accessed_services.length > 0 ? (
              <div className="space-y-3">
                {stats.most_accessed_services.slice(0, 5).map((service, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <div className="flex-1">
                      <p className="font-medium text-gray-800">{service.service}</p>
                      <div className="mt-1 bg-gray-200 rounded-full h-2 overflow-hidden">
                        <div
                          className="h-full bg-blue-500"
                          style={{
                            width: `${(service.count / stats.most_accessed_services[0].count) * 100}%`,
                          }}
                        ></div>
                      </div>
                    </div>
                    <span className="ml-4 font-bold text-gray-900">{service.count}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No data available</p>
            )}
          </div>

          {/* Most Requested Categories */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <LineChart size={24} />
              Service Categories
            </h2>
            {stats.most_requested_categories.length > 0 ? (
              <div className="space-y-3">
                {stats.most_requested_categories.slice(0, 5).map((cat, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <div className="flex-1">
                      <p className="font-medium text-gray-800 capitalize">{cat.category}</p>
                      <div className="mt-1 bg-gray-200 rounded-full h-2 overflow-hidden">
                        <div
                          className="h-full bg-green-500"
                          style={{
                            width: `${(cat.count / stats.most_requested_categories[0].count) * 100}%`,
                          }}
                        ></div>
                      </div>
                    </div>
                    <span className="ml-4 font-bold text-gray-900">{cat.count}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No data available</p>
            )}
          </div>
        </div>
      )}

      {/* Engagement Stats */}
      {stats && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Engagement Metrics</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="border-l-4 border-blue-500 pl-4">
              <p className="text-gray-600 text-sm">Unique Services</p>
              <p className="text-2xl font-bold text-gray-900">{stats.unique_services_used}</p>
            </div>
            <div className="border-l-4 border-green-500 pl-4">
              <p className="text-gray-600 text-sm">Avg Messages/User</p>
              <p className="text-2xl font-bold text-gray-900">{stats.average_messages_per_user}</p>
            </div>
            <div className="border-l-4 border-orange-500 pl-4">
              <p className="text-gray-600 text-sm">Total Users</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total_users}</p>
            </div>
            <div className="border-l-4 border-purple-500 pl-4">
              <p className="text-gray-600 text-sm">Total Interactions</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total_conversations}</p>
            </div>
          </div>
        </div>
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 flex items-start gap-4">
        <AlertCircle size={24} className="text-blue-600 flex-shrink-0 mt-1" />
        <div>
          <h3 className="font-bold text-blue-900 mb-2">Impact Dashboard</h3>
          <p className="text-blue-800 text-sm">
            This dashboard tracks our progress in helping vulnerable populations find critical community resources.
            All metrics are updated in real-time as users interact with our AI agent and access services.
          </p>
        </div>
      </div>
    </div>
  );
}
