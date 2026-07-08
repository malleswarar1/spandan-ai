import { useState, useCallback } from 'react'
import SplashPage from './pages/SplashPage.jsx'
import LandingPage from './pages/LandingPage.jsx'
import SpaceDesignerPage from './pages/SpaceDesignerPage.jsx'
import IdentityPage from './pages/IdentityPage.jsx'
import FundingPage from './pages/FundingPage.jsx'
import OpportunityPage from './pages/OpportunityPage.jsx'
import { T, Card, Stat, Skeleton, Alert, fmt } from './components/UI.jsx'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// ─── Sidebar nav items ────────────────────────────────────────────────────────
const NAV = [
  { key: 'dashboard',   icon: '⬡', label: 'Dashboard',       color: T.orange },
  { key: 'opportunity', icon: '🔍', label: 'Opportunity',     color: T.orange },
  { key: 'identity',    icon: '👤', label: 'Identity',        color: T.purple },
  { key: 'space',       icon: '📐', label: 'Space Designer',  color: T.gold   },
  { key: 'funding',     icon: '💰', label: 'Funding',         color: T.teal   },
]

// ─── Sidebar ─────────────────────────────────────────────────────────────────
function Sidebar({ page, onNavigate, onGoHome }) {
  return (
    <aside className="sidebar" role="navigation" aria-label="Main navigation">
      {/* Logo */}
      <div
        onClick={onGoHome}
        style={{
          padding: '1.4rem 1.2rem 1.2rem',
          borderBottom: `0.5px solid ${T.border}`,
          cursor: 'pointer',
        }}
      >
        <svg width="72" height="28" viewBox="0 0 120 48">
          <polyline
            points="0,24 12,24 18,8 24,40 30,4 38,44 44,24 56,24 62,14 70,34 76,24 90,24 96,16 104,32 110,24 120,24"
            fill="none" stroke={T.orange} strokeWidth="2.5"
            strokeLinecap="round" strokeLinejoin="round"
          />
        </svg>
        <div style={{
          fontFamily: T.serif,
          fontSize: '1.15rem',
          fontWeight: 700,
          background: `linear-gradient(135deg,${T.orange},${T.gold})`,
          WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
          letterSpacing: '0.15em',
          marginTop: '0.3rem',
        }}>
          SPANDAN
        </div>
        <div style={{ fontSize: '0.6rem', color: T.dim, letterSpacing: '0.25em', marginTop: 2 }}>
          स्पन्दन · AI
        </div>
      </div>

      {/* Nav items */}
      <nav style={{ padding: '0.75rem 0.6rem', flex: 1 }}>
        {NAV.map(({ key, icon, label, color }) => {
          const active = page === key
          return (
            <button
              key={key}
              onClick={() => onNavigate(key)}
              aria-current={active ? 'page' : undefined}
              style={{
                width: '100%',
                display: 'flex',
                alignItems: 'center',
                gap: '0.65rem',
                padding: '0.6rem 0.85rem',
                marginBottom: 2,
                background: active ? `${color}18` : 'transparent',
                border: `0.5px solid ${active ? `${color}60` : 'transparent'}`,
                borderRadius: 8,
                color: active ? color : T.muted,
                fontSize: '0.82rem',
                fontFamily: T.ff,
                fontWeight: active ? 600 : 400,
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.15s',
              }}
              onMouseEnter={e => { if (!active) e.currentTarget.style.background = T.s2 }}
              onMouseLeave={e => { if (!active) e.currentTarget.style.background = 'transparent' }}
            >
              <span style={{ fontSize: '1rem', width: 20, textAlign: 'center', flexShrink: 0 }}>{icon}</span>
              <span>{label}</span>
            </button>
          )
        })}
      </nav>

      {/* Bottom */}
      <div style={{
        padding: '0.75rem 1rem',
        borderTop: `0.5px solid ${T.border}`,
        fontSize: '0.62rem',
        color: T.dim,
        letterSpacing: '0.1em',
        lineHeight: 1.8,
      }}>
        <div>SPANDAN AI v3.0</div>
        <div style={{ color: '#3a3444' }}>423+ pin codes · 34 states</div>
        <button
          onClick={onGoHome}
          style={{
            marginTop: 6,
            fontSize: '0.62rem',
            color: T.dim,
            background: 'transparent',
            border: `0.5px solid ${T.borderL}`,
            padding: '2px 8px',
            borderRadius: 4,
            cursor: 'pointer',
            fontFamily: T.ff,
          }}
        >
          ↩ Home
        </button>
      </div>
    </aside>
  )
}

// ─── Mobile bottom tab bar ────────────────────────────────────────────────────
function MobileNav({ page, onNavigate }) {
  return (
    <nav className="mobile-nav" role="navigation" aria-label="Mobile navigation">
      {NAV.map(({ key, icon, label, color }) => {
        const active = page === key
        return (
          <button
            key={key}
            onClick={() => onNavigate(key)}
            aria-current={active ? 'page' : undefined}
            style={{
              display: 'flex', flexDirection: 'column', alignItems: 'center',
              gap: 3, padding: '0.4rem 0.5rem',
              background: 'transparent', border: 'none',
              color: active ? color : T.dim,
              fontSize: '0.55rem',
              fontFamily: T.ff,
              cursor: 'pointer',
              transition: 'color 0.15s',
              flex: 1,
            }}
          >
            <span style={{ fontSize: '1.2rem' }}>{icon}</span>
            <span style={{ letterSpacing: '0.06em' }}>{label.split(' ')[0]}</span>
          </button>
        )
      })}
    </nav>
  )
}

// ─── Dashboard ────────────────────────────────────────────────────────────────
function DashboardPage({ onNavigate }) {
  const modules = [
    {
      key: 'opportunity', icon: '🔍', label: 'Find My Opportunity',
      desc: 'Scan any pincode, match your profile to the best business opportunity in that area',
      color: T.orange, badge: 'Most Used',
    },
    {
      key: 'identity', icon: '👤', label: 'Identity Profiler',
      desc: 'Full opportunity analysis, scheme eligibility, career paths, skill gap insights',
      color: T.purple,
    },
    {
      key: 'space', icon: '📐', label: 'Space Designer',
      desc: 'Autonomous floor plan generator — equipment layout, cost estimate for any business',
      color: T.gold, badge: 'AI Generated',
    },
    {
      key: 'funding', icon: '💰', label: 'Funding Finder',
      desc: '12 govt schemes including MUDRA, SVANidhi, PMEGP — with live EMI calculator',
      color: T.teal,
    },
  ]

  return (
    <div className="page-wrap fade-in">
      {/* Hero */}
      <div style={{ textAlign: 'center', padding: '2rem 1rem 2.5rem', borderBottom: `0.5px solid ${T.border}`, marginBottom: '2rem' }}>
        <div style={{ display: 'inline-flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
          <svg width="88" height="34" viewBox="0 0 120 48">
            <polyline
              points="0,24 12,24 18,8 24,40 30,4 38,44 44,24 56,24 62,14 70,34 76,24 90,24 96,16 104,32 110,24 120,24"
              fill="none" stroke={T.orange} strokeWidth="2.5"
              strokeLinecap="round" strokeLinejoin="round"
            />
          </svg>
          <div style={{
            fontFamily: T.serif,
            fontSize: 'clamp(2rem, 5vw, 3rem)',
            fontWeight: 700,
            background: `linear-gradient(135deg,${T.orange},${T.gold},#F5C842)`,
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
            letterSpacing: '0.15em',
            lineHeight: 1,
          }}>
            SPANDAN
          </div>
          <div style={{ fontFamily: T.serif, fontSize: '0.88rem', color: T.muted, letterSpacing: '0.3em' }}>
            स्पन्दन · AI
          </div>
          <div style={{ fontSize: '0.72rem', color: T.teal, letterSpacing: '0.2em' }}>
            भारत की धड़कन · India's Pulse
          </div>
        </div>
        <p style={{ fontSize: '0.9rem', color: T.muted, maxWidth: 480, margin: '1.5rem auto 0', lineHeight: 1.8 }}>
          Every corner of India holds an opportunity. SPANDAN finds it, designs it, and funds it.
        </p>
      </div>

      {/* Module grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(240px,1fr))', gap: '0.75rem', marginBottom: '2rem' }}>
        {modules.map(m => (
          <button
            key={m.key}
            onClick={() => onNavigate(m.key)}
            style={{
              background: T.s1,
              border: `0.5px solid ${T.border}`,
              borderRadius: 12,
              padding: '1.4rem',
              textAlign: 'left',
              cursor: 'pointer',
              fontFamily: T.ff,
              transition: 'border-color 0.15s, background 0.15s',
              position: 'relative',
              display: 'flex',
              flexDirection: 'column',
              gap: 8,
            }}
            onMouseEnter={e => {
              e.currentTarget.style.borderColor = m.color
              e.currentTarget.style.background = T.s2
            }}
            onMouseLeave={e => {
              e.currentTarget.style.borderColor = T.border
              e.currentTarget.style.background = T.s1
            }}
          >
            {m.badge && (
              <div style={{
                position: 'absolute', top: 12, right: 12,
                fontSize: '0.58rem', color: m.color,
                border: `0.5px solid ${m.color}50`,
                padding: '2px 7px', borderRadius: 4,
                letterSpacing: '0.08em', textTransform: 'uppercase',
              }}>
                {m.badge}
              </div>
            )}
            <span style={{ fontSize: '1.8rem' }}>{m.icon}</span>
            <div style={{ fontSize: '0.92rem', fontWeight: 600, color: m.color }}>{m.label}</div>
            <div style={{ fontSize: '0.75rem', color: T.muted, lineHeight: 1.6 }}>{m.desc}</div>
            <div style={{ fontSize: '0.72rem', color: m.color, marginTop: 4, opacity: 0.7 }}>
              Open →
            </div>
          </button>
        ))}
      </div>

      {/* Stats strip */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4,1fr)',
        gap: 1,
        background: '#131124',
        border: `1px solid #131124`,
        borderRadius: 10,
        overflow: 'hidden',
        marginBottom: '2rem',
      }}>
        {[
          ['423+', 'Pin Codes', T.orange],
          ['12+', 'Govt Schemes', T.teal],
          ['14', 'Business Types', T.gold],
          ['₹0', 'Cost to Use', T.purple],
        ].map(([n, l, c]) => (
          <div key={l} style={{ background: T.s1, padding: '1.2rem 0.75rem', textAlign: 'center' }}>
            <div style={{
              fontFamily: T.serif, fontSize: '1.4rem', fontWeight: 700,
              background: `linear-gradient(135deg,${c},${T.gold})`,
              WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
              marginBottom: 4,
            }}>
              {n}
            </div>
            <div style={{ fontSize: '0.6rem', color: T.dim, textTransform: 'uppercase', letterSpacing: '0.1em' }}>{l}</div>
          </div>
        ))}
      </div>

      {/* Quick actions */}
      <div style={{ borderTop: `0.5px solid ${T.border}`, paddingTop: '1.5rem' }}>
        <div style={{ fontSize: '0.65rem', color: T.dim, letterSpacing: '0.2em', textTransform: 'uppercase', marginBottom: '0.8rem' }}>
          Quick Start
        </div>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {[
            ['🎯 Find opportunity in 560037', 'opportunity'],
            ['💡 Check MUDRA eligibility', 'funding'],
            ['🏗️ Design a tea stall layout', 'space'],
          ].map(([label, page]) => (
            <button
              key={label}
              onClick={() => onNavigate(page)}
              style={{
                fontSize: '0.75rem', color: T.muted,
                background: T.s2,
                border: `0.5px solid ${T.border}`,
                padding: '0.4rem 0.9rem', borderRadius: 6,
                cursor: 'pointer', fontFamily: T.ff,
                transition: 'border-color 0.15s, color 0.15s',
              }}
              onMouseEnter={e => {
                e.currentTarget.style.borderColor = T.orange
                e.currentTarget.style.color = T.text
              }}
              onMouseLeave={e => {
                e.currentTarget.style.borderColor = T.border
                e.currentTarget.style.color = T.muted
              }}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Footer note */}
      <div style={{ textAlign: 'center', marginTop: '3rem', fontSize: '0.62rem', color: '#2a2438' }}>
        SPANDAN AI · स्पन्दन · 34 states · 423 pin codes · Aligned to UN SDG 1, 8
      </div>
    </div>
  )
}

// ─── App Shell (sidebar + content) ───────────────────────────────────────────
function AppShell({ page, setPage }) {
  const goHome = useCallback(() => setPage('landing'), [setPage])

  const renderPage = () => {
    switch (page) {
      case 'dashboard':   return <DashboardPage onNavigate={setPage} />
      case 'opportunity': return <OpportunityPage onBack={() => setPage('dashboard')} />
      case 'space':       return <SpaceDesignerPage onBack={() => setPage('dashboard')} />
      case 'identity':    return <IdentityPage onBack={() => setPage('dashboard')} />
      case 'funding':     return <FundingPage onBack={() => setPage('dashboard')} />
      default:            return <DashboardPage onNavigate={setPage} />
    }
  }

  return (
    <div className="app-shell">
      <Sidebar page={page} onNavigate={setPage} onGoHome={goHome} />
      <main className="content-pane" role="main">
        {renderPage()}
      </main>
      <MobileNav page={page} onNavigate={setPage} />
    </div>
  )
}

// ─── Root ────────────────────────────────────────────────────────────────────
export default function App() {
  const [page, setPage] = useState('splash')

  if (page === 'splash') return <SplashPage onEnter={() => setPage('landing')} />
  if (page === 'landing') return <LandingPage onEnter={() => setPage('dashboard')} />

  // All app pages rendered inside the shell
  return <AppShell page={page} setPage={setPage} />
}
