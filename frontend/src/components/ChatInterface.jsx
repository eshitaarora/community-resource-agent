import React, { useState, useEffect, useRef } from 'react';
import { chatService, resourcesService } from '../services/api';
import { useChatStore, useUserStore } from '../store/index';
import { Send, Copy, ThumbsUp, ThumbsDown, MapPin } from 'lucide-react';
import LocationSearch from './LocationSearch';

export default function ChatInterface() {
  const {
    userId,
    messages,
    isLoading,
    error,
    addMessage,
    setMessages,
    setLoading,
    setError,
  } = useChatStore();

  const { updateContext, location, latitude, longitude } = useUserStore();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const [feedback, setFeedback] = useState({});
  const [showLocationSearch, setShowLocationSearch] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState(null);

  // Load chat history on mount
  useEffect(() => {
    // Skip loading history - start fresh for better UX
    setMessages([]);
  }, [setMessages]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleLocationSelect = (location) => {
    setSelectedLocation(location);
    updateContext({
      location: location.city,
      latitude: location.latitude,
      longitude: location.longitude,
    });
    setShowLocationSearch(false);
    
    // Add a suggestion message
    setInput(`Find shelter nearby ${location.city}`);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message to UI immediately
    addMessage({
      id: Date.now(),
      user_message: input,
      agent_response: '',
      tools_used: [],
      timestamp: new Date().toISOString(),
      pending: true,
    });

    setInput('');
    setLoading(true);
    setError(null);

    try {
      const userContext = { location, latitude, longitude };
      const response = await chatService.sendMessage(userId, input, userContext);

      // Update the last message with the response
      const updatedMessages = [...messages];
      updatedMessages[updatedMessages.length - 1] = {
        ...updatedMessages[updatedMessages.length - 1],
        agent_response: response.message,
        tools_used: response.tools_used || [],
        pending: false,
      };
      setMessages(updatedMessages);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send message');
      // Remove the pending message
      setMessages(messages.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (messageId, helpful) => {
    try {
      await chatService.submitFeedback(messageId, helpful);
      setFeedback({ ...feedback, [messageId]: helpful });
    } catch (err) {
      console.error('Failed to submit feedback:', err);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      {/* Location Search Modal Overlay */}
      {showLocationSearch && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-2xl max-w-2xl w-full mx-4">
            <LocationSearch onLocationSelect={handleLocationSelect} onClose={() => setShowLocationSearch(false)} />
          </div>
        </div>
      )}

      {/* Header */}
      <div className="bg-blue-600 text-white p-4 rounded-t-lg">
        <h2 className="text-xl font-bold">Resource Navigator</h2>
        <p className="text-blue-100 text-sm">Ask about services and resources available in your area</p>
        {selectedLocation && (
          <p className="text-blue-100 text-sm mt-2">📍 Currently viewing: {selectedLocation.city}</p>
        )}
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && !isLoading && (
          <div className="flex items-center justify-center h-full text-center">
            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Welcome!</h3>
              <p className="text-gray-500 mb-4">
                Tell me about what services you're looking for. I can help you find shelter,
                food, healthcare, job training, and other resources.
              </p>
              <button
                onClick={() => setShowLocationSearch(true)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition inline-flex items-center gap-2"
              >
                <MapPin size={20} />
                Choose a Location First
              </button>
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className="space-y-3">
            {/* User Message */}
            <div className="flex justify-end">
              <div className="bg-blue-500 text-white rounded-lg px-4 py-2 max-w-xs lg:max-w-md">
                {msg.user_message}
              </div>
            </div>

            {/* Agent Response */}
            {(msg.agent_response || msg.pending) && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-lg px-4 py-2 max-w-xs lg:max-w-md">
                  {msg.pending ? (
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                    </div>
                  ) : (
                    <>
                      <p className="text-gray-800">{msg.agent_response}</p>
                      {msg.tools_used && msg.tools_used.length > 0 && (
                        <div className="mt-2 pt-2 border-t border-gray-300">
                          <p className="text-xs text-gray-500">
                            Tools used: {msg.tools_used.join(', ')}
                          </p>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>
            )}

            {/* Message Actions */}
            {!msg.pending && msg.agent_response && (
              <div className="flex justify-start gap-2 pl-4">
                <button
                  onClick={() => copyToClipboard(msg.agent_response)}
                  className="p-1 hover:bg-gray-200 rounded transition"
                  title="Copy message"
                >
                  <Copy size={16} className="text-gray-500" />
                </button>
                <button
                  onClick={() => handleFeedback(msg.id, true)}
                  className={`p-1 rounded transition ${
                    feedback[msg.id] === true ? 'bg-green-100' : 'hover:bg-gray-200'
                  }`}
                  title="Helpful"
                >
                  <ThumbsUp size={16} className={feedback[msg.id] === true ? 'text-green-600' : 'text-gray-500'} />
                </button>
                <button
                  onClick={() => handleFeedback(msg.id, false)}
                  className={`p-1 rounded transition ${
                    feedback[msg.id] === false ? 'bg-red-100' : 'hover:bg-gray-200'
                  }`}
                  title="Not helpful"
                >
                  <ThumbsDown size={16} className={feedback[msg.id] === false ? 'text-red-600' : 'text-gray-500'} />
                </button>
              </div>
            )}
          </div>
        ))}

        <div ref={messagesEndRef} />
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md mx-4 mb-4">
          {error}
        </div>
      )}

      {/* Input Form */}
      <form onSubmit={handleSendMessage} className="p-4 border-t border-gray-200 space-y-3">
        {/* Quick action buttons */}
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setShowLocationSearch(true)}
            className="bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded-lg transition flex items-center gap-2 text-sm font-medium"
          >
            <MapPin size={16} />
            Choose Location
          </button>
        </div>
        
        {/* Input and send button */}
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about services you need... (e.g., 'Find shelter nearby')"
            disabled={isLoading}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition flex items-center gap-2"
          >
            <Send size={20} />
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
