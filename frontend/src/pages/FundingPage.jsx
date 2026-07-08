import { useState, useEffect } from 'react'
import {
  T, Card, Stat, Tabs, Badge, Alert, Btn, Field, SelectField,
  Skeleton, SkeletonCard, SectionTitle, Divider, PageHeader,
  PriorityBadge, fmt, Empty,
} from '../components/UI.jsx'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Tag({ children, color = T.teal }) {
  return <Badge color={color}>{children}</Badge>
}

function SchemeCard({ scheme, onCalc }) {
  const [expanded, setExpanded] = useState(false)
  const maxAmt = scheme.max_amount
  const display = fmt(maxAmt)

  return (
    <Card style={{ marginBottom: '0.75rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 8, marginBottom: '0.75rem' }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: '0.95rem', fontWeight: 600, color: T.text, marginBottom: 2 }}>
            {scheme.name}
          </div>
          {scheme.ministry && (
            <div style={{ fontSize: '0.68rem', color: T.dim }}>{scheme.ministry}</div>
          )}
          {scheme.hindi_name && (
            <div style={{ fontSize: '0.68rem', color: T.muted, fontStyle: 'italic' }}>{scheme.hindi_name}</div>
          )}
        </div>
        <div style={{ textAlign: 'right', flexShrink: 0 }}>
          <div style={{ fontSize: '1.1rem', fontWeight: 700, color: T.gold, fontVariantNumeric: 'tabular-nums' }}>
            {display}
          </div>
          <div style={{ fontSize: '0.6rem', color: T.dim }}>max loan</div>
          {scheme.subsidy_percent > 0 && (
            <div style={{ fontSize: '0.68rem', color: T.teal, marginTop: 2 }}>
              {scheme.subsidy_percent}% govt subsidy
            </div>
          )}
        </div>
      </div>

      {/* Description */}
      <div style={{ fontSize: '0.78rem', color: T.muted, lineHeight: 1.7, marginBottom: '0.75rem' }}>
        {scheme.description}
      </div>

      {/* Tags */}
      <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginBottom: '0.75rem' }}>
        {scheme.tags?.map(t => <Tag key={t}>{t.replace(/_/g, ' ')}</Tag>)}
        {!scheme.collateral && <Tag color={T.orange}>No Collateral</Tag>}
        {scheme.subsidy_percent > 0 && <Tag color={T.gold}>{scheme.subsidy_percent}% Subsidy</Tag>}
        {scheme.processing_days && <Tag color={T.muted}>⏱ {scheme.processing_days} days</Tag>}
        {scheme.interest_rate && <Tag color={T.muted}>{scheme.interest_rate}</Tag>}
      </div>

      {/* Expanded detail */}
      {expanded && (
        <div style={{ borderTop: `0.5px solid ${T.border}`, paddingTop: '0.75rem', marginTop: '0.25rem' }}>
          {scheme.eligibility?.length > 0 && (
            <div style={{ marginBottom: '0.75rem' }}>
              <div style={{ fontSize: '0.65rem', color: T.dim, letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 5 }}>
                Eligibility
              </div>
              {scheme.eligibility.map((e, i) => (
                <div key={i} style={{ fontSize: '0.75rem', color: T.muted, marginBottom: 3, display: 'flex', gap: 6 }}>
                  <span style={{ color: T.teal, flexShrink: 0 }}>•</span>{e}
                </div>
              ))}
            </div>
          )}
          {scheme.documents?.length > 0 && (
            <div style={{ marginBottom: '0.75rem' }}>
              <div style={{ fontSize: '0.65rem', color: T.dim, letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 5 }}>
                Documents Required
              </div>
              {scheme.documents.map((d, i) => (
                <div key={i} style={{ fontSize: '0.75rem', color: T.muted, marginBottom: 3, display: 'flex', gap: 6 }}>
                  <span style={{ color: T.gold, flexShrink: 0 }}>📄</span>{d}
                </div>
              ))}
            </div>
          )}
          {scheme.apply_at && (
            <div style={{
              padding: '0.55rem 0.8rem',
              background: `${T.teal}0a`,
              border: `0.5px solid ${T.teal}30`,
              borderRadius: 7,
              fontSize: '0.75rem',
              color: T.teal,
            }}>
              📍 {scheme.apply_at}
            </div>
          )}
        </div>
      )}

      {/* Actions */}
      <div style={{ display: 'flex', gap: 6, marginTop: '0.75rem', flexWrap: 'wrap' }}>
        <Btn variant="ghost" size="sm" onClick={() => setExpanded(!expanded)}>
          {expanded ? '▲ Less' : '▼ Details'}
        </Btn>
        <Btn variant="teal" size="sm" onClick={() => onCalc(scheme)} icon="💰">
          EMI Calculator
        </Btn>
        {scheme.apply_url && (
          <a
            href={scheme.apply_url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              fontSize: '0.75rem', color: T.purple,
              border: `0.5px solid ${T.purple}40`,
              padding: '4px 10px', borderRadius: 6,
              background: `${T.purple}10`,
              display: 'inline-flex', alignItems: 'center', gap: 4,
            }}
          >
            Apply ↗
          </a>
        )}
      </div>
    </Card>
  )
}

function EMIModal({ scheme, onClose }) {
  const [amount, setAmount]   = useState(Math.min(50000, scheme.max_amount))
  const [tenure, setTenure]   = useState(36)
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const handler = (e) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', handler)
    return () => document.removeEventListener('keydown', handler)
  }, [onClose])

  const calculate = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API}/api/funding/calculator/${scheme.id}?amount=${amount}&tenure_months=${tenure}`)
      setResult(await res.json())
    } catch {}
    finally { setLoading(false) }
  }

  useEffect(() => { calculate() }, [amount, tenure])

  return (
    <div
      style={{
        position: 'fixed', inset: 0,
        background: 'rgba(4,3,12,0.92)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        zIndex: 1000, padding: '1rem',
        backdropFilter: 'blur(4px)',
      }}
      onClick={e => { if (e.target === e.currentTarget) onClose() }}
    >
      <div style={{
        background: T.s1,
        border: `0.5px solid ${T.border}`,
        borderRadius: 14,
        padding: '1.5rem',
        maxWidth: 480, width: '100%',
        boxShadow: '0 24px 80px #00000090',
      }}>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
          <div>
            <div style={{ fontSize: '0.92rem', fontWeight: 600, color: T.text }}>{scheme.name}</div>
            <div style={{ fontSize: '0.65rem', color: T.dim, letterSpacing: '0.1em', textTransform: 'uppercase', marginTop: 2 }}>EMI Calculator</div>
          </div>
          <button
            onClick={onClose}
            style={{
              background: T.s2, border: `0.5px solid ${T.border}`,
              color: T.muted, cursor: 'pointer', borderRadius: 6,
              width: 30, height: 30, fontSize: '1rem',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}
          >
            ×
          </button>
        </div>

        {/* Amount slider */}
        <div style={{ marginBottom: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
            <span style={{ fontSize: '0.68rem', color: T.muted, letterSpacing: '0.1em', textTransform: 'uppercase' }}>Loan Amount</span>
            <span style={{ fontSize: '0.9rem', fontWeight: 700, color: T.gold, fontVariantNumeric: 'tabular-nums' }}>{fmt(amount)}</span>
          </div>
          <input
            type="range"
            min={scheme.min_amount || 10000}
            max={scheme.max_amount}
            step={Math.max(1000, Math.round(scheme.max_amount / 100))}
            value={amount}
            onChange={e => setAmount(Number(e.target.value))}
            style={{ width: '100%', accentColor: T.orange }}
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 3 }}>
            <span style={{ fontSize: '0.62rem', color: T.dim }}>{fmt(scheme.min_amount || 10000)}</span>
            <span style={{ fontSize: '0.62rem', color: T.dim }}>{fmt(scheme.max_amount)}</span>
          </div>
        </div>

        {/* Tenure slider */}
        <div style={{ marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
            <span style={{ fontSize: '0.68rem', color: T.muted, letterSpacing: '0.1em', textTransform: 'uppercase' }}>Tenure</span>
            <span style={{ fontSize: '0.9rem', fontWeight: 600, color: T.text }}>
              {tenure} months · {(tenure / 12).toFixed(1)} yrs
            </span>
          </div>
          <input
            type="range" min={6} max={84} step={6} value={tenure}
            onChange={e => setTenure(Number(e.target.value))}
            style={{ width: '100%', accentColor: T.orange }}
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 3 }}>
            <span style={{ fontSize: '0.62rem', color: T.dim }}>6 months</span>
            <span style={{ fontSize: '0.62rem', color: T.dim }}>7 years</span>
          </div>
        </div>

        {/* EMI results */}
        {result && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2,1fr)', gap: '0.5rem', marginBottom: '0.75rem' }}>
            {[
              { label: 'Monthly EMI',      value: fmt(result.monthly_emi),       color: T.orange },
              { label: 'Daily Repayment',  value: fmt(result.daily_repayment),   color: T.teal },
              { label: 'Total Payment',    value: fmt(result.total_payment),     color: T.gold },
              { label: 'Total Interest',   value: fmt(result.total_interest),    color: T.muted },
              { label: 'Govt Subsidy',     value: fmt(result.subsidy_amount),    color: T.teal },
              { label: 'Effective Cost',   value: fmt(result.effective_cost),    color: T.text },
            ].map(item => (
              <div key={item.label} style={{
                background: T.s2, padding: '0.65rem', borderRadius: 8, textAlign: 'center',
                border: `0.5px solid ${T.border}`,
              }}>
                <div style={{ fontSize: '0.95rem', fontWeight: 700, color: item.color, fontVariantNumeric: 'tabular-nums' }}>
                  {item.value}
                </div>
                <div style={{ fontSize: '0.6rem', color: T.dim, marginTop: 2 }}>{item.label}</div>
              </div>
            ))}
          </div>
        )}

        <div style={{ fontSize: '0.65rem', color: T.dim, textAlign: 'center' }}>
          Rates are indicative. Actual rates depend on bank and credit profile.
        </div>
      </div>
    </div>
  )
}

export default function FundingPage({ onBack }) {
  const [schemes,    setSchemes]    = useState([])
  const [schemsLoad, setSchemsLoad] = useState(true)
  const [tab,        setTab]        = useState('browse')
  const [searchForm, setSearchForm] = useState({
    capital_gap: 100000, is_woman: false, caste_category: 'general', business_type: '',
  })
  const [matched,   setMatched]   = useState([])
  const [searched,  setSearched]  = useState(false)
  const [findLoad,  setFindLoad]  = useState(false)
  const [calcScheme,setCalcScheme]= useState(null)
  const [error,     setError]     = useState('')

  const sf = (k, v) => setSearchForm(f => ({ ...f, [k]: v }))

  useEffect(() => {
    fetch(`${API}/api/funding/schemes`)
      .then(r => r.json())
      .then(d => setSchemes(d.schemes || []))
      .catch(() => {})
      .finally(() => setSchemsLoad(false))
  }, [])

  const findSchemes = async () => {
    setFindLoad(true); setError('')
    try {
      const res = await fetch(`${API}/api/funding/find`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...searchForm, capital_gap: parseFloat(searchForm.capital_gap) }),
      })
      const d = await res.json()
      setMatched(d.matched_schemes || [])
      setSearched(true)
    } catch (e) { setError(e.message) }
    finally { setFindLoad(false) }
  }

  return (
    <div className="fade-in">
      <PageHeader
        icon="💰"
        title="Funding Finder"
        sub="12+ government schemes · Live EMI calculator · Eligibility check"
        color={T.teal}
        onBack={onBack}
      />

      <div className="page-wrap">
        {/* Stats */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(110px,1fr))', gap: '0.5rem', marginBottom: '1.5rem' }}>
          <Stat label="Total Schemes" value="12+"     color={T.teal} />
          <Stat label="Max Loan"      value="₹50 Cr"  color={T.gold} />
          <Stat label="Min Rate"      value="0%"       color={T.orange} />
          <Stat label="No Collateral" value="7 Schemes" color={T.purple} />
        </div>

        <Tabs
          tabs={[['browse', '📋 Browse All Schemes'], ['find', '🎯 Find My Scheme']]}
          active={tab}
          onChange={setTab}
        />
        <div style={{ marginTop: '1.25rem' }}>

          {/* ── Browse ───────────────────────────────────────────── */}
          {tab === 'browse' && (
            <div>
              {schemsLoad
                ? [0,1,2,3].map(i => <SkeletonCard key={i} />)
                : schemes.length === 0
                  ? <Empty icon="📋" title="Loading schemes…" sub="Connecting to server" />
                  : schemes.map(s => <SchemeCard key={s.id} scheme={s} onCalc={setCalcScheme} />)
              }
            </div>
          )}

          {/* ── Find ─────────────────────────────────────────────── */}
          {tab === 'find' && (
            <div>
              <Card style={{ marginBottom: '1.25rem' }}>
                <div style={{ fontSize: '0.88rem', fontWeight: 600, color: T.text, marginBottom: '1.1rem' }}>
                  Find the right scheme for you
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(175px,1fr))', gap: '0.9rem', marginBottom: '1rem' }}>
                  <Field
                    label="Capital Gap (₹)"
                    value={searchForm.capital_gap}
                    onChange={e => sf('capital_gap', e.target.value)}
                    type="number"
                    hint="How much more do you need?"
                  />
                  <SelectField
                    label="Category"
                    value={searchForm.caste_category}
                    onChange={e => sf('caste_category', e.target.value)}
                  >
                    <option value="general">General</option>
                    <option value="obc">OBC</option>
                    <option value="sc">SC</option>
                    <option value="st">ST</option>
                  </SelectField>
                  <Field
                    label="Business Type (optional)"
                    value={searchForm.business_type}
                    onChange={e => sf('business_type', e.target.value)}
                    placeholder="e.g. grocery, salon"
                  />
                </div>
                <label style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: '1rem', cursor: 'pointer', userSelect: 'none' }}>
                  <input
                    type="checkbox" checked={searchForm.is_woman}
                    onChange={e => sf('is_woman', e.target.checked)}
                    style={{ accentColor: T.orange, width: 15, height: 15 }}
                  />
                  <span style={{ fontSize: '0.82rem', color: T.muted }}>
                    Woman entrepreneur — unlocks Mahila Udyam Nidhi & Stand Up India
                  </span>
                </label>
                {error && <Alert type="error" style={{ marginBottom: '0.75rem' }}>{error}</Alert>}
                <Btn variant="primary" size="lg" full disabled={findLoad} onClick={findSchemes} icon="🎯">
                  {findLoad ? 'Finding best schemes…' : 'Find My Best Schemes'}
                </Btn>
              </Card>

              {findLoad && [0,1].map(i => <SkeletonCard key={i} />)}

              {searched && !findLoad && matched.length === 0 && (
                <Empty
                  icon="🔍"
                  title="No exact matches"
                  sub="Try reducing the capital gap or browse all schemes."
                />
              )}

              {searched && !findLoad && matched.length > 0 && (
                <div>
                  <SectionTitle
                    title="Matched Schemes"
                    sub={`${matched.length} schemes eligible for your profile`}
                  />
                  {matched.map(s => <SchemeCard key={s.id} scheme={s} onCalc={setCalcScheme} />)}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {calcScheme && <EMIModal scheme={calcScheme} onClose={() => setCalcScheme(null)} />}
    </div>
  )
}
