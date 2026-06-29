import { useEffect } from 'react'

export default function LandingPage({ onEnter }) {
  useEffect(() => {
    document.title = 'SPANDAN AI — स्पन्दन | India\'s Pulse'
  }, [])

  return (
    <div style={{fontFamily:"'Inter',sans-serif",background:'#0a0a12',color:'#f0ede6',overflowX:'hidden'}}>

      {/* ── Logo Section ── */}
      <div style={{display:'flex',flexDirection:'column',alignItems:'center',padding:'3rem 2rem 2rem',background:'linear-gradient(180deg,#0a0412 0%,#0a0a12 100%)',borderBottom:'1px solid #1e1a2e',position:'relative',overflow:'hidden'}}>

        {/* Mandala background */}
        <svg style={{position:'absolute',top:'50%',left:'50%',transform:'translate(-50%,-50%)',width:400,height:400,opacity:0.04,pointerEvents:'none'}} viewBox="0 0 400 400">
          <g transform="translate(200,200)" stroke="#FF6B00" fill="none" strokeWidth="0.5">
            <circle r="180"/><circle r="150"/><circle r="120"/><circle r="90"/><circle r="60"/><circle r="30"/>
            <line x1="-180" y1="0" x2="180" y2="0"/><line x1="0" y1="-180" x2="0" y2="180"/>
            <line x1="-127" y1="-127" x2="127" y2="127"/><line x1="127" y1="-127" x2="-127" y2="127"/>
          </g>
        </svg>

        {/* Logo mark */}
        <div style={{position:'relative',width:90,height:90,marginBottom:'1.5rem'}}>
          {[90,70,50].map((s,i)=>(
            <div key={i} style={{position:'absolute',borderRadius:'50%',border:'1.5px solid #FF6B00',top:'50%',left:'50%',transform:'translate(-50%,-50%)',width:s,height:s,opacity:[0.3,0.5,0.7][i]}}/>
          ))}
          <svg style={{position:'absolute',top:'50%',left:'50%',transform:'translate(-50%,-50%)',width:100,height:40}} viewBox="0 0 100 40">
            <polyline points="0,20 15,20 22,8 28,32 35,5 42,35 48,20 58,20 65,12 72,28 78,20 100,20" fill="none" stroke="#FF6B00" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <div style={{position:'absolute',width:8,height:8,background:'#FF6B00',borderRadius:'50%',top:'50%',left:'50%',transform:'translate(-50%,-50%)',boxShadow:'0 0 12px #FF6B00'}}/>
        </div>

        <div style={{fontFamily:"'Cinzel',serif",fontSize:'2.8rem',fontWeight:700,letterSpacing:'0.15em',background:'linear-gradient(135deg,#FF6B00 0%,#E8A020 50%,#F5C842 100%)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent',backgroundClip:'text',marginBottom:'0.2rem'}}>
          SPANDAN
        </div>
        <div style={{fontFamily:"'Cinzel',serif",fontSize:'1rem',color:'#8a8070',letterSpacing:'0.3em',marginBottom:'0.8rem'}}>
          स्पन्दन &nbsp;·&nbsp; AI
        </div>
        <div style={{fontSize:'0.85rem',color:'#4DDBBC',letterSpacing:'0.2em',textTransform:'uppercase'}}>
          भारत की धड़कन &nbsp;·&nbsp; India's Pulse
        </div>
        <div style={{width:80,height:1,background:'linear-gradient(90deg,transparent,#FF6B00,transparent)',margin:'1.5rem auto 0'}}/>
      </div>

      {/* ── Nav ── */}
      <nav style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'1rem 2rem',borderBottom:'0.5px solid #1e1a2e',background:'#0a0a12',flexWrap:'wrap',gap:'0.5rem'}}>
        <div style={{fontFamily:"'Cinzel',serif",fontSize:'1.3rem',fontWeight:700,background:'linear-gradient(135deg,#FF6B00,#E8A020)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent',backgroundClip:'text',letterSpacing:'0.12em'}}>
          SPANDAN AI
        </div>
        <div style={{display:'flex',gap:'1.5rem'}}>
          {['How it works','For whom','Impact','Schemes'].map(l=>(
            <span key={l} style={{fontSize:'0.82rem',color:'#8a8070',letterSpacing:'0.08em',textTransform:'uppercase',cursor:'pointer'}}>{l}</span>
          ))}
        </div>
        <button onClick={onEnter} style={{background:'#FF6B00',color:'white',border:'none',padding:'0.5rem 1.2rem',borderRadius:4,fontSize:'0.82rem',fontWeight:500,letterSpacing:'0.08em',cursor:'pointer'}}>
          Get started ↗
        </button>
      </nav>

      {/* ── Hero ── */}
      <section style={{padding:'4rem 2rem 3rem',textAlign:'center'}}>
        <div style={{fontSize:'0.75rem',letterSpacing:'0.3em',textTransform:'uppercase',color:'#00C9A7',marginBottom:'1.5rem',display:'flex',alignItems:'center',justifyContent:'center',gap:'0.8rem'}}>
          <span style={{width:30,height:1,background:'#00C9A7',opacity:0.5,display:'inline-block'}}/>
          AI · Location Intelligence · India
          <span style={{width:30,height:1,background:'#00C9A7',opacity:0.5,display:'inline-block'}}/>
        </div>
        <h1 style={{fontFamily:"'Cinzel',serif",fontSize:'2.4rem',fontWeight:600,lineHeight:1.3,color:'#F5EDD8',marginBottom:'0.5rem',letterSpacing:'0.05em'}}>
          Every Corner of India<br/>
          <span style={{background:'linear-gradient(135deg,#FF6B00,#F5C842)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent',backgroundClip:'text'}}>
            Holds an Opportunity
          </span>
        </h1>
        <p style={{fontFamily:"'Cinzel',serif",fontSize:'1rem',color:'#8a8070',marginBottom:'1.5rem',letterSpacing:'0.08em'}}>
          We find it. We show it. You build it.
        </p>
        <p style={{fontSize:'0.95rem',color:'#9a9280',maxWidth:500,margin:'0 auto 2.5rem',lineHeight:1.8,fontWeight:300}}>
          SPANDAN AI reads the pulse of every pin code in India — identifying business gaps, matching the right opportunity to the right person, and guiding them from idea to income.
        </p>
        <div style={{display:'flex',gap:'1rem',justifyContent:'center',flexWrap:'wrap'}}>
          <button onClick={onEnter} style={{background:'linear-gradient(135deg,#FF6B00,#E8A020)',color:'white',border:'none',padding:'0.8rem 2rem',borderRadius:4,fontSize:'0.88rem',fontWeight:500,letterSpacing:'0.08em',cursor:'pointer',textTransform:'uppercase'}}>
            Find My Opportunity ↗
          </button>
          <button onClick={onEnter} style={{background:'transparent',color:'#F5EDD8',border:'0.5px solid #3a3040',padding:'0.8rem 2rem',borderRadius:4,fontSize:'0.88rem',letterSpacing:'0.08em',cursor:'pointer',textTransform:'uppercase'}}>
            See How It Works
          </button>
        </div>
      </section>

      {/* ── Stats ── */}
      <section style={{padding:'2.5rem 2rem',background:'#0a0a12'}}>
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(130px,1fr))',gap:1,background:'#1a1628',border:'1px solid #1a1628',borderRadius:8,overflow:'hidden',maxWidth:640,margin:'0 auto'}}>
          {[['19K+','Pin codes scanned'],['63M','MSMEs in India'],['Rs.0','Cost to find'],['22','Indian languages']].map(([n,l])=>(
            <div key={l} style={{background:'#0d0d1a',padding:'1.5rem 1rem',textAlign:'center'}}>
              <span style={{fontFamily:"'Cinzel',serif",fontSize:'1.8rem',fontWeight:700,background:'linear-gradient(135deg,#FF6B00,#E8A020)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent',backgroundClip:'text',display:'block',marginBottom:'0.3rem'}}>{n}</span>
              <span style={{fontSize:'0.72rem',color:'#8a8070',letterSpacing:'0.12em',textTransform:'uppercase',lineHeight:1.4}}>{l}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── How it works ── */}
      <section style={{padding:'3rem 2rem',background:'#06060f',borderTop:'0.5px solid #1a1628'}}>
        <h2 style={{fontFamily:"'Cinzel',serif",fontSize:'1.3rem',fontWeight:600,color:'#F5EDD8',textAlign:'center',marginBottom:'0.5rem',letterSpacing:'0.1em'}}>How SPANDAN Works</h2>
        <p style={{fontSize:'0.82rem',color:'#8a8070',textAlign:'center',marginBottom:'2.5rem',letterSpacing:'0.08em'}}>कैसे काम करता है · From pulse to prosperity</p>
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(140px,1fr))',gap:'1rem',maxWidth:640,margin:'0 auto'}}>
          {[
            ['STEP 01','📍','Share location','Tell us where you are. GPS auto-detects your pin code anywhere in India.'],
            ['STEP 02','💰','Share capital','From Rs.5,000 to Rs.50 lakh — every level gets the right opportunity.'],
            ['STEP 03','🧠','AI reads pulse','SPANDAN scans 10+ data sources — census, maps, delivery data, finance.'],
            ['STEP 04','🎯','Your opportunity','Exact location, exact business, exact revenue estimate. No guessing.'],
            ['STEP 05','💳','Funding match','MUDRA, PM SVANidhi, PMEGP — AI finds your best scheme instantly.'],
            ['STEP 06','🏪','Start business','Complete setup guide, shop design, first week action plan. Begin.'],
          ].map(([num,icon,title,desc])=>(
            <div key={num} style={{background:'#0d0d1a',border:'0.5px solid #1e1a2e',borderRadius:8,padding:'1.5rem 1rem',textAlign:'center'}}>
              <div style={{fontFamily:"'Cinzel',serif",fontSize:'0.7rem',color:'#FF6B00',letterSpacing:'0.2em',marginBottom:'0.8rem',opacity:0.7}}>{num}</div>
              <div style={{fontSize:'1.8rem',marginBottom:'0.8rem'}}>{icon}</div>
              <div style={{fontSize:'0.88rem',fontWeight:500,color:'#F5EDD8',marginBottom:'0.5rem',letterSpacing:'0.05em'}}>{title}</div>
              <div style={{fontSize:'0.75rem',color:'#8a8070',lineHeight:1.6,fontWeight:300}}>{desc}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Who it serves ── */}
      <section style={{padding:'3rem 2rem',background:'#0a0a12',borderTop:'0.5px solid #1a1628'}}>
        <h2 style={{fontFamily:"'Cinzel',serif",fontSize:'1.3rem',fontWeight:600,color:'#F5EDD8',textAlign:'center',marginBottom:'0.5rem',letterSpacing:'0.1em'}}>Built for Every Indian</h2>
        <p style={{fontSize:'0.82rem',color:'#8a8070',textAlign:'center',marginBottom:'2.5rem',letterSpacing:'0.08em'}}>हर भारतीय के लिए · All levels. All dreams.</p>
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(140px,1fr))',gap:'1rem',maxWidth:640,margin:'0 auto'}}>
          {[
            ['🛒','Street vendor','Rs.5,000 – Rs.20,000','Tea stall, fruit cart, snack vendor, cobbler, mobile repair'],
            ['🏪','Micro shop','Rs.20,000 – Rs.1 lakh','Kirana, pan shop, salon, tailoring, STD booth'],
            ['🏬','Small business','Rs.1 – Rs.10 lakh','Medical store, restaurant, coaching centre, hardware'],
            ['🏢','Medium business','Rs.10 lakh+','Supermarket, gym, clinic, school, hotel, showroom'],
          ].map(([emoji,title,cap,desc])=>(
            <div key={title} style={{background:'#0d0d1a',border:'0.5px solid #1e1a2e',borderRadius:8,padding:'1.5rem 1rem',textAlign:'center'}}>
              <span style={{fontSize:'2rem',marginBottom:'0.8rem',display:'block'}}>{emoji}</span>
              <div style={{fontSize:'0.85rem',fontWeight:500,color:'#F5EDD8',marginBottom:'0.3rem'}}>{title}</div>
              <div style={{fontSize:'0.72rem',color:'#00C9A7',letterSpacing:'0.08em',marginBottom:'0.5rem'}}>{cap}</div>
              <div style={{fontSize:'0.72rem',color:'#8a8070',lineHeight:1.5,fontWeight:300}}>{desc}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Impact ── */}
      <section style={{padding:'3rem 2rem',background:'#06060f',borderTop:'0.5px solid #1a1628',textAlign:'center'}}>
        <p style={{fontFamily:"'Cinzel',serif",fontSize:'1.1rem',color:'#F5EDD8',lineHeight:1.7,maxWidth:480,margin:'0 auto 1rem',fontWeight:400,letterSpacing:'0.05em'}}>
          "Every corner of India holds an opportunity.<br/>SPANDAN finds it before you do."
        </p>
        <p style={{fontSize:'0.85rem',color:'#FF6B00',letterSpacing:'0.08em',marginBottom:'2rem'}}>
          हर कोने में अवसर है। स्पन्दन उसे पहले देखता है।
        </p>
        <div style={{display:'flex',gap:'0.8rem',justifyContent:'center',flexWrap:'wrap',marginTop:'1.5rem'}}>
          {['UN SDG Goal 1 · No Poverty','UN SDG Goal 8 · Decent Work','Startup India','Make in India','Digital India'].map(b=>(
            <span key={b} style={{background:'#0d0d1a',border:'0.5px solid #2a2040',borderRadius:4,padding:'0.4rem 0.8rem',fontSize:'0.7rem',color:'#00C9A7',letterSpacing:'0.1em',textTransform:'uppercase'}}>{b}</span>
          ))}
        </div>
      </section>

      {/* ── Footer ── */}
      <footer style={{padding:'2rem',borderTop:'0.5px solid #1a1628',display:'flex',flexDirection:'column',alignItems:'center',gap:'0.8rem',background:'#0a0a12'}}>
        <div style={{fontFamily:"'Cinzel',serif",fontSize:'1.1rem',background:'linear-gradient(135deg,#FF6B00,#E8A020)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent',backgroundClip:'text',letterSpacing:'0.15em'}}>SPANDAN AI</div>
        <div style={{fontSize:'0.75rem',color:'#8a8070',letterSpacing:'0.2em'}}>स्पन्दन · The Pulse of India's Opportunity</div>
        <div style={{fontSize:'0.75rem',color:'#4a4050',letterSpacing:'0.08em',textAlign:'center'}}>Building prosperity. One pin code at a time.</div>
      </footer>

    </div>
  )
}
