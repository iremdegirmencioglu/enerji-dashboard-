import { useState } from 'react';
import './style.css';

function App() {
  const [veri, setVeri] = useState(null);

  const getir = async () => {
    try {
      const res = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=41.01&longitude=28.97&current_weather=true`
      );
      const data = await res.json();
      setVeri(data.current_weather);
    } catch {
      alert("Veri alınamadı");
      setVeri(null);
    }
  };

  return (
    <div className="container">
      <h2>🌤 İstanbul Hava Durumu</h2>
      <button onClick={getir}>Güncel Hava Bilgisini Al</button>

      {veri && (
        <div style={{ marginTop: '1.5rem' }}>
          <p><strong>Sıcaklık:</strong> {veri.temperature} °C</p>
          <p><strong>Rüzgar:</strong> {veri.windspeed} km/s</p>
          <p><strong>Zaman:</strong> {veri.time}</p>
        </div>
      )}
    </div>
  );
}

export default App;
