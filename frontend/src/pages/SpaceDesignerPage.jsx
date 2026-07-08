import { useState } from 'react'
import {
  T, Card, Stat, Tabs, Badge, Alert, Btn, Field,
  SkeletonCard, SectionTitle, Divider, PageHeader,
  Progress, fmt, Empty,
} from '../components/UI.jsx'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const BUSINESS_TYPES = [
  { type: 'tea_stall',       label: 'Tea Stall',        icon: '🫖', minArea: 40   },
  { type: 'vegetable_vendor',label: 'Vegetable Cart',   icon: '🥬', minArea: 20   },
  { type: 'mobile_repair',   label: 'Mobile Repair',    icon: '📱', minArea: 80   },
  { type: 'grocery',         label: 'Grocery / Kirana', icon: '🛒', minArea: 150  },
  { type: 'salon',           label: 'Salon / Parlour',  icon: '✂️', minArea: 200  },
  { type: 'pharmacy',        label: 'Medical Store',    icon: '💊', minArea: 200  },
  { type: 'coaching',        label: 'Coaching Centre',  icon: '📚', minArea: 200  },
  { type: 'bakery',          label: 'Bakery',           icon: '🍰', minArea: 200  },
  { type: 'cafe',            label: 'Cafe / Coffee',    icon: '☕', minArea: 250  },
  { type: 'hardware',        label: 'Hardware Store',   icon: '🔧', minArea: 300  },
  { type: 'clinic',          label: 'Medical Clinic',   icon: '🩺', minArea: 300  },
  { type: 'restaurant',      label: 'Restaurant / Dhaba',icon: '🍽️', minArea: 400 },
  { type: 'gym',             label: 'Gym / Fitness',    icon: '💪', minArea: 800  },
]

const ZONE_COLORS = {
  '#2d0a0a': 'rgba(180,50,50,0.32)',
  '#0d1a2d': 'rgba(30,80,180,0.32)',
  '#1a3d2e': 'rgba(50,150,80,0.32)',
  '#2d1a0a': 'rgba(160,100,30,0.32)',
  '#0a1a3d': 'rgba(20,60,180,0.36)',
  '#1a1a2d': 'rgba(60,60,150,0.32)',
  '#1a2a1a': 'rgba(40,120,40,0.32)',
  '#2d1a2d': 'rgba(150,50,150,0.32)',
  '#0a2040': 'rgba(10,60,130,0.36)',
  '#2d2d0a': 'rgba(150,150,20,0.32)',
  '#1a0d2d': 'rgba(100,40,180,0.36)',
  '#0d2d1a': 'rgba(20,140,60,0.36)',
  '#2d0a1a': 'rgba(180,20,80,0.36)',
  '#1a2d2d': 'rgba(20,140,140,0.36)',
  '#0a2d1a': 'rgba(10,150,80,0.36)',
}
const colorFor = hex => ZONE_COLORS[hex] || 'rgba(60,60,100,0.32)'

// ─── Floor Plan SVG ────────────────────────────────────────────────────────────
function FloorPlan({ result }) {
  if (!result) return null
  const W = 560, H = 420
  const sx = (W - 48) / result.width_ft
  const sy = (H - 68) / result.depth_ft
  const ox = 24, oy = 34

  return (
    <Card style={{ marginBottom: '1.25rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 8, marginBottom: '1rem' }}>
        <div>
          <div style={{ fontSize: '0.92rem', fontWeight: 600, color: T.orange }}>{result.display_name} — Floor Plan</div>
          <div style={{ fontSize: '0.72rem', color: T.muted, marginTop: 2 }}>
            {result.width_ft}ft × {result.depth_ft}ft = {result.total_area} sqft · {result.layout_style}
          </div>
        </div>
        <div style={{ textAlign: 'center', background: T.s2, padding: '0.5rem 0.85rem', borderRadius: 8, border: `0.5px solid ${T.border}` }}>
          <div style={{ fontSize: '1.3rem', fontWeight: 700, color: T.gold, fontFamily: T.serif }}>
            {result.efficiency_score}
          </div>
          <div style={{ fontSize: '0.58rem', color: T.dim, textTransform: 'uppercase', letterSpacing: '0.1em' }}>Efficiency</div>
        </div>
      </div>

      {/* SVG */}
      <div className="floor-plan-wrap">
        <svg width={W} height={H} style={{ display: 'block', background: '#04040c', borderRadius: 8 }}>
          {/* Grid */}
          {Array.from({ length: Math.ceil(result.width_ft / 5) + 1 }, (_, i) => (
            <line key={`gx${i}`} x1={ox + i*5*sx} y1={oy} x2={ox + i*5*sx} y2={oy + result.depth_ft*sy}
              stroke="#121224" strokeWidth="0.5"/>
          ))}
          {Array.from({ length: Math.ceil(result.depth_ft / 5) + 1 }, (_, i) => (
            <line key={`gy${i}`} x1={ox} y1={oy + i*5*sy} x2={ox + result.width_ft*sx} y2={oy + i*5*sy}
              stroke="#121224" strokeWidth="0.5"/>
          ))}

          {/* Boundary */}
          <rect x={ox} y={oy} width={result.width_ft*sx} height={result.depth_ft*sy}
            fill="none" stroke={T.orange} strokeWidth="1.5" rx="2"/>

          {/* Entry arrow */}
          <polygon points={`${ox + result.width_ft*sx/2 - 6},${oy + result.depth_ft*sy} ${ox + result.width_ft*sx/2 + 6},${oy + result.depth_ft*sy} ${ox + result.width_ft*sx/2},${oy + result.depth_ft*sy - 10}`}
            fill={T.teal} opacity="0.7"/>
          <text x={ox + result.width_ft*sx/2} y={H - 8} textAnchor="middle" fontSize="8" fill={T.teal}>Entry</text>

          {/* Zones */}
          {result.zones?.map(z => (
            <g key={z.id}>
              <rect x={ox + z.x*sx} y={oy + z.y*sy} width={z.w*sx} height={z.h*sy}
                fill={colorFor(z.color)} stroke={T.border} strokeWidth="0.5" rx="2"/>
              {z.h*sy > 22 && (
                <text x={ox + (z.x + z.w/2)*sx} y={oy + (z.y + z.h/2)*sy - 4}
                  textAnchor="middle" fontSize="10" fill={T.text} opacity="0.8">{z.icon}</text>
              )}
              {z.h*sy > 34 && (
                <text x={ox + (z.x + z.w/2)*sx} y={oy + (z.y + z.h/2)*sy + 9}
                  textAnchor="middle" fontSize="7" fill={T.muted} opacity="0.85">
                  {z.name.length > 14 ? z.name.slice(0,14) + '…' : z.name}
                </text>
              )}
            </g>
          ))}

          {/* Essential equipment */}
          {result.equipment?.filter(e => e.priority === 'essential').map(e => (
            <g key={e.id}>
              <rect x={ox + e.x*sx} y={oy + e.y*sy}
                width={Math.max(e.w*sx, 12)} height={Math.max(e.h*sy, 10)}
                fill={`${T.orange}22`} stroke={T.orange} strokeWidth="0.8" rx="2"/>
              <text x={ox + (e.x + e.w/2)*sx} y={oy + (e.y + e.h/2)*sy + 3}
                textAnchor="middle" fontSize="7" fill={T.orange}>{e.icon}</text>
            </g>
          ))}

          {/* Dimension labels */}
          <text x={ox + result.width_ft*sx/2} y={oy - 14} textAnchor="middle" fontSize="9" fill={T.gold}>
            {result.width_ft} ft
          </text>
          <text x={ox - 12} y={oy + result.depth_ft*sy/2} textAnchor="middle" fontSize="9" fill={T.gold}
            transform={`rotate(-90, ${ox - 12}, ${oy + result.depth_ft*sy/2})`}>
            {result.depth_ft} ft
          </text>

          {/* Compass */}
          <g transform={`translate(${W - 26}, 18)`}>
            <polygon points="0,-8 -4,2 0,-1 4,2" fill={T.teal} opacity="0.8"/>
            <text x="0" y="13" textAnchor="middle" fontSize="7" fill={T.teal}>N</text>
          </g>
        </svg>
      </div>

      {/* Flow note */}
      {result.customer_flow && (
        <div style={{
          marginTop: '0.75rem',
          padding: '0.55rem 0.8rem',
          background: `${T.teal}0a`,
          border: `0.5px solid ${T.teal}30`,
          borderRadius: 7,
          fontSize: '0.75rem',
          color: T.teal,
        }}>
          🚶 {result.customer_flow}
        </div>
      )}

      {/* Zone legend */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.75rem' }}>
        {result.zones?.map(z => (
          <div key={z.id} style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: '0.68rem', color: T.muted }}>
            <div style={{ width: 9, height: 9, background: colorFor(z.color), borderRadius: 2, border: `0.5px solid ${T.border}`, flexShrink: 0 }} />
            {z.icon} {z.name} ({z.pct}%)
          </div>
        ))}
      </div>
    </Card>
  )
}

// ─── Equipment List ─────────────────────────────────────────────────────────
function EquipmentList({ equipment }) {
  const [tab, setTab] = useState('essential')
  const filtered = equipment?.filter(e => tab === 'all' || e.priority === tab) || []
  const total = filtered.reduce((s, e) => s + (e.total_cost || 0), 0)

  return (
    <Card style={{ marginBottom: '1.25rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 8, marginBottom: '0.75rem' }}>
        <div style={{ fontSize: '0.85rem', fontWeight: 600, color: T.text }}>Equipment List</div>
        <Tabs
          size="sm"
          tabs={[['essential','Essential'],['recommended','Recommended'],['optional','Optional'],['all','All']]}
          active={tab}
          onChange={setTab}
        />
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
        {filtered.length === 0 && <Empty icon="⚙️" title="No items" sub="Switch to a different filter" />}
        {filtered.map(e => (
          <div key={e.id} style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            padding: '0.55rem 0.75rem',
            background: T.s2,
            borderRadius: 8,
            flexWrap: 'wrap', gap: 6,
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flex: 1 }}>
              <span style={{ fontSize: '1.1rem', flexShrink: 0 }}>{e.icon}</span>
              <div>
                <div style={{ fontSize: '0.82rem', color: T.text }}>
                  {e.name}
                  <span style={{ color: T.dim, fontSize: '0.7rem', marginLeft: 4 }}>×{e.quantity}</span>
                </div>
                {e.notes && <div style={{ fontSize: '0.67rem', color: T.dim }}>{e.notes}</div>}
              </div>
            </div>
            <div style={{ textAlign: 'right', flexShrink: 0 }}>
              <div style={{ fontSize: '0.82rem', fontWeight: 600, color: T.gold, fontVariantNumeric: 'tabular-nums' }}>
                {fmt(e.total_cost)}
              </div>
              <div style={{ fontSize: '0.6rem', color: T.dim }}>{fmt(e.unit_cost)} each</div>
            </div>
          </div>
        ))}
      </div>

      {filtered.length > 0 && (
        <div style={{
          marginTop: '0.75rem',
          padding: '0.6rem 0.75rem',
          background: `${T.gold}12`,
          border: `0.5px solid ${T.gold}30`,
          borderRadius: 7,
          display: 'flex', justifyContent: 'space-between',
        }}>
          <span style={{ fontSize: '0.8rem', color: T.muted }}>
            {tab === 'all' ? 'All Equipment' : `${tab.charAt(0).toUpperCase() + tab.slice(1)} Equipment`} Total
          </span>
          <span style={{ fontSize: '0.88rem', fontWeight: 700, color: T.gold, fontVariantNumeric: 'tabular-nums' }}>
            {fmt(total)}
          </span>
        </div>
      )}
    </Card>
  )
}

// ─── Cost Breakdown ─────────────────────────────────────────────────────────
function CostBreakdown({ costs, budget }) {
  if (!costs) return null
  const items = [
    { label: 'Essential Equipment', value: costs.equipment_essential, color: T.orange },
    { label: 'Interior Work',       value: costs.interior_work,       color: T.gold   },
    { label: 'Electrical Wiring',   value: costs.electrical_wiring,   color: T.teal   },
    { label: 'Plumbing',            value: costs.plumbing,            color: T.blue   },
    { label: 'Signage & Branding',  value: costs.signage_branding,    color: T.purple },
    { label: 'Security Deposit',    value: costs.security_deposit,    color: '#F472B6' },
  ]
  const total = costs.total_estimated
  const hasGap = costs.budget_gap > 0

  return (
    <Card style={{ marginBottom: '1.25rem' }}>
      <div style={{ fontSize: '0.85rem', fontWeight: 600, color: T.text, marginBottom: '1rem' }}>Cost Breakdown</div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.55rem', marginBottom: '1rem' }}>
        {items.map(item => (
          <div key={item.label}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3 }}>
              <span style={{ fontSize: '0.75rem', color: T.muted }}>{item.label}</span>
              <span style={{ fontSize: '0.75rem', color: item.color, fontVariantNumeric: 'tabular-nums' }}>
                {fmt(item.value)}
              </span>
            </div>
            <Progress
              value={item.value}
              max={total}
              color={item.color}
              thin
            />
          </div>
        ))}
      </div>

      {/* Summary box */}
      <div style={{ padding: '0.85rem', background: T.s2, borderRadius: 9, border: `0.5px solid ${T.border}` }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 5 }}>
          <span style={{ fontSize: '0.8rem', color: T.muted }}>Total Estimated Cost</span>
          <span style={{ fontSize: '1rem', fontWeight: 700, color: hasGap ? T.red : T.teal, fontVariantNumeric: 'tabular-nums' }}>
            {fmt(total)}
          </span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
          <span style={{ fontSize: '0.75rem', color: T.muted }}>Your Budget</span>
          <span style={{ fontSize: '0.88rem', color: T.gold, fontVariantNumeric: 'tabular-nums' }}>
            {fmt(budget)}
          </span>
        </div>
        <Progress
          value={budget}
          max={total || budget}
          color={hasGap ? T.red : T.teal}
          label="Budget Coverage"
        />
        <div style={{ marginTop: '0.6rem' }}>
          {hasGap ? (
            <Alert type="warning">
              ⚠ Funding gap: {fmt(costs.budget_gap)} — Consider MUDRA loan to bridge
            </Alert>
          ) : (
            <Alert type="success">
              ✓ Within budget — Reserve {fmt(budget - total)} for first month working capital
            </Alert>
          )}
        </div>
        {costs.monthly_rent_estimate > 0 && (
          <div style={{ marginTop: 6, fontSize: '0.68rem', color: T.dim }}>
            Monthly rent estimate: {fmt(costs.monthly_rent_estimate)} · Budget utilization: {costs.budget_utilization_pct}%
          </div>
        )}
      </div>
    </Card>
  )
}

// ─── Main Component ─────────────────────────────────────────────────────────
export default function SpaceDesignerPage({ onBack }) {
  const [form, setForm] = useState({ business_type: '', area_sqft: '', width_ft: '', depth_ft: '', budget: '' })
  const [result,    setResult]    = useState(null)
  const [loading,   setLoading]   = useState(false)
  const [error,     setError]     = useState('')
  const [activeTab, setActiveTab] = useState('plan')

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const design = async () => {
    if (!form.business_type) { setError('Select a business type'); return }
    if (!form.area_sqft)     { setError('Enter the area in sqft'); return }
    if (!form.budget)        { setError('Enter your budget'); return }
    setLoading(true); setError(''); setResult(null)
    try {
      const res = await fetch(`${API}/api/space/design`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          business_type: form.business_type,
          area_sqft: parseFloat(form.area_sqft),
          width_ft:  parseFloat(form.width_ft)  || null,
          depth_ft:  parseFloat(form.depth_ft)  || null,
          budget:    parseFloat(form.budget),
        }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Design failed')
      setResult(data)
      setActiveTab('plan')
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <div className="fade-in">
      <PageHeader
        icon="📐"
        title="Space Designer"
        sub="Autonomous floor plan · Equipment layout · Cost estimate"
        color={T.gold}
        onBack={onBack}
      />

      <div className="page-wrap">
        {/* Form card */}
        <Card style={{ marginBottom: '1.25rem' }}>
          <div style={{ fontSize: '0.88rem', fontWeight: 600, color: T.text, marginBottom: '1rem' }}>
            Design Your Business Space
          </div>

          {/* Business type selector */}
          <div style={{ fontSize: '0.65rem', color: T.muted, letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
            Business Type
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(118px,1fr))', gap: '0.4rem', marginBottom: '1.1rem' }}>
            {BUSINESS_TYPES.map(b => {
              const active = form.business_type === b.type
              return (
                <button
                  key={b.type}
                  onClick={() => set('business_type', b.type)}
                  style={{
                    padding: '0.6rem 0.4rem',
                    borderRadius: 8, border: `0.5px solid ${active ? T.gold : T.border}`,
                    cursor: 'pointer', textAlign: 'center', fontSize: '0.7rem',
                    background: active ? `${T.gold}14` : T.s2,
                    color: active ? T.gold : T.muted,
                    fontFamily: T.ff,
                    transition: 'all 0.15s',
                  }}
                  onMouseEnter={e => { if (!active) e.currentTarget.style.borderColor = `${T.gold}60` }}
                  onMouseLeave={e => { if (!active) e.currentTarget.style.borderColor = T.border }}
                >
                  <div style={{ fontSize: '1.2rem', marginBottom: 3 }}>{b.icon}</div>
                  <div style={{ lineHeight: 1.3 }}>{b.label}</div>
                  <div style={{ fontSize: '0.58rem', color: T.dim, marginTop: 2 }}>Min {b.minArea} sqft</div>
                </button>
              )
            })}
          </div>

          {/* Dimensions */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(175px,1fr))', gap: '0.9rem', marginBottom: '1rem' }}>
            <Field
              label="Total Area (sqft)"
              value={form.area_sqft}
              onChange={e => set('area_sqft', e.target.value)}
              type="number"
              placeholder="e.g. 400"
              required
            />
            <Field
              label="Width (feet) — optional"
              value={form.width_ft}
              onChange={e => set('width_ft', e.target.value)}
              type="number"
              placeholder="e.g. 20"
            />
            <Field
              label="Depth (feet) — optional"
              value={form.depth_ft}
              onChange={e => set('depth_ft', e.target.value)}
              type="number"
              placeholder="e.g. 20"
            />
            <Field
              label="Budget (₹)"
              value={form.budget}
              onChange={e => set('budget', e.target.value)}
              type="number"
              placeholder="e.g. 200000"
              required
            />
          </div>

          {error && <Alert type="error" style={{ marginBottom: '0.75rem' }}>{error}</Alert>}

          <Btn variant="primary" size="lg" full disabled={loading} onClick={design} icon="📐">
            {loading ? 'Designing space…' : 'Generate Floor Plan'}
          </Btn>
        </Card>

        {/* Loading */}
        {loading && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            <SkeletonCard />
            <SkeletonCard />
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div className="fade-in">
            {/* Summary stats */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(120px,1fr))', gap: '0.5rem', marginBottom: '1.25rem' }}>
              <Stat label="Monthly Revenue" value={fmt(result.estimated_monthly_revenue)} color={T.teal} />
              <Stat label="Setup Cost"      value={fmt(result.estimated_setup_cost)}      color={T.gold} />
              <Stat label="Budget Gap"
                value={result.cost_breakdown?.budget_gap > 0 ? fmt(result.cost_breakdown.budget_gap) : 'None'}
                color={result.cost_breakdown?.budget_gap > 0 ? T.red : T.teal}
              />
              <Stat label="Efficiency" value={`${result.efficiency_score}/100`} color={T.orange} />
            </div>

            {/* Tabs */}
            <Tabs
              tabs={[
                ['plan',       '🗺️ Floor Plan'],
                ['equipment',  '⚙️ Equipment'],
                ['costs',      '💰 Costs'],
                ['compliance', '📋 Compliance'],
              ]}
              active={activeTab}
              onChange={setActiveTab}
            />
            <div style={{ marginTop: '1.25rem' }}>
              {activeTab === 'plan'       && <FloorPlan result={result} />}
              {activeTab === 'equipment'  && <EquipmentList equipment={result.equipment} />}
              {activeTab === 'costs'      && <CostBreakdown costs={result.cost_breakdown} budget={result.budget} />}
              {activeTab === 'compliance' && (
                <Card>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600, color: T.text, marginBottom: '1rem' }}>
                    Compliance &amp; Licensing
                  </div>
                  {result.compliance_notes?.map((note, i) => (
                    <div key={i} style={{ display: 'flex', gap: 8, marginBottom: '0.5rem', padding: '0.55rem 0.75rem', background: T.s2, borderRadius: 7, fontSize: '0.78rem', color: T.muted }}>
                      <span style={{ color: T.teal, flexShrink: 0 }}>✓</span>{note}
                    </div>
                  ))}
                  {result.optimization_tips?.length > 0 && (
                    <>
                      <Divider label="Optimization Tips" />
                      {result.optimization_tips.map((tip, i) => (
                        <div key={i} style={{ display: 'flex', gap: 8, marginBottom: '0.4rem', fontSize: '0.75rem', color: T.muted }}>
                          <span style={{ color: T.gold, flexShrink: 0 }}>💡</span>{tip}
                        </div>
                      ))}
                    </>
                  )}
                </Card>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
