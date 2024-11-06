import './App.css';
import Navbar from './Components/Navbar';
import { Routes, Route } from 'react-router-dom'
import MainHeader from './Pages/MainHeader'
import Home from './Pages/Home'
import DataInfo from './Pages/DataInfo'
import About from './Pages/About'

function App() {
  return (
   <div className='bg-blue-500 h-screen'>
      <Navbar />

      <Routes>
        <Route path="/" element={<MainHeader />} />
        <Route index element={<Home />} />
        <Route path="/dataInfo" element={<DataInfo />} />
        <Route path="/about" element={<About />} />
     </Routes>
   </div>
  );
}

export default App;
