import { useState, useEffect, useRef } from 'react'
import {
  T, Card, Stat, Tabs, Badge, Alert, Btn, Field, SelectField,
  Skeleton, SkeletonCard, SectionTitle, Divider, PageHeader,
  UrgencyBadge, fmt,
} from '../components/UI.jsx'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function LocationBanner({ data }) {
  if (!data) return null
  return (
    <div style={{
      background: `${T.teal}0a`,
      border: `0.5px solid ${T.teal}30`,
      borderRadius: 9,
      padding: '0.7rem 1rem',
      marginBottom: '1rem',
      display: 'flex',
      gap: '0.8rem',
      flexWrap: 'wrap',
      alignItems: 'center',
    }}>
      <span style={{ fontSize: '0.78rem', color: T.teal, fontWeight: 500 }}>
        📍 {data.city}{data.district ? `, ${data.district}` : ''} · {data.state}
      </span>
      {data.population && (
        <span style={{ fontSize: '0.7rem', color: T.muted }}>
          Pop: {(data.population / 1000).toFixed(0)}K
        </span>
      )}
      {data.city_tier && (
        <Badge color={data.city_tier === 'metro' ? T.orange : T.teal}>
          {data.city_tier}
        </Badge>
      )}
      {data.literacy_rate && (
        <span style={{ fontSize: '0.7rem', color: T.muted }}>
          Literacy {Math.round(data.literacy_rate * 100)}%
        </span>
      )}
      {data.age_dominant && (
        <span style={{ fontSize: '0.7rem', color: T.muted }}>
          Age: {data.age_dominant}
        </span>
      )}
    </div>
  )
}

function BusinessCard({ biz, rank }) {
  const [expanded, setExpanded] = useState(false)
  const isBest = rank === 0
  return (
    <Card
      highlight={isBest ? T.orange : undefined}
      style={{ marginBottom: '0.75rem' }}
    >
      {isBest && (
        <div style={{
          fontSize: '0.6rem', color: T.orange,
          letterSpacing: '0.15em', textTransform: 'uppercase',
          marginBottom: 8,
        }}>
          ★ Best Match
        </div>
      )}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        flexWrap: 'wrap',
        gap: 8,
        marginBottom: 12,
      }}>
        <div>
          <div style={{
            fontSize: '0.95rem', fontWeight: 600, color: T.text,
            textTransform: 'capitalize', letterSpacing: '0.02em',
          }}>
            {biz.business_type.replace(/_/g, ' ')}
          </div>
          {biz.location_advice && (
            <div style={{ fontSize: '0.75rem', color: T.teal, marginTop: 4 }}>
              📍 {biz.location_advice}
            </div>
          )}
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{
            fontSize: '1.4rem', fontWeight: 700,
            color: T.gold, fontFamily: T.serif,
            fontVariantNumeric: 'tabular-nums',
          }}>
            {Math.round((biz.match_score || 0) * 100)}%
          </div>
          <div style={{ fontSize: '0.6rem', color: T.muted }}>match score</div>
        </div>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit,minmax(110px,1fr))',
        gap: '0.5rem',
        marginBottom: 10,
      }}>
        <Stat label="Monthly Revenue"  value={fmt(biz.monthly_revenue)}   color={T.teal} />
        <Stat label="Capital Needed"   value={fmt(biz.capital_needed)}    />
        <Stat label="Capital Gap"      value={biz.capital_gap > 0 ? fmt(biz.capital_gap) : 'None'}
              color={biz.capital_gap > 0 ? T.red : T.green} />
        <Stat label="Success Rate"
              value={biz.success_probability?.split(' ').slice(0,2).join(' ')}
              color={T.teal} />
      </div>

      {/* Funding schemes */}
      {biz.funding_schemes?.length > 0 && (
        <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginBottom: 8 }}>
          {biz.funding_schemes.slice(0, 3).map((s, j) => (
            <Badge key={j} color={T.teal}>💰 {s}</Badge>
          ))}
        </div>
      )}

      {/* Expand toggle */}
      <button
        onClick={() => setExpanded(!expanded)}
        style={{
          background: 'transparent', border: 'none',
          color: T.muted, fontSize: '0.72rem',
          cursor: 'pointer', fontFamily: T.ff,
          padding: 0, textDecoration: 'underline',
        }}
      >
        {expanded ? '▲ Less detail' : '▼ Setup steps & more'}
      </button>

      {expanded && (
        <div style={{ marginTop: 10, paddingTop: 10, borderTop: `0.5px solid ${T.border}` }}>
          {biz.setup_steps?.length > 0 && (
            <div style={{ marginBottom: 8 }}>
              <div style={{ fontSize: '0.65rem', color: T.dim, letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 5 }}>
                Setup Steps
              </div>
              {biz.setup_steps.map((s, j) => (
                <div key={j} style={{ fontSize: '0.78rem', color: T.muted, marginBottom: 3, display: 'flex', gap: 6 }}>
                  <span style={{ color: T.teal, flexShrink: 0 }}>✓</span>
                  <span>{s}</span>
                </div>
              ))}
            </div>
          )}
          {biz.risk_factors?.length > 0 && (
            <div>
              <div style={{ fontSize: '0.65rem', color: T.dim, letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 5 }}>
                Risk Factors
              </div>
              {biz.risk_factors.slice(0, 2).map((r, j) => (
                <div key={j} style={{ fontSize: '0.75rem', color: T.muted, marginBottom: 3, display: 'flex', gap: 6 }}>
                  <span style={{ color: '#f08040', flexShrink: 0 }}>⚠</span>
                  <span>{r}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </Card>
  )
}

function CityResults({ data }) {
  if (!data) return null
  const entries = Object.entries(data.results || {})
  return (
    <div>
      <div style={{ fontSize: '0.72rem', color: T.muted, marginBottom: '1rem' }}>
        {entries.length} pin codes scanned
      </div>
      {entries.map(([pin, d]) => (
        <Card key={pin} style={{ marginBottom: '0.75rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 8, marginBottom: 10 }}>
            <div>
              <div style={{ fontWeight: 600, color: T.text, fontSize: '0.9rem' }}>
                Pin Code {pin}
              </div>
              <div style={{ fontSize: '0.72rem', color: T.muted }}>
                {d.city || 'Area'}
              </div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '1.3rem', fontWeight: 700, color: T.gold, fontFamily: T.serif }}>
                {d.opportunity_score}
              </div>
              <div style={{ fontSize: '0.6rem', color: T.dim }}>score</div>
            </div>
          </div>
          <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
            {d.top_gaps?.slice(0, 4).map((gap, j) => (
              <UrgencyBadge key={j} urgency={gap.urgency} />
            ))}
            {d.top_gaps?.slice(0, 4).map((gap, j) => (
              <Badge key={`biz-${j}`} color={T.muted}>
                {gap.type?.replace(/_/g, ' ')} · {fmt(gap.revenue)}
              </Badge>
            ))}
          </div>
        </Card>
      ))}
    </div>
  )
}

export default function OpportunityPage({ onBack }) {
  const [tab, setTab] = useState('scan')
  const [form, setForm] = useState({
    name: '', pincode: '', capital: '', skills: 'any',
    isWoman: false, caste: 'general', risk: 'medium',
  })
  const [result, setResult] = useState(null)
  const [locationData, setLocationData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [cityData, setCityData] = useState(null)
  const [cityLoading, setCityLoading] = useState(false)
  const [pincodeSearch, setPincodeSearch] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const suggestRef = useRef(null)

  useEffect(() => {
    const handler = (e) => {
      if (suggestRef.current && !suggestRef.current.contains(e.target)) {
        setSuggestions([])
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const searchPincode = async (q) => {
    setPincodeSearch(q)
    set('pincode', q)
    if (q.length < 3) { setSuggestions([]); return }
    try {
      const res = await fetch(`${API}/api/location/suggest/${q}`)
      const data = await res.json()
      setSuggestions(data.suggestions || [])
    } catch { setSuggestions([]) }
  }

  const scan = async () => {
    if (!form.pincode) { setError('Enter a pin code'); return }
    if (!form.capital) { setError('Enter your available capital'); return }
    setLoading(true); setError(''); setResult(null); setLocationData(null)
    try {
      const [scanRes, locRes] = await Promise.all([
        fetch(`${API}/api/opportunity/scan`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            pincode: form.pincode,
            capital: parseFloat(form.capital),
            skills: form.skills.split(',').map(s => s.trim()).filter(Boolean),
            is_woman: form.isWoman,
            caste_category: form.caste,
            risk_appetite: form.risk,
            name: form.name || 'User',
          }),
        }),
        fetch(`${API}/api/location/pincode/${form.pincode}`).catch(() => null),
      ])
      if (!scanRes.ok) {
        const d = await scanRes.json()
        throw new Error(d.detail || 'Scan failed')
      }
      const [scanData] = await Promise.all([
        scanRes.json(),
      ])
      setResult(scanData)
      if (locRes?.ok) setLocationData(await locRes.json())
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const scanCity = async (city) => {
    setCityLoading(true); setCityData(null)
    try {
      const res = await fetch(`${API}/api/opportunity/city/${city}`)
      setCityData(await res.json())
    } catch (e) {
      setError(e.message)
    } finally {
      setCityLoading(false)
    }
  }

  return (
    <div className="fade-in">
      <PageHeader
        icon="🔍"
        title="Find My Opportunity"
        sub="Scan any pin code · Match your profile · Discover business gaps"
        color={T.orange}
        onBack={onBack}
      />

      <div className="page-wrap">
        <Tabs
          tabs={[['scan', '🎯 Personal Scan'], ['city', '🏙️ City Map']]}
          active={tab}
          onChange={setTab}
        />
        <div style={{ marginTop: '1.25rem' }}>

          {/* ── Personal Scan ─────────────────────────────────────── */}
          {tab === 'scan' && (
            <div>
              <Card style={{ marginBottom: '1.25rem' }}>
                <div style={{ fontSize: '0.85rem', fontWeight: 600, color: T.text, marginBottom: '1.2rem' }}>
                  Tell us about yourself
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(175px,1fr))', gap: '1rem', marginBottom: '1rem' }}>
                  <Field
                    label="Your Name"
                    value={form.name}
                    onChange={e => set('name', e.target.value)}
                    placeholder="e.g. Raju Kumar"
                  />
                  <div style={{ position: 'relative' }} ref={suggestRef}>
                    <Field
                      label="Pin Code"
                      value={pincodeSearch}
                      onChange={e => searchPincode(e.target.value)}
                      placeholder="e.g. 560037"
                      required
                      onKeyDown={e => e.key === 'Escape' && setSuggestions([])}
                    />
                    {suggestions.length > 0 && (
                      <div style={{
                        position: 'absolute', top: '100%', left: 0, right: 0,
                        background: T.s2, border: `0.5px solid ${T.border}`,
                        borderRadius: 8, zIndex: 50,
                        marginTop: 4, overflow: 'hidden',
                        boxShadow: '0 8px 24px #00000080',
                      }}>
                        {suggestions.map((s, i) => (
                          <button
                            key={i}
                            onClick={() => {
                              set('pincode', s.pincode)
                              setPincodeSearch(s.pincode)
                              setSuggestions([])
                            }}
                            style={{
                              width: '100%', textAlign: 'left',
                              padding: '0.55rem 0.85rem',
                              background: 'transparent',
                              border: 'none', borderBottom: i < suggestions.length - 1 ? `0.5px solid ${T.border}` : 'none',
                              color: T.text, cursor: 'pointer', fontFamily: T.ff, fontSize: '0.8rem',
                            }}
                            onMouseEnter={e => e.currentTarget.style.background = T.s3}
                            onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                          >
                            <span style={{ color: T.orange, fontVariantNumeric: 'tabular-nums' }}>{s.pincode}</span>
                            {' — '}
                            <span>{s.city}</span>
                            <span style={{ color: T.dim, fontSize: '0.72rem' }}>{', '}{s.state}</span>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                  <Field
                    label="Capital Available (₹)"
                    value={form.capital}
                    onChange={e => set('capital', e.target.value)}
                    type="number"
                    placeholder="e.g. 50000"
                    required
                    hint="Startup budget you can invest"
                  />
                  <Field
                    label="Your Skills"
                    value={form.skills}
                    onChange={e => set('skills', e.target.value)}
                    placeholder="cooking, selling, any"
                    hint="Comma-separated or 'any'"
                  />
                  <SelectField
                    label="Risk Appetite"
                    value={form.risk}
                    onChange={e => set('risk', e.target.value)}
                  >
                    <option value="low">Low — Safe & steady</option>
                    <option value="medium">Medium — Balanced</option>
                    <option value="high">High — Growth focused</option>
                  </SelectField>
                  <SelectField
                    label="Category"
                    value={form.caste}
                    onChange={e => set('caste', e.target.value)}
                  >
                    <option value="general">General</option>
                    <option value="obc">OBC</option>
                    <option value="sc">SC</option>
                    <option value="st">ST</option>
                  </SelectField>
                </div>

                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', userSelect: 'none' }}>
                    <input
                      type="checkbox" checked={form.isWoman}
                      onChange={e => set('isWoman', e.target.checked)}
                      style={{ accentColor: T.orange, width: 15, height: 15 }}
                    />
                    <span style={{ fontSize: '0.82rem', color: T.muted }}>
                      Woman entrepreneur — unlocks Mahila Udyam Nidhi & Stand Up India
                    </span>
                  </label>
                </div>

                {error && <Alert type="error" style={{ marginBottom: '0.75rem' }}>{error}</Alert>}

                <Btn
                  variant="primary"
                  size="lg"
                  full
                  disabled={loading}
                  onClick={scan}
                  icon={loading ? undefined : '🚀'}
                >
                  {loading ? 'Reading India pulse…' : 'Find My Opportunity'}
                </Btn>
              </Card>

              {/* Loading skeleton */}
              {loading && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                  <SkeletonCard />
                  <SkeletonCard />
                </div>
              )}

              {/* Results */}
              {result && !loading && (
                <div className="fade-in">
                  <LocationBanner data={locationData} />

                  {/* Summary card */}
                  <Card style={{ marginBottom: '1.25rem' }}>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'flex-start',
                      flexWrap: 'wrap',
                      gap: '1rem',
                      marginBottom: '1rem',
                    }}>
                      <div>
                        <div style={{ fontSize: '1.3rem', fontWeight: 700, color: T.orange, fontFamily: T.serif }}>
                          {result.city}
                        </div>
                        <div style={{ color: T.muted, fontSize: '0.78rem', marginTop: 3 }}>
                          {result.state} · Pin {result.pincode} · Pop {result.population?.toLocaleString()}
                        </div>
                        {result.message_hindi && (
                          <div style={{ color: T.teal, fontSize: '0.78rem', marginTop: 6 }}>
                            {result.message_hindi}
                          </div>
                        )}
                      </div>
                      <div style={{
                        textAlign: 'center',
                        background: T.s2,
                        padding: '1rem 1.25rem',
                        borderRadius: 10,
                        minWidth: 90,
                        border: `0.5px solid ${T.border}`,
                      }}>
                        <div style={{ fontSize: '2rem', fontWeight: 700, color: T.gold, fontFamily: T.serif, fontVariantNumeric: 'tabular-nums' }}>
                          {result.opportunity_score}
                        </div>
                        <div style={{ fontSize: '0.58rem', color: T.dim, textTransform: 'uppercase', letterSpacing: '0.1em' }}>
                          Opportunity Score
                        </div>
                      </div>
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(110px,1fr))', gap: '0.5rem' }}>
                      <Stat label="Income Level" value={result.income_tier?.replace('_', ' ')} color={T.teal} />
                      <Stat label="Gaps Found" value={`${result.top_gaps?.length || 0}+`} />
                      <Stat label="Matches" value={result.matched_businesses?.length || 0} />
                      <Stat label="Population" value={`${((result.population||0) / 1000).toFixed(0)}K`} />
                    </div>
                  </Card>

                  {/* Business matches */}
                  {result.matched_businesses?.length > 0 && (
                    <div>
                      <SectionTitle title="Your Best Matches" sub={`${result.matched_businesses.length} opportunities ranked by fit`} />
                      {result.matched_businesses.map((biz, i) => (
                        <BusinessCard key={i} biz={biz} rank={i} />
                      ))}
                    </div>
                  )}

                  {/* Market gaps */}
                  {result.top_gaps?.length > 0 && (
                    <div>
                      <SectionTitle title="Market Gaps Identified" sub="Unmet demand in your pin code" />
                      <Card>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                          {result.top_gaps.map((g, i) => (
                            <div key={i} style={{
                              background: T.s2,
                              border: `0.5px solid ${T.border}`,
                              borderRadius: 7,
                              padding: '0.4rem 0.7rem',
                              display: 'flex',
                              flexDirection: 'column',
                              gap: 3,
                            }}>
                              <span style={{ fontSize: '0.78rem', color: T.text, textTransform: 'capitalize' }}>
                                {g.business_type?.replace(/_/g, ' ')}
                              </span>
                              <div style={{ display: 'flex', gap: 4 }}>
                                <span style={{ fontSize: '0.65rem', color: T.teal }}>{fmt(g.monthly_revenue)}/mo</span>
                                <UrgencyBadge urgency={g.urgency} />
                              </div>
                            </div>
                          ))}
                        </div>
                      </Card>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* ── City Map ──────────────────────────────────────────── */}
          {tab === 'city' && (
            <div>
              <Card style={{ marginBottom: '1.25rem' }}>
                <div style={{ fontSize: '0.85rem', fontWeight: 600, color: T.text, marginBottom: '1rem' }}>
                  Scan an entire city
                </div>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  {['bangalore', 'mumbai', 'delhi', 'hyderabad', 'chennai', 'pune', 'ahmedabad', 'kolkata'].map(city => (
                    <Btn
                      key={city}
                      variant="ghost"
                      size="sm"
                      onClick={() => scanCity(city)}
                      disabled={cityLoading}
                    >
                      {city.charAt(0).toUpperCase() + city.slice(1)}
                    </Btn>
                  ))}
                </div>
              </Card>

              {cityLoading && (
                <div style={{ textAlign: 'center', padding: '2rem', color: T.muted, fontSize: '0.85rem' }}>
                  <span className="pulse">Scanning city pulse…</span>
                </div>
              )}

              {cityData && <CityResults data={cityData} />}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
