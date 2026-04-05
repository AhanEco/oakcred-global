import { useLocation, Link, Navigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { CheckCircle2, TrendingDown, ArrowRight, Download, Share2 } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function ResultsDashboard() {
  const { state } = useLocation();
  const [animatedScore, setAnimatedScore] = useState(0);
  
  const scoreData = state?.scoreData;

  useEffect(() => {
    if (scoreData) {
      // Animate score from 0 to actual over 1.5s
      const dur = 1500;
      const fps = 60;
      const steps = dur / (1000 / fps);
      const inc = scoreData.score / steps;
      
      let cur = 0;
      const timer = setInterval(() => {
        cur += inc;
        if (cur >= scoreData.score) {
          setAnimatedScore(scoreData.score);
          clearInterval(timer);
        } else {
          setAnimatedScore(Math.floor(cur));
        }
      }, 1000 / fps);
      return () => clearInterval(timer);
    }
  }, [scoreData]);

  if (!scoreData) return <Navigate to="/apply" />;

  const getBandColor = (b) => {
    const m = {
      "PRIME": "text-green-400 border-green-400",
      "NEAR-PRIME": "text-emerald-400 border-emerald-400",
      "SUBPRIME": "text-yellow-400 border-yellow-400",
      "MICRO": "text-orange-400 border-orange-400",
      "THIN-FILE": "text-red-400 border-red-400"
    };
    return m[b] || "text-gray-400 border-gray-400";
  };

  return (
    <div className="min-h-screen pb-20">
      <header className="px-8 py-6 glass-panel border-b-0 sticky top-0 z-50 flex justify-between items-center">
        <div className="text-xl font-display font-bold">INFRA<span className="text-brand-accent">SCOR</span></div>
        <div className="flex gap-4">
          <button className="flex items-center gap-2 px-4 py-2 text-sm text-gray-300 hover:text-white transition"><Download size={16}/> PDF Report</button>
          <button className="flex items-center gap-2 px-4 py-2 text-sm text-gray-300 hover:text-white transition"><Share2 size={16}/> Share</button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto pt-12 px-6 grid md:grid-cols-2 gap-8">
        
        {/* Left Column */}
        <div className="space-y-8">
          
          {/* Main Score Widget */}
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="glass-panel p-8 rounded-3xl text-center relative overflow-hidden"
          >
            <div className="relative inline-flex items-center justify-center mb-6">
               <svg width="240" height="120" viewBox="0 0 240 120" className="overflow-visible">
                  <path d="M 20 120 A 100 100 0 0 1 220 120" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="16" strokeLinecap="round" />
                  <motion.path 
                    d="M 20 120 A 100 100 0 0 1 220 120" 
                    fill="none" 
                    stroke="url(#gradient)" 
                    strokeWidth="16" 
                    strokeLinecap="round" 
                    strokeDasharray="314"
                    initial={{ strokeDashoffset: 314 }}
                    animate={{ strokeDashoffset: 314 - ((animatedScore - 300) / 550) * 314 }}
                    transition={{ duration: 1.5, ease: "easeOut" }}
                  />
                  <defs>
                    <linearGradient id="gradient">
                      <stop offset="0%" stopColor="#ef4444" />
                      <stop offset="50%" stopColor="#eab308" />
                      <stop offset="100%" stopColor="#22c55e" />
                    </linearGradient>
                  </defs>
               </svg>
               <div className="absolute bottom-2 flex flex-col items-center">
                 <span className="text-6xl font-display font-bold tracking-tighter">{animatedScore}</span>
                 <span className="text-sm text-gray-400 mt-1">out of 850</span>
               </div>
            </div>

            <div className={`inline-block px-4 py-1 border rounded-full text-sm font-bold tracking-widest ${getBandColor(scoreData.band)}`}>
               {scoreData.band}
            </div>
            
            <p className="mt-6 text-gray-300">
               Solid alternative data profile. Matches equivalent of CIBIL 700+.
            </p>
          </motion.div>

          {/* Eligibility Card */}
          <div className="glass-panel p-8 rounded-3xl">
            <h3 className="font-bold text-xl mb-6">Loan Eligibility Estimate</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                 <div className="text-sm tracking-wide text-gray-400 uppercase mb-1">Max Amount</div>
                 <div className="text-3xl font-display font-bold">₹{(scoreData.eligibility.max_loan_amount).toLocaleString()}</div>
              </div>
              <div>
                 <div className="text-sm tracking-wide text-gray-400 uppercase mb-1">Interest Est.</div>
                 <div className="text-3xl font-display font-bold text-brand-light">{scoreData.eligibility.interest_rate}</div>
              </div>
            </div>
            <div className="mt-8 pt-6 border-t border-white/10 flex justify-between items-center">
               <div className="text-sm">
                 <span className="text-gray-400">Gov. Guarantee:</span> 
                 <span className={scoreData.eligibility.icgf_eligible ? "text-green-400 ml-2" : "text-gray-400 ml-2"}>
                   {scoreData.eligibility.icgf_eligible ? 'Eligible' : 'Not Eligible'}
                 </span>
               </div>
               <button className="px-6 py-2 bg-white text-black font-semibold rounded-full hover:bg-gray-200 transition">
                 Connect Lenders
               </button>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-8">
          
          {/* Radar Chart */}
          <div className="glass-panel p-6 rounded-3xl h-[360px] flex flex-col">
            <h3 className="font-bold text-xl mb-2 text-center">Score Profile</h3>
            <div className="flex-grow">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="70%" data={scoreData.radar_data}>
                  <PolarGrid stroke="rgba(255,255,255,0.1)" />
                  <PolarAngleAxis dataKey="category" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                  <Radar name="Applicant" dataKey="value" stroke="#C84B9E" fill="#C84B9E" fillOpacity={0.3} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* SHAP Explanations */}
          <div className="space-y-4">
             <h3 className="font-bold text-xl ml-2">What's Helping You</h3>
             {scoreData.shap.positive.map((factor, i) => (
                <div key={i} className="glass-panel p-4 rounded-xl flex items-start gap-4 border-l-4 border-l-green-500">
                  <CheckCircle2 className="text-green-500 mt-1 flex-shrink-0" size={20} />
                  <div>
                    <div className="flex justify-between w-full">
                       <span className="font-bold text-sm text-gray-200">{factor.factor_name}</span>
                       <span className="text-green-400 text-sm font-medium">{factor.score_impact}</span>
                    </div>
                    <p className="text-sm text-gray-400 mt-1">{factor.reason}</p>
                  </div>
                </div>
             ))}

             <h3 className="font-bold text-xl ml-2 mt-8">Areas to Build</h3>
             {scoreData.shap.negative.map((factor, i) => (
                <div key={i} className="glass-panel p-4 rounded-xl flex items-start gap-4 border-l-4 border-l-orange-500">
                  <TrendingDown className="text-orange-500 mt-1 flex-shrink-0" size={20} />
                  <div>
                    <div className="flex justify-between w-full">
                       <span className="font-bold text-sm text-gray-200">{factor.factor_name}</span>
                       <span className="text-orange-400 text-sm font-medium">{factor.score_impact}</span>
                    </div>
                    <p className="text-sm text-gray-400 mt-1">{factor.reason}</p>
                  </div>
                </div>
             ))}
          </div>

        </div>

      </main>
    </div>
  );
}
