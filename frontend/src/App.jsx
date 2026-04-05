import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import ApplicationForm from './pages/ApplicationForm';
import ResultsDashboard from './pages/ResultsDashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-brand-darker font-sans selection:bg-brand-accent selection:text-white">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/apply" element={<ApplicationForm />} />
          <Route path="/results" element={<ResultsDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
