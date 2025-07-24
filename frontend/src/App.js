import React, { useState, useEffect, useRef } from "react";
import "./App.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [botConfig, setBotConfig] = useState({
    name: "OT Cavebot",
    auto_heal: true,
    auto_food: true,
    auto_attack: true,
    auto_walk: false,
    auto_loot: true,
    heal_spell: "exura",
    heal_at_hp: 70,
    heal_mana_spell: "exura gran",
    heal_at_mp: 50,
    attack_spell: "exori",
    food_type: "ham",
    food_at: 90,
    waypoints: [],
    waypoint_mode: "loop",
    waypoint_delay: 1000,
    target_creatures: ["rat", "rotworm", "cyclops"],
    loot_items: ["gold coin", "platinum coin", "crystal coin"],
    discard_items: ["leather armor", "studded armor", "chain armor"],
    loot_all_and_filter: true,
    loot_range: 3,
    anti_idle: true,
    emergency_logout_hp: 10,
    enabled: false
  });

  const [botStats, setBotStats] = useState(null);
  const [botStatus, setBotStatus] = useState({ is_running: false, is_paused: false });
  const [currentTab, setCurrentTab] = useState('config');
  const [waypointForm, setWaypointForm] = useState({ name: '', x: '', y: '', description: '' });
  const [sessions, setSessions] = useState([]);
  const ws = useRef(null);

  useEffect(() => {
    loadBotConfig();
    loadBotSessions();
    setupWebSocket();
    
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  const setupWebSocket = () => {
    const wsUrl = BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://');
    ws.current = new WebSocket(`${wsUrl}/api/bot/ws`);
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'stats_update') {
        setBotStats(data.data);
        setBotStatus({
          is_running: data.data.is_running,
          is_paused: data.data.is_paused
        });
      }
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  };

  const loadBotConfig = async () => {
    try {
      const response = await fetch(`${API}/bot/config`);
      const data = await response.json();
      if (data.name) {
        setBotConfig(data);
      }
    } catch (error) {
      console.error('Error loading bot config:', error);
    }
  };

  const loadBotSessions = async () => {
    try {
      const response = await fetch(`${API}/bot/sessions`);
      const data = await response.json();
      setSessions(data.sessions || []);
    } catch (error) {
      console.error('Error loading sessions:', error);
    }
  };

  const saveBotConfig = async () => {
    try {
      const response = await fetch(`${API}/bot/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(botConfig)
      });
      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error('Error saving config:', error);
      alert('Error saving configuration');
    }
  };

  const startBot = async () => {
    try {
      const response = await fetch(`${API}/bot/start`, { method: 'POST' });
      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error('Error starting bot:', error);
      alert('Error starting bot');
    }
  };

  const stopBot = async () => {
    try {
      const response = await fetch(`${API}/bot/stop`, { method: 'POST' });
      const data = await response.json();
      alert(data.message);
      loadBotSessions(); // Reload sessions after stopping
    } catch (error) {
      console.error('Error stopping bot:', error);
      alert('Error stopping bot');
    }
  };

  const pauseBot = async () => {
    try {
      const response = await fetch(`${API}/bot/pause`, { method: 'POST' });
      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error('Error pausing bot:', error);
      alert('Error pausing bot');
    }
  };

  const getCurrentPosition = async () => {
    try {
      const response = await fetch(`${API}/bot/current-position`);
      const data = await response.json();
      setWaypointForm({ 
        ...waypointForm, 
        x: data.x.toString(), 
        y: data.y.toString() 
      });
      alert(`Position captured: ${data.x}, ${data.y}`);
    } catch (error) {
      console.error('Error getting position:', error);
      alert('Error getting current position');
    }
  };

  const addWaypoint = () => {
    if (waypointForm.name && waypointForm.x && waypointForm.y) {
      const newWaypoint = {
        name: waypointForm.name,
        x: parseInt(waypointForm.x),
        y: parseInt(waypointForm.y),
        description: waypointForm.description
      };
      setBotConfig({
        ...botConfig,
        waypoints: [...botConfig.waypoints, newWaypoint]
      });
      setWaypointForm({ name: '', x: '', y: '', description: '' });
    }
  };

  const removeWaypoint = (index) => {
    const newWaypoints = botConfig.waypoints.filter((_, i) => i !== index);
    setBotConfig({ ...botConfig, waypoints: newWaypoints });
  };

  const updateArrayField = (field, value) => {
    const items = value.split(',').map(item => item.trim()).filter(item => item);
    setBotConfig({ ...botConfig, [field]: items });
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-4">
            🏰 OT Cavebot Indetectável
          </h1>
          <p className="text-gray-300 text-lg">Sistema avançado de automação para Open Tibia</p>
        </div>

        {/* Bot Status Dashboard */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 mb-8 border border-purple-500/20">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className={`w-4 h-4 rounded-full ${botStatus.is_running ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
              <span className="text-white font-semibold">
                Status: {botStatus.is_running ? (botStatus.is_paused ? 'Pausado' : 'Executando') : 'Parado'}
              </span>
            </div>
            
            <div className="flex gap-3">
              <button
                onClick={startBot}
                disabled={botStatus.is_running}
                className="px-6 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded-lg font-medium transition-colors"
              >
                ▶️ Iniciar
              </button>
              <button
                onClick={pauseBot}
                disabled={!botStatus.is_running}
                className="px-6 py-2 bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 text-white rounded-lg font-medium transition-colors"
              >
                ⏸️ {botStatus.is_paused ? 'Continuar' : 'Pausar'}
              </button>
              <button
                onClick={stopBot}
                disabled={!botStatus.is_running}
                className="px-6 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white rounded-lg font-medium transition-colors"
              >
                ⏹️ Parar
              </button>
            </div>
          </div>

          {/* Real-time Stats */}
          {botStats && (
            <div className="mt-6 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
              <div className="bg-slate-700/50 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-blue-400">{formatTime(botStats.time_running)}</div>
                <div className="text-xs text-gray-400">Tempo Ativo</div>
              </div>
              <div className="bg-slate-700/50 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-green-400">{botStats.exp_gained}</div>
                <div className="text-xs text-gray-400">EXP Ganha</div>
              </div>
              <div className="bg-slate-700/50 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-red-400">{botStats.heals_used}</div>
                <div className="text-xs text-gray-400">Curas</div>
              </div>
              <div className="bg-slate-700/50 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-yellow-400">{botStats.food_used}</div>
                <div className="text-xs text-gray-400">Comida</div>
              </div>
              <div className="bg-slate-700/50 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-purple-400">{botStats.attacks_made}</div>
                <div className="text-xs text-gray-400">Ataques</div>
              </div>
              <div className="bg-slate-700/50 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-orange-400">{botStats.creatures_killed}</div>
                <div className="text-xs text-gray-400">Mortes</div>
              </div>
              <div className="bg-slate-700/50 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-cyan-400">{botStats.items_looted}</div>
                <div className="text-xs text-gray-400">Lootados</div>
              </div>
              <div className="bg-slate-700/50 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-pink-400">{botStats.items_discarded}</div>
                <div className="text-xs text-gray-400">Descartados</div>
              </div>
            </div>
          )}
        </div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap gap-2 mb-6">
          {[
            { id: 'config', label: '⚙️ Configurações', icon: '⚙️' },
            { id: 'waypoints', label: '🗺️ Waypoints', icon: '🗺️' },
            { id: 'sessions', label: '📊 Sessões', icon: '📊' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setCurrentTab(tab.id)}
              className={`px-6 py-3 rounded-lg font-medium transition-all ${
                currentTab === tab.id
                  ? 'bg-purple-600 text-white shadow-lg'
                  : 'bg-slate-700/50 text-gray-300 hover:bg-slate-600/50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-purple-500/20">
          
          {/* Configuration Tab */}
          {currentTab === 'config' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-white mb-6">⚙️ Configurações do Bot</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Basic Settings */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-purple-400">Configurações Básicas</h3>
                  
                  <div>
                    <label className="block text-gray-300 mb-2">Nome do Bot</label>
                    <input
                      type="text"
                      value={botConfig.name}
                      onChange={(e) => setBotConfig({...botConfig, name: e.target.value})}
                      className="w-full p-3 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-purple-500 focus:outline-none"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={botConfig.auto_heal}
                        onChange={(e) => setBotConfig({...botConfig, auto_heal: e.target.checked})}
                        className="w-5 h-5 text-purple-600"
                      />
                      <span className="text-gray-300">Auto Heal</span>
                    </label>
                    
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={botConfig.auto_food}
                        onChange={(e) => setBotConfig({...botConfig, auto_food: e.target.checked})}
                        className="w-5 h-5 text-purple-600"
                      />
                      <span className="text-gray-300">Auto Food</span>
                    </label>
                    
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={botConfig.auto_attack}
                        onChange={(e) => setBotConfig({...botConfig, auto_attack: e.target.checked})}
                        className="w-5 h-5 text-purple-600"
                      />
                      <span className="text-gray-300">Auto Attack</span>
                    </label>
                    
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={botConfig.auto_loot}
                        onChange={(e) => setBotConfig({...botConfig, auto_loot: e.target.checked})}
                        className="w-5 h-5 text-purple-600"
                      />
                      <span className="text-gray-300">Auto Loot</span>
                    </label>
                  </div>
                </div>

                {/* Spell Settings */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-purple-400">Magias e Cura</h3>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-gray-300 mb-2">Magia de Cura</label>
                      <input
                        type="text"
                        value={botConfig.heal_spell}
                        onChange={(e) => setBotConfig({...botConfig, heal_spell: e.target.value})}
                        className="w-full p-3 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-purple-500 focus:outline-none"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-gray-300 mb-2">Curar em HP (%)</label>
                      <input
                        type="number"
                        value={botConfig.heal_at_hp}
                        onChange={(e) => setBotConfig({...botConfig, heal_at_hp: parseInt(e.target.value)})}
                        className="w-full p-3 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-purple-500 focus:outline-none"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-gray-300 mb-2">Magia de Ataque</label>
                      <input
                        type="text"
                        value={botConfig.attack_spell}
                        onChange={(e) => setBotConfig({...botConfig, attack_spell: e.target.value})}
                        className="w-full p-3 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-purple-500 focus:outline-none"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-gray-300 mb-2">HP Emergência (%)</label>
                      <input
                        type="number"
                        value={botConfig.emergency_logout_hp}
                        onChange={(e) => setBotConfig({...botConfig, emergency_logout_hp: parseInt(e.target.value)})}
                        className="w-full p-3 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-purple-500 focus:outline-none"
                      />
                    </div>
                  </div>
                </div>

                {/* Targeting */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-purple-400">Alvos e Loot</h3>
                  
                  <div>
                    <label className="block text-gray-300 mb-2">Criaturas (separadas por vírgula)</label>
                    <input
                      type="text"
                      value={botConfig.target_creatures.join(', ')}
                      onChange={(e) => updateArrayField('target_creatures', e.target.value)}
                      className="w-full p-3 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-purple-500 focus:outline-none"
                      placeholder="rat, rotworm, cyclops"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-gray-300 mb-2">Itens para Lootar</label>
                    <input
                      type="text"
                      value={botConfig.loot_items.join(', ')}
                      onChange={(e) => updateArrayField('loot_items', e.target.value)}
                      className="w-full p-3 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-purple-500 focus:outline-none"
                      placeholder="gold coin, platinum coin"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-gray-300 mb-2">Itens para Descartar</label>
                    <input
                      type="text"
                      value={botConfig.discard_items.join(', ')}
                      onChange={(e) => updateArrayField('discard_items', e.target.value)}
                      className="w-full p-3 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-purple-500 focus:outline-none"
                      placeholder="leather armor, studded armor"
                    />
                  </div>
                </div>

                {/* Additional Settings */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-purple-400">Configurações Avançadas</h3>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-gray-300 mb-2">Alcance do Loot</label>
                      <input
                        type="number"
                        value={botConfig.loot_range}
                        onChange={(e) => setBotConfig({...botConfig, loot_range: parseInt(e.target.value)})}
                        className="w-full p-3 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-purple-500 focus:outline-none"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-gray-300 mb-2">Delay Waypoint (ms)</label>
                      <input
                        type="number"
                        value={botConfig.waypoint_delay}
                        onChange={(e) => setBotConfig({...botConfig, waypoint_delay: parseInt(e.target.value)})}
                        className="w-full p-3 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-purple-500 focus:outline-none"
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={botConfig.loot_all_and_filter}
                        onChange={(e) => setBotConfig({...botConfig, loot_all_and_filter: e.target.checked})}
                        className="w-5 h-5 text-purple-600"
                      />
                      <span className="text-gray-300">Lootar Tudo e Filtrar (Free Account)</span>
                    </label>
                    
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={botConfig.anti_idle}
                        onChange={(e) => setBotConfig({...botConfig, anti_idle: e.target.checked})}
                        className="w-5 h-5 text-purple-600"
                      />
                      <span className="text-gray-300">Anti-Idle</span>
                    </label>
                  </div>
                </div>
              </div>

              <button
                onClick={saveBotConfig}
                className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-lg font-medium transition-all transform hover:scale-[1.02]"
              >
                💾 Salvar Configurações
              </button>
            </div>
          )}

          {/* Waypoints Tab */}
          {currentTab === 'waypoints' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-white mb-6">🗺️ Gerenciamento de Waypoints</h2>
              
              {/* Add Waypoint Form */}
              <div className="bg-slate-700/50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-purple-400 mb-4">Adicionar Waypoint</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <input
                    type="text"
                    placeholder="Nome do waypoint"
                    value={waypointForm.name}
                    onChange={(e) => setWaypointForm({...waypointForm, name: e.target.value})}
                    className="p-3 bg-slate-600 text-white rounded-lg border border-slate-500 focus:border-purple-500 focus:outline-none"
                  />
                  
                  <input
                    type="text"
                    placeholder="Descrição (opcional)"
                    value={waypointForm.description}
                    onChange={(e) => setWaypointForm({...waypointForm, description: e.target.value})}
                    className="p-3 bg-slate-600 text-white rounded-lg border border-slate-500 focus:border-purple-500 focus:outline-none"
                  />
                  
                  <input
                    type="number"
                    placeholder="Coordenada X"
                    value={waypointForm.x}
                    onChange={(e) => setWaypointForm({...waypointForm, x: e.target.value})}
                    className="p-3 bg-slate-600 text-white rounded-lg border border-slate-500 focus:border-purple-500 focus:outline-none"
                  />
                  
                  <input
                    type="number"
                    placeholder="Coordenada Y"
                    value={waypointForm.y}
                    onChange={(e) => setWaypointForm({...waypointForm, y: e.target.value})}
                    className="p-3 bg-slate-600 text-white rounded-lg border border-slate-500 focus:border-purple-500 focus:outline-none"
                  />
                </div>
                
                <div className="flex gap-3">
                  <button
                    onClick={getCurrentPosition}
                    className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
                  >
                    📍 Capturar Posição Atual
                  </button>
                  
                  <button
                    onClick={addWaypoint}
                    className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
                  >
                    ➕ Adicionar Waypoint
                  </button>
                </div>
              </div>

              {/* Waypoint Mode Selection */}
              <div className="bg-slate-700/50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-purple-400 mb-4">Modo de Movimento</h3>
                
                <div className="flex flex-wrap gap-4 mb-4">
                  {[
                    { value: 'loop', label: '🔄 Loop Contínuo' },
                    { value: 'back_and_forth', label: '↔️ Ida e Volta' },
                    { value: 'once', label: '1️⃣ Uma Vez' }
                  ].map(mode => (
                    <label key={mode.value} className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="radio"
                        name="waypoint_mode"
                        value={mode.value}
                        checked={botConfig.waypoint_mode === mode.value}
                        onChange={(e) => setBotConfig({...botConfig, waypoint_mode: e.target.value})}
                        className="w-4 h-4 text-purple-600"
                      />
                      <span className="text-gray-300">{mode.label}</span>
                    </label>
                  ))}
                </div>
                
                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={botConfig.auto_walk}
                    onChange={(e) => setBotConfig({...botConfig, auto_walk: e.target.checked})}
                    className="w-5 h-5 text-purple-600"
                  />
                  <span className="text-gray-300">🚶 Ativar Auto Walk</span>
                </label>
              </div>

              {/* Waypoints List */}
              <div className="bg-slate-700/50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-purple-400 mb-4">Waypoints Configurados ({botConfig.waypoints.length})</h3>
                
                {botConfig.waypoints.length === 0 ? (
                  <p className="text-gray-400 text-center py-8">Nenhum waypoint configurado</p>
                ) : (
                  <div className="space-y-3">
                    {botConfig.waypoints.map((waypoint, index) => (
                      <div key={index} className="flex items-center justify-between bg-slate-600/50 rounded-lg p-4">
                        <div>
                          <div className="text-white font-medium">{waypoint.name}</div>
                          <div className="text-gray-400 text-sm">
                            X: {waypoint.x}, Y: {waypoint.y}
                            {waypoint.description && ` - ${waypoint.description}`}
                          </div>
                        </div>
                        <button
                          onClick={() => removeWaypoint(index)}
                          className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm transition-colors"
                        >
                          🗑️ Remover
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Sessions Tab */}
          {currentTab === 'sessions' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-white mb-6">📊 Histórico de Sessões</h2>
              
              {sessions.length === 0 ? (
                <p className="text-gray-400 text-center py-8">Nenhuma sessão encontrada</p>
              ) : (
                <div className="space-y-4">
                  {sessions.map((session, index) => (
                    <div key={index} className="bg-slate-700/50 rounded-lg p-6">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h3 className="text-lg font-semibold text-white">Sessão {session.session_id.slice(-8)}</h3>
                          <p className="text-gray-400">
                            {new Date(session.created_at).toLocaleString('pt-BR')}
                          </p>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-blue-400">{formatTime(session.time_running)}</div>
                          <div className="text-sm text-gray-400">Duração</div>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
                        <div className="text-center">
                          <div className="text-xl font-bold text-green-400">{session.exp_gained}</div>
                          <div className="text-xs text-gray-400">EXP</div>
                        </div>
                        <div className="text-center">
                          <div className="text-xl font-bold text-red-400">{session.heals_used}</div>
                          <div className="text-xs text-gray-400">Curas</div>
                        </div>
                        <div className="text-center">
                          <div className="text-xl font-bold text-yellow-400">{session.food_used}</div>
                          <div className="text-xs text-gray-400">Comida</div>
                        </div>
                        <div className="text-center">
                          <div className="text-xl font-bold text-purple-400">{session.attacks_made}</div>
                          <div className="text-xs text-gray-400">Ataques</div>
                        </div>
                        <div className="text-center">
                          <div className="text-xl font-bold text-orange-400">{session.creatures_killed}</div>
                          <div className="text-xs text-gray-400">Mortes</div>
                        </div>
                        <div className="text-center">
                          <div className="text-xl font-bold text-cyan-400">{session.items_looted}</div>
                          <div className="text-xs text-gray-400">Lootados</div>
                        </div>
                        <div className="text-center">
                          <div className="text-xl font-bold text-pink-400">{session.items_discarded}</div>
                          <div className="text-xs text-gray-400">Descartados</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;