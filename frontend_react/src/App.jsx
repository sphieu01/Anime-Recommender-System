import { useState } from 'react';
import Header from './components/Header';
import MALSearch from './pages/MALSearch';
import ManualImport from './pages/ManualImport';
import './App.css';

function App() {
  // Trạng thái công tắc: 'mal' (mặc định) hoặc 'manual'
  const [importMode, setImportMode] = useState('mal');

  return (
    <div className="layout-container">
      <div className="layout-inner">
        {/* Truyền trạng thái công tắc lên Header */}
        <Header importMode={importMode} setImportMode={setImportMode} />
        
        {/* Render có điều kiện dựa vào Công tắc */}
        <div className="tab-content fade-in">
          {importMode === 'mal' ? <MALSearch /> : <ManualImport />}
        </div>
      </div>
    </div>
  );
}

export default App;