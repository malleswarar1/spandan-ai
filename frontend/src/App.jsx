import { useState } from 'react'
import LandingPage from './pages/LandingPage.jsx'

const API = 'http://localhost:8000'

function Stat({ label, value, color }) {
  return (
    <div style={{background:'#06060f',borderRadius:6,padding:'0.7rem',textAlign:'center'}}>
      <div style={{fontSize:'1rem',fontWeight:600,color:color||'#E8A020'}}>{value}</div>
      <div style={{fontSize:'0.68rem',color:'#8a8070',marginTop:'0.2rem',textTransform:'uppercase',letterSpacing:'0.08em'}}>{label}</div>
    </div>
  )
}

function urgencyColor(u) {
  return {critical:'#ff4444',high:'#FF6B00',medium:'#E8A020',low:'#00C9A7'}[u]||'#8a8070'
}

export default function App() {
  const [showLanding, setShowLanding] = useState(true)
  const [form, setForm] = useState({pincode:'',capital:'',skills:'any',isWoman:false,caste:'general',risk:'medium',name:''})
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [tab, setTab] = useState('scan')
  const [cityData, setCityData] = useState(null)
  const [cityLoading, setCityLoading] = useState(false)

  if (showLanding) return <LandingPage onEnter={() => setShowLanding(false)} />

  const scan = async () => {
    if (!form.pincode || !form.capital) { setError('Enter pincode and capital'); return }
    setLoading(true); setError(''); setResult(null)
    try {
      const res = await fetch(`${API}/api/opportunity/scan`, {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ pincode:form.pincode, capital:parseFloat(form.capital), skills:form.skills.split(',').map(s=>s.trim()), is_woman:form.isWoman, caste_category:form.caste, risk_appetite:form.risk, name:form.name||'User' })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail||'Error')
      setResult(data)
    } catch(e) { setError(e.message) }
    finally { setLoading(false) }
  }

  const scanCity = async (city) => {
    setCityLoading(true); setCityData(null)
    try {
      const res = await fetch(`${API}/api/opportunity/city/${city}`)
      setCityData(await res.json())
    } catch(e) { setError(e.message) }
    finally { setCityLoading(false) }
  }

  return (
    <div style={{maxWidth:820,margin:'0 auto',padding:'1.5rem 1rem'}}>
      <div style={{textAlign:'center',marginBottom:'2rem',paddingBottom:'1.5rem',borderBottom:'0.5px solid #1e1a2e'}}>
        <div style={{fontSize:'2.2rem',fontWeight:700,fontFamily:"'Cinzel',serif",background:'linear-gradient(135deg,#FF6B00,#E8A020)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent',letterSpacing:'0.12em'}}>SPANDAN AI</div>
        <div style={{color:'#8a8070',fontSize:'0.85rem',letterSpacing:'0.25em',marginTop:'0.3rem'}}>स्पन्दन · भारत की धड़कन</div>
        <button onClick={()=>setShowLanding(true)} style={{marginTop:'0.5rem',background:'transparent',border:'0.5px solid #1e1a2e',color:'#5a4050',padding:'0.3rem 0.8rem',borderRadius:4,fontSize:'0.7rem',cursor:'pointer',letterSpacing:'0.1em'}}>← Back to home</button>
      </div>

      <div style={{display:'flex',gap:'0.5rem',marginBottom:'1.5rem'}}>
        {['scan','city'].map(t=>(
          <button key={t} onClick={()=>setTab(t)} style={{padding:'0.5rem 1.2rem',borderRadius:6,border:'0.5px solid',cursor:'pointer',fontSize:'0.82rem',letterSpacing:'0.08em',textTransform:'uppercase',fontWeight:500,background:tab===t?'#FF6B00':'transparent',color:tab===t?'white':'#8a8070',borderColor:tab===t?'#FF6B00':'#1e1a2e'}}>
            {t==='scan'?'Find My Opportunity':'City Map'}
          </button>
        ))}
      </div>

      {tab==='scan' && (
        <div>
          <div style={{background:'#0d0d1a',border:'0.5px solid #1e1a2e',borderRadius:12,padding:'1.5rem',marginBottom:'1.5rem'}}>
            <h2 style={{fontSize:'1rem',color:'#F5EDD8',marginBottom:'1.2rem'}}>Tell us about yourself</h2>
            <div style={{display:'grid',gap:'1rem',gridTemplateColumns:'1fr 1fr'}}>
              {[['Your Name','name','text','e.g. Raju Kumar'],['Pin Code','pincode','text','e.g. 560037'],['Capital (Rs.)','capital','number','e.g. 50000'],['Skills','skills','text','cooking, selling, any']].map(([label,field,type,ph])=>(
                <div key={field}>
                  <label style={{display:'block',fontSize:'0.72rem',color:'#8a8070',marginBottom:'0.35rem',letterSpacing:'0.12em',textTransform:'uppercase'}}>{label}</label>
                  <input type={type} value={form[field]} onChange={e=>setForm({...form,[field]:e.target.value})} placeholder={ph}
                    style={{width:'100%',padding:'0.65rem',background:'#06060f',border:'0.5px solid #1e1a2e',borderRadius:6,color:'#F5EDD8',fontSize:'0.9rem'}}/>
                </div>
              ))}
              <div>
                <label style={{display:'block',fontSize:'0.72rem',color:'#8a8070',marginBottom:'0.35rem',letterSpacing:'0.12em',textTransform:'uppercase'}}>Risk Appetite</label>
                <select value={form.risk} onChange={e=>setForm({...form,risk:e.target.value})} style={{width:'100%',padding:'0.65rem',background:'#06060f',border:'0.5px solid #1e1a2e',borderRadius:6,color:'#F5EDD8',fontSize:'0.9rem'}}>
                  <option value="low">Low — Safe and steady</option>
                  <option value="medium">Medium — Balanced</option>
                  <option value="high">High — Growth focused</option>
                </select>
              </div>
              <div>
                <label style={{display:'block',fontSize:'0.72rem',color:'#8a8070',marginBottom:'0.35rem',letterSpacing:'0.12em',textTransform:'uppercase'}}>Category</label>
                <select value={form.caste} onChange={e=>setForm({...form,caste:e.target.value})} style={{width:'100%',padding:'0.65rem',background:'#06060f',border:'0.5px solid #1e1a2e',borderRadius:6,color:'#F5EDD8',fontSize:'0.9rem'}}>
                  <option value="general">General</option>
                  <option value="obc">OBC</option>
                  <option value="sc">SC</option>
                  <option value="st">ST</option>
                </select>
              </div>
            </div>
            <div style={{marginTop:'1rem',display:'flex',alignItems:'center',gap:'0.5rem'}}>
              <input type="checkbox" id="woman" checked={form.isWoman} onChange={e=>setForm({...form,isWoman:e.target.checked})} style={{accentColor:'#FF6B00'}}/>
              <label htmlFor="woman" style={{fontSize:'0.82rem',color:'#8a8070',cursor:'pointer'}}>Woman entrepreneur — unlocks special schemes</label>
            </div>
            {error && <div style={{marginTop:'0.8rem',padding:'0.6rem',background:'#1a0606',border:'0.5px solid #ff4444',borderRadius:6,color:'#ff8080',fontSize:'0.82rem'}}>{error}</div>}
            <button onClick={scan} disabled={loading} style={{marginTop:'1.2rem',width:'100%',padding:'0.85rem',background:loading?'#2a2030':'linear-gradient(135deg,#FF6B00,#E8A020)',color:'white',border:'none',borderRadius:6,fontSize:'0.92rem',fontWeight:600,cursor:loading?'not-allowed':'pointer',letterSpacing:'0.08em',textTransform:'uppercase'}}>
              {loading?'Reading India pulse...':'Find My Opportunity →'}
            </button>
          </div>

          {result && (
            <div>
              <div style={{background:'#0d0d1a',border:'0.5px solid #1e1a2e',borderRadius:12,padding:'1.5rem',marginBottom:'1.2rem'}}>
                <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',flexWrap:'wrap',gap:'1rem'}}>
                  <div>
                    <div style={{fontSize:'1.4rem',fontWeight:700,color:'#FF6B00',fontFamily:"'Cinzel',serif"}}>{result.city}</div>
                    <div style={{color:'#8a8070',fontSize:'0.82rem',marginTop:'0.2rem'}}>{result.state} · Pin {result.pincode} · Pop {result.population?.toLocaleString()}</div>
                    <div style={{color:'#00C9A7',fontSize:'0.82rem',marginTop:'0.5rem'}}>{result.message_hindi}</div>
                  </div>
                  <div style={{textAlign:'center',background:'#06060f',padding:'1rem 1.5rem',borderRadius:8,minWidth:100}}>
                    <div style={{fontSize:'2rem',fontWeight:700,color:'#E8A020',fontFamily:"'Cinzel',serif"}}>{result.opportunity_score}</div>
                    <div style={{fontSize:'0.65rem',color:'#8a8070',letterSpacing:'0.1em',textTransform:'uppercase'}}>Opportunity Score</div>
                  </div>
                </div>
                <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(110px,1fr))',gap:'0.6rem',marginTop:'1rem'}}>
                  <Stat label="Income Level" value={result.income_tier?.replace('_',' ')} color="#00C9A7"/>
                  <Stat label="Gaps Found" value={result.top_gaps?.length+'+'}/>
                  <Stat label="Matches" value={result.matched_businesses?.length}/>
                  <Stat label="Population" value={(result.population/1000).toFixed(0)+'K'}/>
                </div>
              </div>

              <h3 style={{fontSize:'0.82rem',color:'#8a8070',letterSpacing:'0.2em',textTransform:'uppercase',marginBottom:'0.8rem'}}>Your Best Matches</h3>
              {result.matched_businesses?.map((biz,i)=>(
                <div key={i} style={{background:'#0d0d1a',border:`0.5px solid ${i===0?'#FF6B00':'#1e1a2e'}`,borderRadius:12,padding:'1.2rem',marginBottom:'0.8rem'}}>
                  <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'0.8rem',flexWrap:'wrap',gap:'0.5rem'}}>
                    <div style={{display:'flex',alignItems:'center',gap:'0.6rem'}}>
                      <span style={{fontSize:'1rem',fontWeight:600,color:'#F5EDD8',textTransform:'capitalize'}}>{biz.business_type.replace(/_/g,' ')}</span>
                      {i===0 && <span style={{fontSize:'0.65rem',background:'#FF6B00',color:'white',padding:'2px 7px',borderRadius:4}}>BEST MATCH</span>}
                    </div>
                    <span style={{fontSize:'1.1rem',fontWeight:700,color:'#E8A020'}}>{Math.round(biz.match_score*100)}%</span>
                  </div>
                  <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(110px,1fr))',gap:'0.5rem',marginBottom:'0.8rem'}}>
                    <Stat label="Monthly Revenue" value={`Rs.${(biz.monthly_revenue/1000).toFixed(0)}K`}/>
                    <Stat label="Capital Needed" value={`Rs.${(biz.capital_needed/1000).toFixed(0)}K`}/>
                    <Stat label="Capital Gap" value={biz.capital_gap>0?`Rs.${(biz.capital_gap/1000).toFixed(0)}K`:'None'} color={biz.capital_gap===0?'#00C9A7':'#ff8080'}/>
                    <Stat label="Success" value={biz.success_probability.split(' ')[0]+' '+biz.success_probability.split(' ')[1]} color="#00C9A7"/>
                  </div>
                  <div style={{fontSize:'0.78rem',color:'#00C9A7',marginBottom:'0.6rem'}}>📍 {biz.location_advice}</div>
                  <div style={{marginBottom:'0.6rem'}}>
                    {biz.setup_steps?.slice(0,3).map((s,j)=>(
                      <div key={j} style={{fontSize:'0.78rem',color:'#9a9080',marginBottom:'0.2rem'}}>✓ {s}</div>
                    ))}
                  </div>
                  <div style={{display:'flex',gap:'0.4rem',flexWrap:'wrap'}}>
                    {biz.funding_schemes?.slice(0,2).map((s,j)=>(
                      <span key={j} style={{fontSize:'0.68rem',background:'#0a1a14',color:'#00C9A7',border:'0.5px solid #0f3028',padding:'3px 8px',borderRadius:4}}>💰 {s}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {tab==='city' && (
        <div>
          <div style={{background:'#0d0d1a',border:'0.5px solid #1e1a2e',borderRadius:12,padding:'1.5rem',marginBottom:'1.5rem'}}>
            <h2 style={{fontSize:'1rem',color:'#F5EDD8',marginBottom:'1rem'}}>Scan an Entire City</h2>
            <div style={{display:'flex',gap:'0.5rem',flexWrap:'wrap'}}>
              {['bangalore','mumbai','delhi','hyderabad','chennai'].map(city=>(
                <button key={city} onClick={()=>scanCity(city)} style={{padding:'0.6rem 1.2rem',borderRadius:6,border:'0.5px solid #2a2040',background:'#06060f',color:'#F5EDD8',cursor:'pointer',fontSize:'0.82rem',textTransform:'capitalize',fontWeight:500}}>
                  {city.charAt(0).toUpperCase()+city.slice(1)}
                </button>
              ))}
            </div>
          </div>
          {cityLoading && <div style={{textAlign:'center',color:'#8a8070',padding:'2rem'}}>Scanning city pulse...</div>}
          {cityData && Object.entries(cityData.results||{}).map(([pin,data])=>(
            <div key={pin} style={{background:'#0d0d1a',border:'0.5px solid #1e1a2e',borderRadius:12,padding:'1.2rem',marginBottom:'0.8rem'}}>
              <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'0.8rem',flexWrap:'wrap',gap:'0.5rem'}}>
                <div style={{fontWeight:600,color:'#F5EDD8'}}>Pin Code {pin}</div>
                <div><span style={{fontSize:'1.3rem',fontWeight:700,color:'#E8A020'}}>{data.opportunity_score}</span><span style={{fontSize:'0.68rem',color:'#8a8070',marginLeft:'0.3rem'}}>score</span></div>
              </div>
              <div style={{display:'flex',gap:'0.4rem',flexWrap:'wrap'}}>
                {data.top_gaps?.map((gap,j)=>(
                  <span key={j} style={{fontSize:'0.68rem',background:'#06060f',color:urgencyColor(gap.urgency),border:`0.5px solid ${urgencyColor(gap.urgency)}30`,padding:'3px 8px',borderRadius:4,textTransform:'capitalize'}}>
                    {gap.type.replace(/_/g,' ')} · Rs.{(gap.revenue/1000).toFixed(0)}K
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      <div style={{textAlign:'center',marginTop:'3rem',paddingTop:'1.5rem',borderTop:'0.5px solid #1e1a2e'}}>
        <div style={{fontSize:'0.72rem',color:'#3a3040',letterSpacing:'0.15em'}}>SPANDAN AI · स्पन्दन · Building prosperity, one pin code at a time</div>
      </div>
    </div>
  )
}
