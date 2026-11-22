"""Facade: kalıpları bir araya getirir ve FR-02'yi (dinamik antrenman motoru) karsilar."""
from __future__ import annotations

from dataclasses import dataclass

from .models import Prescription, UserProfile
from .patterns.decorator import (BasePrescription, DeloadDecorator,
                                 InjuryRestrictionDecorator, PrescriptionComponent)
from .patterns.factory_method import WorkoutPlan, creator_for_level
from .patterns.strategy import WorkoutContext, strategy_for_goal
from .physiology import bmr_mifflin_st_jeor, tdee


@dataclass(frozen=True)
class Program:
    plan: WorkoutPlan
    prescription: Prescription
    bmr: float
    tdee: float


class HyperCoachEngine:
    def generate_program(self, user: UserProfile, deload: bool = False) -> Program:
        plan = creator_for_level(user.level).create_plan()                  # Factory Method
        base = WorkoutContext(strategy_for_goal(user.goal)).execute_plan()  # Strategy
        base = Prescription(base.sets, base.reps, base.intensity, base.rest_sec,
                            exercises=plan.all_exercises())

        component: PrescriptionComponent = BasePrescription(base)           # Decorator
        if user.injuries:
            component = InjuryRestrictionDecorator(component, user.injuries)
        if deload:
            component = DeloadDecorator(component)

        bmr = bmr_mifflin_st_jeor(user.weight_kg, user.height_cm, user.age, user.sex)
        return Program(plan, component.get_prescription(), bmr, tdee(bmr, user.activity_factor))
