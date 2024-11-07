import './App.css';
import Navbar from './Components/Navbar';
import { Routes, Route } from 'react-router-dom'
import MainHeader from './Pages/MainHeader'
import Home from './Pages/Home'
import DataInfo from './Pages/DataInfo'
import About from './Pages/About'
import Sidebar from './Components/Sidebar'
// import { Router } from 'express';

function App() {
  return (
   <div className='bg-blue-500 h-screen'>
   
      <Navbar />
      
      
      <div className="flex">
        <Sidebar />
      
      </div>
      

     <div className="ml-64 w-full p-8"> {/* Adjusts for sidebar width */}
          <Routes>
          <Route path="/" element={<MainHeader />} />
          <Route index element={<Home />} />
            <Route path="/dataInfo" element={<DataInfo />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </div>
     
   </div>
  );
}

export default App;
