import { useState } from 'react'
import {
  T, Card, Stat, Tabs, Badge, Alert, Btn, Field, SelectField,
  Skeleton, SkeletonCard, SectionTitle, Divider, PageHeader,
  PriorityBadge, ScoreRing, CheckCard, fmt, Empty,
} from '../components/UI.jsx'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const EDUCATION_OPTIONS = [
  ['no_schooling','No Schooling'],    ['primary','Primary (1–4)'],
  ['5th','5th Pass'],                 ['8th','8th Pass'],
  ['10th','10th / SSC'],             ['12th','12th / HSC'],
  ['diploma','Diploma / ITI'],       ['graduate','Graduate'],
  ['post_graduate','Post Graduate'], ['professional','Professional (MBBS/CA/LLB)'],
]

const SKILLS_LIST = [
  { key: 'cooking',    label: 'Cooking / Food',   icon: '🍳' },
  { key: 'tailoring',  label: 'Tailoring',         icon: '🧵' },
  { key: 'selling',    label: 'Sales / Trading',   icon: '🤝' },
  { key: 'repair',     label: 'Repair / Mechanic', icon: '🔧' },
  { key: 'teaching',   label: 'Teaching',           icon: '📚' },
  { key: 'beauty',     label: 'Beauty / Salon',    icon: '💅' },
  { key: 'health',     label: 'Healthcare',         icon: '🩺' },
  { key: 'computers',  label: 'Computers / IT',    icon: '💻' },
  { key: 'farming',    label: 'Agriculture',        icon: '🌾' },
  { key: 'driving',    label: 'Driving',            icon: '🚗' },
  { key: 'accounting', label: 'Accounts / Finance',icon: '📊' },
  { key: 'any',        label: 'No specific skill', icon: '⭕' },
]

const LANG_OPTIONS = [
  'Hindi','English','Tamil','Telugu','Kannada','Malayalam',
  'Marathi','Bengali','Gujarati','Punjabi','Odia','Urdu',
]

// ─── Career Path Card ─────────────────────────────────────────────────────────
function PathCard({ path, rank }) {
  const isBest = rank === 0
  return (
    <Card highlight={isBest ? T.purple : undefined} style={{ marginBottom: '0.75rem' }}>
      {isBest && (
        <div style={{ fontSize: '0.6rem', color: T.purple, letterSpacing: '0.15em', textTransform: 'uppercase', marginBottom: 8 }}>
          ★ Best Match
        </div>
      )}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 8, marginBottom: 10 }}>
        <div>
          <div style={{ fontSize: '0.95rem', fontWeight: 600, color: T.text }}>{path.path_name}</div>
        </div>
        <div style={{ textAlign: 'right', flexShrink: 0 }}>
          <div style={{ fontSize: '1.1rem', fontWeight: 700, color: T.teal, fontVariantNumeric: 'tabular-nums' }}>
            {fmt(path.expected_monthly_income)}/mo
          </div>
          <div style={{ fontSize: '0.62rem', color: T.dim }}>{path.success_rate} success</div>
        </div>
      </div>

      <div style={{ fontSize: '0.78rem', color: T.muted, lineHeight: 1.7, marginBottom: 10 }}>
        {path.description}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '0.5rem', marginBottom: 10 }}>
        <Stat label="Capital"  value={fmt(path.capital_needed)}     color={T.gold} />
        <Stat label="Timeline" value={`${path.timeline_months}m`}  color={T.teal} />
        <Stat label="Success"  value={path.success_rate}             color={T.orange} />
      </div>

      {path.first_steps?.length > 0 && (
        <div>
          <div style={{ fontSize: '0.65rem', color: T.dim, letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 5 }}>First Steps</div>
          {path.first_steps.slice(0,3).map((s, j) => (
            <div key={j} style={{ fontSize: '0.75rem', color: T.muted, marginBottom: 3, display: 'flex', gap: 6 }}>
              <span style={{ color: T.teal, flexShrink: 0 }}>✓</span>{s}
            </div>
          ))}
        </div>
      )}

      {path.risks?.[0] && (
        <div style={{ marginTop: 8, fontSize: '0.72rem', color: '#f08040', display: 'flex', gap: 5 }}>
          <span>⚠</span><span>{path.risks[0]}</span>
        </div>
      )}
    </Card>
  )
}

export default function IdentityPage({ onBack }) {
  const [form, setForm] = useState({
    name: '', age: 28, gender: 'male', education: '10th',
    occupation: 'unemployed', pincode: '110001', state: 'Delhi',
    languages: ['Hindi'], skills: [], capital: 50000,
    is_woman: false, caste_category: 'general', has_space: false, risk_appetite: 'medium',
  })
  const [result,    setResult]    = useState(null)
  const [loading,   setLoading]   = useState(false)
  const [error,     setError]     = useState('')
  const [activeTab, setActiveTab] = useState('paths')

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const toggleSkill = (sk) => setForm(f => {
    const has = f.skills.includes(sk)
    const next = has ? f.skills.filter(s => s !== sk) : [...f.skills.filter(s => s !== 'any'), sk]
    return { ...f, skills: next.length === 0 ? ['any'] : next }
  })

  const toggleLang = (lang) => setForm(f => {
    const has = f.languages.includes(lang)
    const next = has ? f.languages.filter(l => l !== lang) : [...f.languages, lang]
    return { ...f, languages: next.length === 0 ? ['Hindi'] : next }
  })

  const analyse = async () => {
    if (!form.name.trim()) { setError('Enter your name'); return }
    setLoading(true); setError(''); setResult(null)
    try {
      const res = await fetch(`${API}/api/identity/analyse`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          skills: form.skills.length > 0 ? form.skills : ['any'],
          age: parseInt(form.age),
          capital: parseFloat(form.capital),
        }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Analysis failed')
      setResult(data)
      setActiveTab('paths')
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <div className="fade-in">
      <PageHeader
        icon="👤"
        title="Identity Profiler"
        sub="Full opportunity analysis · Scheme eligibility · Career paths · Skill gaps"
        color={T.purple}
        onBack={onBack}
      />

      <div className="page-wrap">
        {/* ── Profile form ───────────────────────────────────────────── */}
        {!result && (
          <Card style={{ marginBottom: '1.25rem' }}>
            <div style={{ fontSize: '0.88rem', fontWeight: 600, color: T.text, marginBottom: '1.1rem' }}>
              Your Profile
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(175px,1fr))', gap: '0.9rem', marginBottom: '1rem' }}>
              <Field
                label="Full Name"
                value={form.name}
                onChange={e => set('name', e.target.value)}
                placeholder="e.g. Sunita Devi"
                required
              />
              <Field
                label="Age"
                value={form.age}
                onChange={e => set('age', e.target.value)}
                type="number" min={15} max={80}
              />
              <SelectField
                label="Gender"
                value={form.gender}
                onChange={e => {
                  set('gender', e.target.value)
                  if (e.target.value === 'female') set('is_woman', true)
                }}
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </SelectField>
              <SelectField
                label="Education"
                value={form.education}
                onChange={e => set('education', e.target.value)}
              >
                {EDUCATION_OPTIONS.map(([k, l]) => <option key={k} value={k}>{l}</option>)}
              </SelectField>
              <Field
                label="Current Occupation"
                value={form.occupation}
                onChange={e => set('occupation', e.target.value)}
                placeholder="e.g. daily wage / housewife"
              />
              <Field
                label="Pin Code"
                value={form.pincode}
                onChange={e => set('pincode', e.target.value)}
                placeholder="e.g. 560037"
              />
              <Field
                label="State"
                value={form.state}
                onChange={e => set('state', e.target.value)}
                placeholder="e.g. Karnataka"
              />
              <Field
                label="Available Capital (₹)"
                value={form.capital}
                onChange={e => set('capital', e.target.value)}
                type="number"
                hint="Investment budget"
              />
              <SelectField
                label="Category"
                value={form.caste_category}
                onChange={e => set('caste_category', e.target.value)}
              >
                <option value="general">General</option>
                <option value="obc">OBC</option>
                <option value="sc">SC</option>
                <option value="st">ST</option>
                <option value="minority">Minority</option>
              </SelectField>
              <SelectField
                label="Risk Appetite"
                value={form.risk_appetite}
                onChange={e => set('risk_appetite', e.target.value)}
              >
                <option value="low">Low — Safe &amp; Steady</option>
                <option value="medium">Medium — Balanced</option>
                <option value="high">High — Growth First</option>
              </SelectField>
            </div>

            <Divider label="Skills" />
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(130px,1fr))', gap: '0.4rem', marginBottom: '1rem' }}>
              {SKILLS_LIST.map(s => {
                const active = form.skills.includes(s.key)
                return (
                  <button
                    key={s.key}
                    onClick={() => toggleSkill(s.key)}
                    style={{
                      padding: '0.5rem 0.4rem', borderRadius: 7, border: '0.5px solid',
                      cursor: 'pointer', textAlign: 'center', fontSize: '0.72rem',
                      background: active ? `${T.purple}18` : T.s2,
                      color: active ? T.purple : T.muted,
                      borderColor: active ? `${T.purple}80` : T.border,
                      fontFamily: T.ff,
                      transition: 'all 0.15s',
                    }}
                  >
                    <div style={{ fontSize: '1rem', marginBottom: 2 }}>{s.icon}</div>
                    {s.label}
                  </button>
                )
              })}
            </div>

            <Divider label="Languages" />
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginBottom: '1rem' }}>
              {LANG_OPTIONS.map(l => {
                const active = form.languages.includes(l)
                return (
                  <button
                    key={l}
                    onClick={() => toggleLang(l)}
                    style={{
                      padding: '0.3rem 0.75rem', borderRadius: 5, border: '0.5px solid',
                      cursor: 'pointer', fontSize: '0.75rem', fontFamily: T.ff,
                      background: active ? `${T.teal}15` : T.s2,
                      color: active ? T.teal : T.muted,
                      borderColor: active ? `${T.teal}60` : T.border,
                      transition: 'all 0.15s',
                    }}
                  >
                    {l}
                  </button>
                )
              })}
            </div>

            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '1.1rem' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', userSelect: 'none' }}>
                <input
                  type="checkbox" checked={form.is_woman}
                  onChange={e => set('is_woman', e.target.checked)}
                  style={{ accentColor: T.orange, width: 15, height: 15 }}
                />
                <span style={{ fontSize: '0.82rem', color: T.muted }}>Woman entrepreneur</span>
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', userSelect: 'none' }}>
                <input
                  type="checkbox" checked={form.has_space}
                  onChange={e => set('has_space', e.target.checked)}
                  style={{ accentColor: T.orange, width: 15, height: 15 }}
                />
                <span style={{ fontSize: '0.82rem', color: T.muted }}>Have physical space</span>
              </label>
            </div>

            {error && <Alert type="error" style={{ marginBottom: '0.75rem' }}>{error}</Alert>}

            <Btn
              variant="primary"
              size="lg"
              full
              disabled={loading}
              onClick={analyse}
              icon="🧠"
              style={{ background: loading ? T.s2 : `linear-gradient(135deg,${T.purple},${T.orange})` }}
            >
              {loading ? 'Analysing your profile…' : 'Analyse My Opportunities'}
            </Btn>
          </Card>
        )}

        {/* Loading */}
        {loading && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            <SkeletonCard />
            <SkeletonCard />
          </div>
        )}

        {/* ── Results ──────────────────────────────────────────────── */}
        {result && !loading && (
          <div className="fade-in">
            {/* Score summary */}
            <Card style={{ marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem' }}>
                <div>
                  <div style={{ fontSize: '1.3rem', fontWeight: 700, color: T.purple }}>{result.name}</div>
                  <div style={{ fontSize: '0.78rem', color: T.muted, marginTop: 3 }}>
                    {result.entrepreneurship_readiness}
                  </div>
                  {result.hindi_summary && (
                    <div style={{ fontSize: '0.75rem', color: T.teal, marginTop: 6 }}>
                      {result.hindi_summary}
                    </div>
                  )}
                </div>
                <div style={{ display: 'flex', gap: '1rem', flexShrink: 0 }}>
                  <ScoreRing score={result.opportunity_score}      label="Opportunity" color={T.orange} />
                  <ScoreRing score={result.digital_literacy_score} label="Digital"     color={T.teal} />
                </div>
              </div>

              {result.summary && (
                <div style={{
                  padding: '0.75rem',
                  background: T.s2,
                  borderRadius: 8,
                  fontSize: '0.8rem',
                  color: T.muted,
                  lineHeight: 1.7,
                  marginBottom: '0.75rem',
                }}>
                  {result.summary}
                </div>
              )}

              <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8 }}>
                <div>
                  <span style={{ fontSize: '0.68rem', color: T.dim }}>Economic Tier: </span>
                  <span style={{ fontSize: '0.8rem', color: T.gold }}>
                    {result.economic_tier?.replace('_', ' ')}
                  </span>
                </div>
                <div>
                  <span style={{ fontSize: '0.68rem', color: T.dim }}>Income Potential: </span>
                  <span style={{ fontSize: '0.88rem', fontWeight: 600, color: T.teal, fontVariantNumeric: 'tabular-nums' }}>
                    {fmt(result.monthly_income_potential)}/mo
                  </span>
                </div>
              </div>

              <div style={{ marginTop: '0.75rem' }}>
                <Btn variant="ghost" size="sm" onClick={() => setResult(null)}>
                  ← Edit Profile
                </Btn>
              </div>
            </Card>

            {/* Tab navigation */}
            <Tabs
              tabs={[
                ['paths',   '🛤️ Career Paths'],
                ['schemes', '🏛️ Schemes'],
                ['gaps',    '📈 Skill Gaps'],
                ['actions', '⚡ Actions'],
              ]}
              active={activeTab}
              onChange={setActiveTab}
            />
            <div style={{ marginTop: '1.25rem' }}>

              {/* Career Paths */}
              {activeTab === 'paths' && (
                <div>
                  {result.recommended_paths?.length > 0
                    ? result.recommended_paths.map((p, i) => <PathCard key={i} path={p} rank={i} />)
                    : <Empty icon="🛤️" title="No paths found" sub="Try adjusting your profile" />
                  }
                </div>
              )}

              {/* Schemes */}
              {activeTab === 'schemes' && (
                <div>
                  {result.government_eligibilities?.map((g, i) => (
                    <Card
                      key={i}
                      highlight={g.eligible ? T.teal : undefined}
                      style={{ marginBottom: '0.75rem', opacity: g.eligible ? 1 : 0.65 }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 8, marginBottom: 6 }}>
                        <div style={{ flex: 1 }}>
                          <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap', marginBottom: 3 }}>
                            <span style={{ fontSize: '0.9rem', fontWeight: 600, color: g.eligible ? T.text : T.muted }}>
                              {g.scheme_name}
                            </span>
                            <PriorityBadge priority={g.priority} />
                            {!g.eligible && (
                              <Badge color={T.red}>Not eligible</Badge>
                            )}
                          </div>
                          <div style={{ fontSize: '0.68rem', color: T.dim }}>{g.ministry}</div>
                        </div>
                        <div style={{ fontSize: '0.88rem', fontWeight: 600, color: T.gold, fontVariantNumeric: 'tabular-nums' }}>
                          {g.max_benefit}
                        </div>
                      </div>
                      <div style={{ fontSize: '0.75rem', color: T.muted, marginBottom: 6 }}>{g.reason}</div>
                      {g.eligible && g.action_required && (
                        <div style={{
                          padding: '0.5rem 0.75rem',
                          background: `${T.teal}0a`,
                          border: `0.5px solid ${T.teal}30`,
                          borderRadius: 7,
                          fontSize: '0.75rem',
                          color: T.teal,
                        }}>
                          → {g.action_required}
                        </div>
                      )}
                    </Card>
                  ))}
                </div>
              )}

              {/* Skill Gaps */}
              {activeTab === 'gaps' && (
                <div>
                  {result.skill_gaps?.map((g, i) => (
                    <Card key={i} style={{ marginBottom: '0.75rem' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 8, marginBottom: 8 }}>
                        <div style={{ fontSize: '0.9rem', fontWeight: 600, color: T.text }}>{g.skill_name}</div>
                        <Badge
                          color={g.importance === 'critical' ? T.red : T.gold}
                          bg={g.importance === 'critical' ? `${T.red}18` : `${T.gold}18`}
                        >
                          {g.importance}
                        </Badge>
                      </div>
                      <div style={{ fontSize: '0.78rem', color: T.teal, marginBottom: 8 }}>
                        📈 {g.expected_income_boost}
                      </div>
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                        <div style={{ background: T.s2, padding: '0.5rem', borderRadius: 7 }}>
                          <div style={{ fontSize: '0.6rem', color: T.orange, letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 3 }}>Free Resource</div>
                          <div style={{ fontSize: '0.72rem', color: T.muted }}>{g.free_resource}</div>
                        </div>
                        <div style={{ background: T.s2, padding: '0.5rem', borderRadius: 7 }}>
                          <div style={{ fontSize: '0.6rem', color: T.teal, letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 3 }}>Govt Course · {g.learning_time_days}d</div>
                          <div style={{ fontSize: '0.72rem', color: T.muted }}>{g.government_course}</div>
                        </div>
                      </div>
                    </Card>
                  ))}

                  {/* Strengths + Challenges */}
                  {(result.strengths?.length > 0 || result.challenges?.length > 0) && (
                    <Card>
                      {result.strengths?.length > 0 && (
                        <div style={{ marginBottom: '0.75rem' }}>
                          <div style={{ fontSize: '0.68rem', color: T.dim, letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 6 }}>Your Strengths</div>
                          {result.strengths.map((s, i) => (
                            <div key={i} style={{ fontSize: '0.78rem', color: T.teal, marginBottom: 4, display: 'flex', gap: 6 }}>
                              <span>✓</span>{s}
                            </div>
                          ))}
                        </div>
                      )}
                      {result.challenges?.length > 0 && (
                        <div>
                          <div style={{ fontSize: '0.68rem', color: T.dim, letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 6 }}>Challenges</div>
                          {result.challenges.map((c, i) => (
                            <div key={i} style={{ fontSize: '0.78rem', color: T.gold, marginBottom: 4, display: 'flex', gap: 6 }}>
                              <span>⚠</span>{c}
                            </div>
                          ))}
                        </div>
                      )}
                    </Card>
                  )}
                </div>
              )}

              {/* Actions */}
              {activeTab === 'actions' && (
                <div>
                  <Card>
                    <div style={{ fontSize: '0.88rem', fontWeight: 600, color: T.text, marginBottom: '1rem' }}>
                      Immediate Actions — Start Today
                    </div>
                    {result.immediate_actions?.map((action, i) => (
                      <div key={i} style={{
                        display: 'flex', gap: '0.75rem',
                        padding: '0.75rem',
                        background: T.s2,
                        borderRadius: 8,
                        marginBottom: '0.5rem',
                        alignItems: 'flex-start',
                      }}>
                        <div style={{
                          flexShrink: 0,
                          width: 24, height: 24,
                          borderRadius: '50%',
                          background: `${T.orange}20`,
                          border: `0.5px solid ${T.orange}60`,
                          display: 'flex', alignItems: 'center', justifyContent: 'center',
                          fontSize: '0.72rem', fontWeight: 700, color: T.orange,
                        }}>
                          {i + 1}
                        </div>
                        <div style={{ fontSize: '0.8rem', color: T.muted, lineHeight: 1.6 }}>
                          {typeof action === 'string' ? action.replace(/^\d+\.\s*/, '') : action}
                        </div>
                      </div>
                    ))}
                    {result.immediate_actions?.length === 0 && (
                      <Empty icon="⚡" title="No immediate actions" sub="Complete your profile for personalised steps" />
                    )}
                  </Card>

                  <div style={{
                    marginTop: '0.75rem',
                    padding: '0.75rem 1rem',
                    background: `${T.orange}0a`,
                    border: `0.5px solid ${T.orange}25`,
                    borderRadius: 9,
                    fontSize: '0.78rem',
                    color: T.orange,
                    lineHeight: 1.6,
                  }}>
                    💡 The fastest path to income is to start with one of these actions today. Every day of delay is a day of income missed.
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
