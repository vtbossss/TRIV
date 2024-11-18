import './App.css';
import Navbar from './Components/Navbar';
import { Routes, Route } from 'react-router-dom'
import MainHeader from './Pages/MainHeader'
import Home from './Pages/Home'
import DataInfo from './Pages/DataInfo'
import About from './Pages/About'
import Weather from './Pages/Weather'
import Ndvi from './Pages/Ndvi' 
import Sidebar from './Components/Sidebar'
import { useState } from 'react';
// import { Router } from 'express';

function App() {

  const [isSidebarVisible, setSidebarVisible] = useState(false);

  const toggleSidebar = () => {
    setSidebarVisible(!isSidebarVisible);
  };

  return (
   <div className=' h-screen'>
   
      <Navbar toggleSidebar = {toggleSidebar}/>
      
      
      <div className="flex">
      {isSidebarVisible && <Sidebar /> }
      </div>
      

     <div className=" w-full"> {/* Adjusts for sidebar width */}
          <Routes>
          <Route path="/" element={<MainHeader />} />
          <Route index element={<Home />} />
            <Route path="/dataInfo" element={<DataInfo />} />
            <Route path="/about" element={<About />} />
            <Route path="/weather" element={<Weather />} />
            <Route path="/ndvi" element={<Ndvi />} />
          </Routes>
        </div>
     
   </div>
  );
}

export default App;
