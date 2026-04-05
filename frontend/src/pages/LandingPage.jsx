import { Link } from 'react-router-dom';
import { ArrowRight, ShieldCheck, Activity, Users } from 'lucide-react';
import { motion } from 'framer-motion';

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-8 py-6 flex justify-between items-center glass-panel border-b-0 sticky top-0 z-50">
        <div className="text-2xl font-display font-bold tracking-tight">
          INFRA<span className="text-brand-accent">SCOR</span>
        </div>
        <nav className="space-x-6 text-sm font-medium">
          <a href="#how" className="hover:text-brand-light transition">How it Works</a>
          <button className="px-4 py-2 border border-white/20 rounded-full hover:bg-white/5 transition">
            Bank Portal
          </button>
        </nav>
      </header>

      <main className="flex-grow">
        {/* Hero Section */}
        <section className="relative px-8 pt-32 pb-24 max-w-7xl mx-auto overflow-hidden">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-brand-dark rounded-full blur-[120px] opacity-50 pointer-events-none"></div>
          
          <div className="relative z-10 max-w-3xl">
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-6xl md:text-7xl font-display font-bold leading-tight mb-6"
            >
              Your Work is Your <br/>
              <span className="gradient-text">Credit Score</span>
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-xl text-gray-400 mb-10 max-w-2xl"
            >
              Unlocking the formal economy for India's unorganized sector. We use your digital footprint, utility payments, and trade activity to generate a verifiable financial identity.
            </motion.p>
            
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="flex gap-4"
            >
              <Link to="/apply" className="px-8 py-4 bg-brand-accent text-white font-medium rounded-full hover:bg-pink-600 transition flex items-center gap-2">
                Apply Now <ArrowRight size={18} />
              </Link>
              <button className="px-8 py-4 glass-panel font-medium rounded-full hover:bg-white/5 transition">
                Business Assessment
              </button>
            </motion.div>
          </div>
        </section>

        {/* Stats Strip */}
        <section className="border-y border-white/10 bg-black/20">
          <div className="max-w-7xl mx-auto px-8 py-12 flex flex-wrap justify-between gap-8 text-center md:text-left">
            <div>
              <div className="text-4xl font-display font-bold text-brand-light mb-2">400M+</div>
              <div className="text-sm text-gray-400">Potential Beneficiaries</div>
            </div>
            <div>
              <div className="text-4xl font-display font-bold text-brand-light mb-2">₹87L Cr</div>
              <div className="text-sm text-gray-400">Informal Economy Value</div>
            </div>
            <div>
              <div className="text-4xl font-display font-bold text-brand-light mb-2">93%</div>
              <div className="text-sm text-gray-400">India's Workforce</div>
            </div>
            <div>
              <div className="text-4xl font-display font-bold text-brand-light mb-2">0</div>
              <div className="text-sm text-gray-400">CIBIL Score Required</div>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section id="how" className="max-w-7xl mx-auto px-8 py-32">
          <h2 className="text-4xl font-display font-bold mb-16 text-center">How INFRASCOR Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="glass-panel p-8 rounded-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 text-white/5 group-hover:text-brand-accent/20 transition duration-500">
                <Activity size={100} strokeWidth={1} />
              </div>
              <div className="w-12 h-12 bg-white/10 rounded-full flex items-center justify-center mb-6 text-brand-light">1</div>
              <h3 className="text-xl font-bold mb-4">Connect Your Data</h3>
              <p className="text-gray-400">Link your UPI, utility bills, and basic assets. No formal income statements needed.</p>
            </div>
            <div className="glass-panel p-8 rounded-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 text-white/5 group-hover:text-brand-accent/20 transition duration-500">
                <ShieldCheck size={100} strokeWidth={1} />
              </div>
              <div className="w-12 h-12 bg-white/10 rounded-full flex items-center justify-center mb-6 text-brand-light">2</div>
              <h3 className="text-xl font-bold mb-4">Get AI Scored</h3>
              <p className="text-gray-400">Our machine learning models translate your behavior into a trusted 300-850 credit band.</p>
            </div>
            <div className="glass-panel p-8 rounded-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 text-white/5 group-hover:text-brand-accent/20 transition duration-500">
                <Users size={100} strokeWidth={1} />
              </div>
              <div className="w-12 h-12 bg-white/10 rounded-full flex items-center justify-center mb-6 text-brand-light">3</div>
              <h3 className="text-xl font-bold mb-4">Access Capital</h3>
              <p className="text-gray-400">Match with banks, NBFCs, and MFIs instantly based on your true repayment capacity.</p>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-white/10 py-8 px-8 text-center text-sm text-gray-500">
        Empowering India's Next Billion. Built for policy impact.
      </footer>
    </div>
  );
}
