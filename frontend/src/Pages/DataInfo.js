import React, { useEffect, useState } from 'react';

const DataInfo = () => {
  const [soilData, setSoilData] = useState(null);
  const [statusMessage, setStatusMessage] = useState('Waiting for data...');

  useEffect(() => {
    const connectWebSocket = () => {
      const socket = new WebSocket(`ws://${window.location.hostname}:8000/ws/agro_data/`);
      
      socket.onopen = () => {
        setStatusMessage('Connected to server, awaiting data...');
      };
      
      socket.onmessage = (e) => {
        // Process data as usual
        socket.onmessage = (e) => {
          console.log('Message received from WebSocket:', e.data);
      
          const data = JSON.parse(e.data);
          if (data && data.data && data.data.data) {
            const soilData = data.data.data;
            let formattedTimestamp = 'N/A';
      
            if (data.data.timestamp) {
              const timestamp = parseFloat(data.data.timestamp);
              if (!isNaN(timestamp)) {
                formattedTimestamp = new Date(timestamp * 1000).toLocaleString();
              }
            }
      
            setSoilData({
              moisture: soilData.moisture,
              t0: soilData.t0,
              t10: soilData.t10,
              timestamp: formattedTimestamp,
            });
          } else {
            setStatusMessage('Received invalid or incomplete data. Please try again later.');
          }
        };
      };
      
      socket.onclose = (e) => {
        console.error('WebSocket closed unexpectedly', e);
        setStatusMessage('Connection closed. Attempting to reconnect...');
        setTimeout(connectWebSocket, 5000);  // Reconnect after 5 seconds
      };
      
      socket.onerror = (e) => {
        console.error('WebSocket error:', e);
        setStatusMessage('Error connecting to the server. Retrying...');
      };
    };
    
    connectWebSocket();
    
    // return () => {
    //   socket.close();
    // };
  }, []);
  

  return (
    <div className="flex flex-col items-center justify-center p-6">
      <div className="mt-6 p-6 rounded-lg bg-white shadow-md w-full max-w-md">
        {soilData ? (
          <>
            <div className="flex items-center my-2 text-lg">
              <span role="img" aria-label="Moisture" className="text-green-600 mr-2">🌱</span>
              <strong className="text-green-600 mr-2">Moisture:</strong>
              <span className="font-bold">{soilData.moisture ?? 'N/A'}</span>
            </div>
            <div className="flex items-center my-2 text-lg">
              <span role="img" aria-label="Temp at 0m" className="text-green-600 mr-2">🌡️</span>
              <strong className="text-green-600 mr-2">Temp at 0m:</strong>
              <span className="font-bold">{soilData.t0 ?? 'N/A'} K</span>
            </div>
            <div className="flex items-center my-2 text-lg">
              <span role="img" aria-label="Temp at 10m" className="text-green-600 mr-2">🌡️</span>
              <strong className="text-green-600 mr-2">Temp at 10m:</strong>
              <span className="font-bold">{soilData.t10 ?? 'N/A'} K</span>
            </div>
            <div className="flex items-center my-2 text-lg">
              <span role="img" aria-label="Timestamp" className="text-green-600 mr-2">⏰</span>
              <strong className="text-green-600 mr-2">Timestamp:</strong>
              <span className="font-bold">{soilData.timestamp}</span>
            </div>
          </>
        ) : (
          <p className="italic text-gray-600">{statusMessage}</p>
        )}
      </div>
    </div>
  );
};

export default DataInfo;
