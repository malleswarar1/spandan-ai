import { useEffect, useState } from 'react'

const msgs = [
  'Reading India\'s pulse...',
  'Scanning 19,000+ pin codes...',
  'Mapping business gaps...',
  'Matching opportunities...',
  'Ready...'
]

export default function SplashPage({ onEnter }) {
  const [msg, setMsg] = useState(msgs[0])
  const [progress, setProgress] = useState(0)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    let i = 0
    const iv = setInterval(() => {
      i++
      if (i < msgs.length) {
        setMsg(msgs[i])
        setProgress(Math.round((i / msgs.length) * 100))
      } else {
        setReady(true)
        clearInterval(iv)
      }
    }, 700)
    return () => clearInterval(iv)
  }, [])

  return (
    <div style={{
      background:'#07060f', minHeight:'100vh', display:'flex',
      flexDirection:'column', alignItems:'center', justifyContent:'center',
      fontFamily:"'Inter',sans-serif", padding:'2rem 1rem', position:'relative', overflow:'hidden'
    }}>
      {/* Corner decorations */}
      {['tl','tr','bl','br'].map(c => (
        <div key={c} style={{
          position:'absolute',
          width:20, height:20, opacity:0.2,
          top: c.includes('t') ? '1rem' : 'auto',
          bottom: c.includes('b') ? '1rem' : 'auto',
          left: c.includes('l') ? '1rem' : 'auto',
          right: c.includes('r') ? '1rem' : 'auto',
          borderTop: c.includes('t') ? '1px solid #FF6B00' : 'none',
          borderBottom: c.includes('b') ? '1px solid #FF6B00' : 'none',
          borderLeft: c.includes('l') ? '1px solid #FF6B00' : 'none',
          borderRight: c.includes('r') ? '1px solid #FF6B00' : 'none',
        }}/>
      ))}

      {/* Pulse SVG */}
      <svg width="140" height="56" viewBox="0 0 120 48" style={{marginBottom:'0.5rem'}}>
        <polyline points="0,24 12,24 18,8 24,40 30,4 38,44 44,24 56,24 62,14 70,34 76,24 90,24 96,16 104,32 110,24 120,24"
          fill="none" stroke="#FF6B00" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>

      {/* Center dot */}
      <div style={{width:10,height:10,background:'#FF6B00',borderRadius:'50%',margin:'0 auto 1rem',boxShadow:'0 0 12px #FF6B00'}}/>

      {/* Name */}
      <div style={{fontSize:'3rem',fontWeight:700,fontFamily:"'Cinzel',serif",color:'#FF6B00',letterSpacing:'0.18em',lineHeight:1,marginBottom:'0.3rem',textAlign:'center'}}>
        SPANDAN
      </div>
      <div style={{fontFamily:"'Cinzel',serif",fontSize:'1rem',color:'#5a4a38',letterSpacing:'0.35em',marginBottom:'0.5rem',textAlign:'center'}}>
        स्पन्दन · AI
      </div>
      <div style={{width:60,height:1,background:'#FF6B00',opacity:0.4,margin:'0.6rem auto'}}/>
      <div style={{fontSize:'0.78rem',color:'#00C9A7',letterSpacing:'0.28em',textTransform:'uppercase',textAlign:'center',marginBottom:'0.2rem'}}>
        भारत की धड़कन · India's Pulse
      </div>
      <div style={{fontSize:'0.72rem',color:'#3a3040',letterSpacing:'0.18em',textAlign:'center',marginBottom:'2rem'}}>
        Every Indian · Every Opportunity
      </div>

      {/* Progress bar */}
      <div style={{width:220,height:2,background:'#1a1228',borderRadius:2,overflow:'hidden',marginBottom:'0.6rem'}}>
        <div style={{height:'100%',background:'#FF6B00',borderRadius:2,width:`${progress}%`,transition:'width 0.6s ease'}}/>
      </div>
      <div style={{fontSize:'0.72rem',color:'#5a4a38',letterSpacing:'0.2em',textTransform:'uppercase',marginBottom:'2rem'}}>
        {msg}
      </div>

      {/* Stats */}
      <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:8,width:'100%',maxWidth:520,marginBottom:'1.5rem'}}>
        {[['19K+','Pin codes'],['63M','MSMEs'],['Rs.0','Cost'],['22','Languages']].map(([n,l])=>(
          <div key={l} style={{background:'#0d0b18',border:'0.5px solid #1e1628',borderRadius:8,padding:'0.8rem 0.4rem',textAlign:'center'}}>
            <div style={{fontFamily:"'Cinzel',serif",fontSize:'1.1rem',fontWeight:700,color:'#E8A020'}}>{n}</div>
            <div style={{fontSize:'0.6rem',color:'#4a4050',letterSpacing:'0.08em',textTransform:'uppercase',marginTop:2,lineHeight:1.3}}>{l}</div>
          </div>
        ))}
      </div>

      {/* Enter button */}
      {ready && (
        <button onClick={onEnter} style={{
          background:'#FF6B00',color:'white',border:'none',
          padding:'0.8rem 2.4rem',borderRadius:5,
          fontSize:'0.82rem',fontWeight:500,
          letterSpacing:'0.14em',textTransform:'uppercase',
          cursor:'pointer',fontFamily:"'Inter',sans-serif"
        }}>
          Enter SPANDAN AI &rarr;
        </button>
      )}
    </div>
  )
}
