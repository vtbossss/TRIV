import React, { useEffect, useState } from 'react';

const Weather = () => {
  const [weatherData, setWeatherData] = useState(null);
  const [statusMessage, setStatusMessage] = useState('Waiting for data...');

  useEffect(() => {
    const socket = new WebSocket(`ws://${window.location.hostname}:8000/ws/weather/`);

    socket.onopen = () => {
      console.log('WebSocket connection established');
      setStatusMessage('Connected to server, awaiting weather data...');
    };

    socket.onmessage = (e) => {
      console.log('Message received from WebSocket:', e.data);
      const data = JSON.parse(e.data);

      if (data && data.weather && data.weather.main && data.weather.wind && data.weather.weather && data.weather.dt) {
        const weatherMain = data.weather.main;
        const weatherWind = data.weather.wind;
        const weatherDescription = data.weather.weather[0];
        
        const timestamp = parseFloat(data.weather.dt);
        const formattedTimestamp = !isNaN(timestamp)
          ? new Date(timestamp * 1000).toLocaleString()
          : 'N/A';

        setWeatherData({
          temperature: weatherMain.temp ? (weatherMain.temp - 273.15).toFixed(2) : 'N/A',
          humidity: weatherMain.humidity,
          windSpeed: weatherWind.speed,
          pressure: weatherMain.pressure,
          description: `${weatherDescription.main} (${weatherDescription.description})`,
          timestamp: formattedTimestamp,
        });
      } else {
        setStatusMessage('Received invalid or incomplete data. Please try again later.');
      }
    };

    socket.onclose = () => {
      setStatusMessage('Connection closed. Please try again later.');
    };

    socket.onerror = () => {
      setStatusMessage('Error connecting to the server. Please check your connection.');
    };

    return () => socket.close();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center p-6">
      <div className="mt-6 p-6 rounded-lg bg-white shadow-md w-full max-w-md">
        {weatherData ? (
          <>
            <div className="flex items-center my-2 text-lg">
              <span role="img" aria-label="Temperature" className="text-green-600 mr-2">🌡️</span>
              <strong className="text-green-600 mr-2">Temperature:</strong>
              <span className="font-bold">{weatherData.temperature} °C</span>
            </div>
            <div className="flex items-center my-2 text-lg">
              <span role="img" aria-label="Humidity" className="text-green-600 mr-2">💧</span>
              <strong className="text-green-600 mr-2">Humidity:</strong>
              <span className="font-bold">{weatherData.humidity} %</span>
            </div>
            <div className="flex items-center my-2 text-lg">
              <span role="img" aria-label="Wind Speed" className="text-green-600 mr-2">🌬️</span>
              <strong className="text-green-600 mr-2">Wind Speed:</strong>
              <span className="font-bold">{weatherData.windSpeed} m/s</span>
            </div>
            <div className="flex items-center my-2 text-lg">
              <span role="img" aria-label="Pressure" className="text-green-600 mr-2">⚖️</span>
              <strong className="text-green-600 mr-2">Pressure:</strong>
              <span className="font-bold">{weatherData.pressure} hPa</span>
            </div>
            <div className="flex items-center my-2 text-lg">
              <span role="img" aria-label="Weather" className="text-green-600 mr-2">☁️</span>
              <strong className="text-green-600 mr-2">Weather:</strong>
              <span className="font-bold">{weatherData.description}</span>
            </div>
            <div className="flex items-center my-2 text-lg">
              <span role="img" aria-label="Timestamp" className="text-green-600 mr-2">⏰</span>
              <strong className="text-green-600 mr-2">Timestamp:</strong>
              <span className="font-bold">{weatherData.timestamp}</span>
            </div>
          </>
        ) : (
          <p className="italic text-gray-600">{statusMessage}</p>
        )}
      </div>
    </div>
  );
};

export default Weather;
