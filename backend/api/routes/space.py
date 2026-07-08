"""SPANDAN AI — Autonomous Space Designer Routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
router = APIRouter()

class SpaceDesignRequest(BaseModel):
    business_type: str
    area_sqft: float
    width_ft: Optional[float] = None
    depth_ft: Optional[float] = None
    budget: float
    name: Optional[str] = ""
    include_3d: bool = False

class SpaceCompareRequest(BaseModel):
    business_type: str
    area_sqft: float
    budget: float
    layouts: List[str] = ["linear", "open_plan", "workstation"]

@router.post("/design")
async def design_space(req: SpaceDesignRequest):
    try:
        from ai_engine.space.designer import SpaceDesigner
        designer = SpaceDesigner()
        result = designer.design(
            business_type=req.business_type,
            area_sqft=req.area_sqft,
            width_ft=req.width_ft or 0,
            depth_ft=req.depth_ft or 0,
            budget=req.budget,
        )
        return {
            "business_type": result.business_type,
            "display_name": result.display_name,
            "total_area": result.total_area,
            "width_ft": result.width_ft,
            "depth_ft": result.depth_ft,
            "budget": result.budget,
            "layout_style": result.layout_style,
            "customer_flow": result.customer_flow,
            "efficiency_score": result.efficiency_score,
            "estimated_setup_cost": result.estimated_setup_cost,
            "estimated_monthly_revenue": result.estimated_monthly_revenue,
            "zones": [
                {"id": z.id, "name": z.name, "x": z.x, "y": z.y, "w": z.w, "h": z.h,
                 "color": z.color, "icon": z.icon, "pct": round(z.pct_of_total * 100, 1), "purpose": z.purpose}
                for z in result.zones
            ],
            "equipment": [
                {"id": e.id, "name": e.name, "x": e.x, "y": e.y, "w": e.w, "h": e.h,
                 "icon": e.icon, "quantity": e.quantity, "unit_cost": e.unit_cost,
                 "total_cost": e.total_cost, "priority": e.priority, "notes": e.notes}
                for e in result.equipment
            ],
            "cost_breakdown": result.cost_breakdown,
            "compliance_notes": result.compliance_notes,
            "optimization_tips": result.optimization_tips,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business-types")
async def get_business_types():
    from ai_engine.space.designer import SpaceDesigner, TEMPLATES
    return {
        "types": [
            {"type": k, "display_name": v["display_name"],
             "min_area": v.get("min_area", 100), "ideal_area": v.get("ideal_area", 300),
             "layout_style": v.get("layout_style","standard")}
            for k, v in TEMPLATES.items()
        ]
    }

@router.get("/template/{business_type}")
async def get_template(business_type: str):
    from ai_engine.space.designer import TEMPLATES
    t = TEMPLATES.get(business_type)
    if not t:
        raise HTTPException(status_code=404, detail=f"No template for {business_type}")
    return {
        "business_type": business_type,
        "display_name": t["display_name"],
        "min_area": t.get("min_area",100),
        "ideal_area": t.get("ideal_area",300),
        "layout_style": t.get("layout_style","standard"),
        "customer_flow": t.get("customer_flow","Enter → Browse → Buy → Exit"),
        "zones": t.get("zones",[]),
        "equipment": t.get("equipment",[]),
        "compliance": t.get("compliance",[]),
        "tips": t.get("tips",[]),
    }

@router.get("/sizing-guide/{business_type}")
async def sizing_guide(business_type: str, budget: float = 100000):
    from ai_engine.space.designer import TEMPLATES, SpaceDesigner
    t = TEMPLATES.get(business_type)
    if not t:
        raise HTTPException(status_code=404, detail="Business type not found")
    designer = SpaceDesigner()
    scenarios = []
    for area in [t.get("min_area",100), t.get("ideal_area",300) * 0.6, t.get("ideal_area",300)]:
        try:
            r = designer.design(business_type, area, 0, 0, budget)
            scenarios.append({
                "area_sqft": area,
                "label": "Minimum" if area == t.get("min_area",100) else "Starter" if area < t.get("ideal_area",300) else "Ideal",
                "efficiency_score": r.efficiency_score,
                "setup_cost": r.estimated_setup_cost,
                "monthly_revenue": r.estimated_monthly_revenue,
                "budget_gap": r.cost_breakdown.get("budget_gap", 0),
            })
        except Exception:
            pass
    return {
        "business_type": business_type,
        "display_name": t["display_name"],
        "scenarios": scenarios,
        "recommendation": f"For Rs.{budget:,.0f} budget, a {t.get('min_area',100)}-{t.get('ideal_area',300)} sqft space is optimal.",
    }

@router.post("/cost-estimate")
async def cost_estimate(req: SpaceDesignRequest):
    try:
        from ai_engine.space.designer import SpaceDesigner
        designer = SpaceDesigner()
        result = designer.design(req.business_type, req.area_sqft, req.width_ft or 0, req.depth_ft or 0, req.budget)
        cb = result.cost_breakdown
        essential_eq = [e for e in result.equipment if e.priority == "essential"]
        return {
            "summary": cb,
            "essential_equipment": [{"name": e.name, "quantity": e.quantity, "total": e.total_cost} for e in essential_eq],
            "total_essential_equipment": sum(e.total_cost for e in essential_eq),
            "roi_months": round(cb.get("total_estimated",0) / max(result.estimated_monthly_revenue, 1) * 1.5),
            "payback_period": f"{round(cb.get('total_estimated',0) / max(result.estimated_monthly_revenue, 1) * 1.5)} months",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
