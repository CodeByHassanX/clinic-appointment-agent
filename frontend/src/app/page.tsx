'use client';
import { useState, useRef, useEffect } from 'react';

export default function Chatbot() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am your AI Clinic Assistant. I can help you book, reschedule, or cancel appointments. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setIsLoading(true);

    try {
      // Connects to Flowise Cloud API
      const res = await fetch('https://cloud.flowiseai.com/api/v1/prediction/a249af83-0328-4815-a927-d6be49803fe0', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          question: userMessage,
          overrideConfig: {
            sessionId: "demo-session-123"
          }
        })
      });
      
      const data = await res.json();
      const botReply = data.text || data.message || data.error || "Sorry, Flowise returned an empty response.";
      setMessages(prev => [...prev, { role: 'assistant', content: botReply }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Error connecting to the Flowise Cloud server." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-[100dvh] md:min-h-screen bg-gray-50 flex items-center justify-center md:p-4 font-sans text-black">
      <div className="w-full max-w-2xl bg-white md:rounded-2xl shadow-2xl overflow-hidden flex flex-col h-full md:h-[85vh] md:border border-gray-100">
        
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-4 md:p-6 flex items-center gap-3 md:gap-4 shrink-0">
          <div className="w-10 h-10 md:w-12 md:h-12 bg-white rounded-full flex items-center justify-center text-blue-600 font-bold text-lg md:text-xl shadow-md shrink-0">
            AI
          </div>
          <div>
            <h1 className="text-lg md:text-2xl font-bold tracking-tight leading-tight">Synexus Clinic Agent</h1>
            <p className="text-blue-100 text-xs md:text-sm font-medium">Powered by FastAPI, Supabase & n8n</p>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 md:space-y-6 bg-gray-50/50">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] md:max-w-[80%] rounded-2xl p-3 md:p-4 shadow-sm text-sm md:text-base ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-br-none' : 'bg-white border border-gray-100 text-gray-800 rounded-bl-none'}`}>
                {msg.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-100 rounded-2xl rounded-bl-none p-4 shadow-sm flex items-center gap-1.5">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-3 md:p-4 bg-white border-t border-gray-100 shrink-0">
          <form onSubmit={handleSend} className="flex gap-2 md:gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message here..."
              className="flex-1 px-4 md:px-5 py-2.5 md:py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-sm md:text-base text-gray-800 placeholder-gray-400"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-5 md:px-8 py-2.5 md:py-3 bg-blue-600 text-white text-sm md:text-base font-semibold rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg shrink-0"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
