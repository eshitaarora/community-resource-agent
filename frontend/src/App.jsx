import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import Dashboard from './pages/Dashboard';
import ResourceBrowser from './components/ResourceBrowser';
import UserProfile from './components/UserProfile';
import { Menu, X } from 'lucide-react';

export default function App() {
  const [currentPage, setCurrentPage] = useState('chat');
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-0'} bg-gray-900 text-white transition-all duration-300 overflow-hidden flex flex-col`}>
        <div className="p-4 border-b border-gray-700">
          <h1 className="text-xl font-bold">Community Resource Navigator</h1>
        </div>
        <nav className="flex-1 p-4">
          <button
            onClick={() => setCurrentPage('chat')}
            className={`w-full text-left px-4 py-2 rounded mb-2 ${
              currentPage === 'chat' ? 'bg-blue-600' : 'hover:bg-gray-800'
            }`}
          >
            💬 Chat with AI Agent
          </button>
          <button
            onClick={() => setCurrentPage('resources')}
            className={`w-full text-left px-4 py-2 rounded mb-2 ${
              currentPage === 'resources' ? 'bg-blue-600' : 'hover:bg-gray-800'
            }`}
          >
            🔍 Browse Resources
          </button>
          <button
            onClick={() => setCurrentPage('dashboard')}
            className={`w-full text-left px-4 py-2 rounded mb-2 ${
              currentPage === 'dashboard' ? 'bg-blue-600' : 'hover:bg-gray-800'
            }`}
          >
            📊 Analytics Dashboard
          </button>
          <button
            onClick={() => setCurrentPage('profile')}
            className={`w-full text-left px-4 py-2 rounded mb-2 ${
              currentPage === 'profile' ? 'bg-blue-600' : 'hover:bg-gray-800'
            }`}
          >
            👤 My Profile
          </button>
        </nav>
        <div className="p-4 border-t border-gray-700 text-sm text-gray-400">
          <p>© 2025 Community Resource Navigator</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <div className="bg-white border-b border-gray-200 p-4 flex items-center justify-between">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-gray-100 rounded"
          >
            {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
          <h2 className="text-xl font-bold text-gray-800">
            {currentPage === 'chat' && '💬 Chat with AI Agent'}
            {currentPage === 'resources' && '🔍 Browse Resources'}
            {currentPage === 'dashboard' && '📊 Analytics Dashboard'}
            {currentPage === 'profile' && '👤 My Profile'}
          </h2>
          <div className="w-10"></div>
        </div>

        {/* Page Content */}
        <div className="flex-1 overflow-auto">
          {currentPage === 'chat' && <ChatInterface />}
          {currentPage === 'resources' && <ResourceBrowser />}
          {currentPage === 'dashboard' && <Dashboard />}
          {currentPage === 'profile' && <UserProfile />}
        </div>
      </div>
    </div>
  );
}
