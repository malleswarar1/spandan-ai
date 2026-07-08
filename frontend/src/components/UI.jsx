/**
 * SPANDAN AI — Design System v3
 * Shared tokens, primitives and compound components.
 * All styles are inline (no external deps) so this works everywhere.
 */

// ─── Design Tokens ────────────────────────────────────────────────────────────
export const T = {
  bg:      '#07060e',
  s1:      '#0d0c1a',   // surface 1 (cards)
  s2:      '#111022',   // surface 2 (inputs, elevated)
  s3:      '#161430',   // surface 3 (active/selected)
  border:  '#1e1b30',
  borderL: '#131124',   // lighter border
  text:    '#F0EDD6',   // warm off-white
  muted:   '#9A9280',
  dim:     '#5A5468',
  orange:  '#FF6B00',
  gold:    '#E8A020',
  teal:    '#00C9A7',
  red:     '#F04444',
  purple:  '#9333EA',
  blue:    '#3B82F6',
  green:   '#22C55E',
  grad:    'linear-gradient(135deg,#FF6B00,#E8A020)',
  ff:      "'Inter',system-ui,sans-serif",
  serif:   "'Cinzel',Georgia,serif",
}

// ─── Button ──────────────────────────────────────────────────────────────────
export function Btn({
  children, onClick, variant = 'primary', size = 'md',
  disabled, full, icon, type = 'button', style: extra
}) {
  const sizes = {
    sm: { padding: '0.35rem 0.85rem', fontSize: '0.75rem' },
    md: { padding: '0.6rem 1.4rem',   fontSize: '0.85rem' },
    lg: { padding: '0.8rem 2rem',     fontSize: '0.92rem' },
  }
  const variants = {
    primary: {
      background: disabled ? '#2a2038' : T.grad,
      color: 'white',
      border: 'none',
    },
    secondary: {
      background: 'transparent',
      color: T.text,
      border: `0.5px solid ${T.border}`,
    },
    ghost: {
      background: 'transparent',
      color: T.muted,
      border: `0.5px solid ${T.borderL}`,
    },
    danger: {
      background: disabled ? '#2a1818' : '#3a1010',
      color: T.red,
      border: `0.5px solid ${T.red}40`,
    },
    teal: {
      background: disabled ? '#0d1e1a' : '#0a2420',
      color: T.teal,
      border: `0.5px solid ${T.teal}40`,
    },
  }
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      style={{
        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
        gap: '0.4rem',
        fontFamily: T.ff,
        fontWeight: 500,
        letterSpacing: '0.04em',
        borderRadius: 7,
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.55 : 1,
        transition: 'opacity 0.15s, filter 0.15s',
        width: full ? '100%' : undefined,
        whiteSpace: 'nowrap',
        ...sizes[size],
        ...variants[variant],
        ...extra,
      }}
      onMouseEnter={e => { if (!disabled) e.currentTarget.style.filter = 'brightness(1.12)' }}
      onMouseLeave={e => { e.currentTarget.style.filter = 'none' }}
    >
      {icon && <span style={{ fontSize: '0.95em', lineHeight: 1 }}>{icon}</span>}
      {children}
    </button>
  )
}

// ─── Field ───────────────────────────────────────────────────────────────────
export function Field({
  label, value, onChange, type = 'text', placeholder,
  hint, error, required, name, min, max, step, disabled, onKeyDown
}) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
      {label && (
        <label style={{
          fontSize: '0.68rem', color: T.muted,
          letterSpacing: '0.12em', textTransform: 'uppercase',
          fontFamily: T.ff,
        }}>
          {label}{required && <span style={{ color: T.orange, marginLeft: 3 }}>*</span>}
        </label>
      )}
      <input
        type={type} value={value} onChange={onChange}
        placeholder={placeholder} name={name}
        min={min} max={max} step={step} disabled={disabled} onKeyDown={onKeyDown}
        style={{
          width: '100%',
          padding: '0.6rem 0.75rem',
          background: T.s2,
          border: `0.5px solid ${error ? T.red : T.border}`,
          borderRadius: 7,
          color: T.text,
          fontSize: '0.88rem',
          fontFamily: T.ff,
          outline: 'none',
          transition: 'border-color 0.15s',
          opacity: disabled ? 0.55 : 1,
          boxSizing: 'border-box',
        }}
        onFocus={e => { if (!error) e.target.style.borderColor = T.orange }}
        onBlur={e => { e.target.style.borderColor = error ? T.red : T.border }}
      />
      {(hint || error) && (
        <span style={{ fontSize: '0.7rem', color: error ? T.red : T.dim, marginTop: 2 }}>
          {error || hint}
        </span>
      )}
    </div>
  )
}

// ─── SelectField ─────────────────────────────────────────────────────────────
export function SelectField({ label, value, onChange, children, hint, required }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
      {label && (
        <label style={{
          fontSize: '0.68rem', color: T.muted,
          letterSpacing: '0.12em', textTransform: 'uppercase',
          fontFamily: T.ff,
        }}>
          {label}{required && <span style={{ color: T.orange, marginLeft: 3 }}>*</span>}
        </label>
      )}
      <select
        value={value} onChange={onChange}
        style={{
          width: '100%',
          padding: '0.6rem 0.75rem',
          background: T.s2,
          border: `0.5px solid ${T.border}`,
          borderRadius: 7,
          color: T.text,
          fontSize: '0.88rem',
          fontFamily: T.ff,
          outline: 'none',
          cursor: 'pointer',
          boxSizing: 'border-box',
        }}
        onFocus={e => { e.target.style.borderColor = T.orange }}
        onBlur={e => { e.target.style.borderColor = T.border }}
      >
        {children}
      </select>
      {hint && <span style={{ fontSize: '0.7rem', color: T.dim, marginTop: 2 }}>{hint}</span>}
    </div>
  )
}

// ─── Card ────────────────────────────────────────────────────────────────────
export function Card({ children, highlight, onClick, pad = '1.25rem', style: extra }) {
  return (
    <div
      onClick={onClick}
      style={{
        background: T.s1,
        border: `0.5px solid ${highlight || T.border}`,
        borderRadius: 12,
        padding: pad,
        cursor: onClick ? 'pointer' : undefined,
        transition: onClick ? 'border-color 0.15s, background 0.15s' : undefined,
        ...extra,
      }}
      onMouseEnter={onClick ? e => { e.currentTarget.style.background = T.s2 } : undefined}
      onMouseLeave={onClick ? e => { e.currentTarget.style.background = T.s1 } : undefined}
    >
      {children}
    </div>
  )
}

// ─── Badge ───────────────────────────────────────────────────────────────────
export function Badge({ children, color = T.teal, bg }) {
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center',
      fontSize: '0.62rem',
      fontFamily: T.ff,
      letterSpacing: '0.08em',
      color,
      background: bg || `${color}12`,
      border: `0.5px solid ${color}40`,
      padding: '2px 8px',
      borderRadius: 4,
    }}>
      {children}
    </span>
  )
}

// ─── Stat tile ───────────────────────────────────────────────────────────────
export function Stat({ label, value, color, icon, sub }) {
  return (
    <div style={{
      background: T.s2,
      borderRadius: 8,
      padding: '0.75rem',
      textAlign: 'center',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: 3,
    }}>
      {icon && <span style={{ fontSize: '1.1rem', marginBottom: 2 }}>{icon}</span>}
      <div style={{
        fontSize: value && value.toString().length > 6 ? '0.88rem' : '1.05rem',
        fontWeight: 600,
        color: color || T.gold,
        fontFamily: T.ff,
        fontVariantNumeric: 'tabular-nums',
        lineHeight: 1.2,
      }}>
        {value ?? '—'}
      </div>
      <div style={{
        fontSize: '0.6rem', color: T.muted,
        textTransform: 'uppercase', letterSpacing: '0.1em', lineHeight: 1.3,
      }}>
        {label}
      </div>
      {sub && <div style={{ fontSize: '0.6rem', color: T.dim }}>{sub}</div>}
    </div>
  )
}

// ─── Spinner ─────────────────────────────────────────────────────────────────
export function Spinner({ size = 20, color = T.orange }) {
  return (
    <svg width={size} height={size} viewBox="0 0 20 20" style={{ animation: 'spin 0.8s linear infinite' }}>
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
      <circle cx="10" cy="10" r="8" fill="none" stroke={`${color}30`} strokeWidth="2.5"/>
      <path d="M10 2 A8 8 0 0 1 18 10" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round"/>
    </svg>
  )
}

// ─── Skeleton ────────────────────────────────────────────────────────────────
export function Skeleton({ w = '100%', h = 16, r = 6 }) {
  return (
    <div style={{
      width: w, height: h, borderRadius: r,
      background: `linear-gradient(90deg,${T.s2} 25%,${T.s3} 50%,${T.s2} 75%)`,
      backgroundSize: '200% 100%',
      animation: 'shimmer 1.4s infinite',
    }}>
      <style>{`@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}`}</style>
    </div>
  )
}

// ─── SkeletonCard ─────────────────────────────────────────────────────────────
export function SkeletonCard() {
  return (
    <Card>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <Skeleton h={18} w="60%" />
        <Skeleton h={12} w="80%" />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 8 }}>
          {[0,1,2,3].map(i => <Skeleton key={i} h={52} />)}
        </div>
        <Skeleton h={12} w="90%" />
        <Skeleton h={12} w="70%" />
      </div>
    </Card>
  )
}

// ─── Alert ───────────────────────────────────────────────────────────────────
export function Alert({ type = 'error', children, style: extra }) {
  const cfg = {
    error:   { bg: '#1a0808', border: T.red,    text: '#ff8080', icon: '✕' },
    success: { bg: '#081a10', border: T.green,   text: '#80ffb0', icon: '✓' },
    info:    { bg: '#08101a', border: T.blue,    text: '#80c0ff', icon: 'ℹ' },
    warning: { bg: '#1a1208', border: T.gold,    text: '#ffd080', icon: '⚠' },
  }[type] || {}
  return (
    <div style={{
      padding: '0.7rem 1rem',
      background: cfg.bg,
      border: `0.5px solid ${cfg.border}`,
      borderRadius: 8,
      color: cfg.text,
      fontSize: '0.82rem',
      fontFamily: T.ff,
      display: 'flex',
      alignItems: 'flex-start',
      gap: '0.5rem',
      ...extra,
    }}>
      <span style={{ marginTop: 1, flexShrink: 0 }}>{cfg.icon}</span>
      <span>{children}</span>
    </div>
  )
}

// ─── Progress bar ────────────────────────────────────────────────────────────
export function Progress({ value = 0, max = 100, color = T.orange, label, thin }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100))
  return (
    <div>
      {label && (
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
          <span style={{ fontSize: '0.72rem', color: T.muted }}>{label}</span>
          <span style={{ fontSize: '0.72rem', color, fontVariantNumeric: 'tabular-nums' }}>
            {Math.round(pct)}%
          </span>
        </div>
      )}
      <div style={{
        height: thin ? 3 : 6, background: T.s2, borderRadius: 3, overflow: 'hidden',
      }}>
        <div style={{
          height: '100%', width: `${pct}%`,
          background: color,
          borderRadius: 3,
          transition: 'width 0.6s ease',
        }} />
      </div>
    </div>
  )
}

// ─── Tabs ────────────────────────────────────────────────────────────────────
export function Tabs({ tabs, active, onChange, size = 'md' }) {
  const sizes = {
    sm: { padding: '0.3rem 0.8rem', fontSize: '0.72rem' },
    md: { padding: '0.45rem 1.1rem', fontSize: '0.8rem' },
  }
  return (
    <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
      {tabs.map(([key, label]) => (
        <button
          key={key} onClick={() => onChange(key)}
          style={{
            fontFamily: T.ff, fontWeight: 500,
            borderRadius: 6,
            border: `0.5px solid ${active === key ? T.orange : T.border}`,
            background: active === key ? `${T.orange}15` : 'transparent',
            color: active === key ? T.orange : T.muted,
            cursor: 'pointer',
            transition: 'all 0.15s',
            letterSpacing: '0.04em',
            ...sizes[size],
          }}
        >
          {label}
        </button>
      ))}
    </div>
  )
}

// ─── SectionTitle ─────────────────────────────────────────────────────────────
export function SectionTitle({ title, sub, action, right }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1rem', flexWrap: 'wrap', gap: 8 }}>
      <div>
        <div style={{
          fontSize: '0.75rem', color: T.muted,
          letterSpacing: '0.2em', textTransform: 'uppercase',
          fontFamily: T.ff, marginBottom: 3,
        }}>
          {title}
        </div>
        {sub && <div style={{ fontSize: '0.72rem', color: T.dim }}>{sub}</div>}
      </div>
      {(action || right) && <div>{action || right}</div>}
    </div>
  )
}

// ─── Divider ─────────────────────────────────────────────────────────────────
export function Divider({ label }) {
  if (!label) return (
    <div style={{ height: '0.5px', background: T.border, margin: '1.25rem 0' }} />
  )
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12, margin: '1.25rem 0' }}>
      <div style={{ flex: 1, height: '0.5px', background: T.border }} />
      <span style={{ fontSize: '0.65rem', color: T.dim, letterSpacing: '0.15em', textTransform: 'uppercase' }}>{label}</span>
      <div style={{ flex: 1, height: '0.5px', background: T.border }} />
    </div>
  )
}

// ─── PageHeader ──────────────────────────────────────────────────────────────
export function PageHeader({ title, sub, icon, color = T.orange, onBack, action }) {
  return (
    <div style={{
      padding: '1.25rem 1.5rem',
      borderBottom: `0.5px solid ${T.border}`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: 12,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        {onBack && (
          <button onClick={onBack} style={{
            background: 'transparent', border: `0.5px solid ${T.border}`,
            color: T.muted, padding: '0.3rem 0.6rem', borderRadius: 6,
            fontSize: '0.75rem', cursor: 'pointer', fontFamily: T.ff,
          }}>
            ← Back
          </button>
        )}
        {icon && <span style={{ fontSize: '1.5rem' }}>{icon}</span>}
        <div>
          <div style={{
            fontFamily: T.ff, fontSize: '0.95rem', fontWeight: 600,
            color, letterSpacing: '0.04em',
          }}>
            {title}
          </div>
          {sub && <div style={{ fontSize: '0.72rem', color: T.muted, marginTop: 2 }}>{sub}</div>}
        </div>
      </div>
      {action && <div>{action}</div>}
    </div>
  )
}

// ─── CheckCard ───────────────────────────────────────────────────────────────
export function CheckCard({ checked, onChange, label, sub, icon }) {
  return (
    <div
      onClick={() => onChange(!checked)}
      style={{
        background: checked ? `${T.orange}10` : T.s1,
        border: `0.5px solid ${checked ? T.orange : T.border}`,
        borderRadius: 9,
        padding: '0.65rem 0.8rem',
        cursor: 'pointer',
        transition: 'all 0.15s',
        display: 'flex',
        alignItems: 'center',
        gap: '0.6rem',
        userSelect: 'none',
      }}
    >
      <div style={{
        width: 16, height: 16,
        borderRadius: 4,
        border: `1.5px solid ${checked ? T.orange : T.border}`,
        background: checked ? T.orange : 'transparent',
        flexShrink: 0,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        transition: 'all 0.15s',
      }}>
        {checked && <span style={{ fontSize: 10, color: 'white', lineHeight: 1 }}>✓</span>}
      </div>
      {icon && <span style={{ fontSize: '1.1rem' }}>{icon}</span>}
      <div>
        <div style={{ fontSize: '0.82rem', color: T.text, fontFamily: T.ff }}>{label}</div>
        {sub && <div style={{ fontSize: '0.68rem', color: T.muted, marginTop: 1 }}>{sub}</div>}
      </div>
    </div>
  )
}

// ─── ScoreRing ───────────────────────────────────────────────────────────────
export function ScoreRing({ score = 0, label, color = T.orange, size = 80 }) {
  const r = size * 0.34
  const circ = 2 * Math.PI * r
  const pct = Math.min(1, score / 100)
  return (
    <div style={{ textAlign: 'center', display: 'inline-flex', flexDirection: 'column', alignItems: 'center' }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ transform: 'rotate(-90deg)' }}>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={T.s2} strokeWidth="3.5"/>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth="3.5"
          strokeDasharray={circ}
          strokeDashoffset={circ * (1 - pct)}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 0.8s ease' }}
        />
        <text x={size/2} y={size/2} textAnchor="middle" dominantBaseline="middle"
          fill={color} fontSize={size * 0.22} fontWeight="700" fontFamily={T.ff}
          style={{ transform: `rotate(90deg) translate(0, -${size}px)`, transformOrigin: `${size/2}px ${size/2}px` }}>
          {score}
        </text>
      </svg>
      {label && <div style={{ fontSize: '0.62rem', color: T.muted, marginTop: 4, letterSpacing: '0.1em', textTransform: 'uppercase' }}>{label}</div>}
    </div>
  )
}

// ─── UrgencyBadge ─────────────────────────────────────────────────────────────
export function UrgencyBadge({ urgency }) {
  const cfg = {
    critical: { color: T.red,    label: '🔴 Critical' },
    high:     { color: T.orange, label: '🟠 High' },
    medium:   { color: T.gold,   label: '🟡 Medium' },
    low:      { color: T.teal,   label: '🟢 Low' },
  }[urgency] || { color: T.muted, label: urgency }
  return <Badge color={cfg.color}>{cfg.label}</Badge>
}

// ─── PriorityBadge ────────────────────────────────────────────────────────────
export function PriorityBadge({ priority }) {
  const cfg = {
    immediate: T.orange,
    medium:    T.gold,
    low:       T.teal,
  }[priority] || T.muted
  return <Badge color={cfg}>{priority}</Badge>
}

// ─── MoneyFmt ─────────────────────────────────────────────────────────────────
export function fmt(amount) {
  if (!amount && amount !== 0) return '—'
  if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(1)} Cr`
  if (amount >= 100000)   return `₹${(amount / 100000).toFixed(0)} L`
  if (amount >= 1000)     return `₹${(amount / 1000).toFixed(0)}K`
  return `₹${amount}`
}

// ─── Empty state ─────────────────────────────────────────────────────────────
export function Empty({ icon = '📭', title, sub }) {
  return (
    <div style={{ textAlign: 'center', padding: '3rem 1rem', color: T.muted }}>
      <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>{icon}</div>
      {title && <div style={{ fontSize: '0.9rem', fontWeight: 500, color: T.text, marginBottom: '0.4rem' }}>{title}</div>}
      {sub && <div style={{ fontSize: '0.78rem', color: T.dim }}>{sub}</div>}
    </div>
  )
}
