"""Calistirilabilir demo: python -m hypercoach.demo"""
from .engine import HyperCoachEngine
from .models import Goal, Level, SetLog, Sex, UserProfile
from .patterns.adapter import (ActivityAggregator, AppleHealthAdapter, AppleHealthService,
                               StravaAdapter, StravaService)
from .patterns.observer import (OneRepMaxTracker, OverloadAdvisor, VolumeLoadTracker,
                                WorkoutSession)
from .supplements import recommend_supplements


def main() -> None:
    user = UserProfile(age=22, weight_kg=80, height_cm=180, sex=Sex.MALE,
                       level=Level.INTERMEDIATE, goal=Goal.HYPERTROPHY, injuries=("knee",))
    program = HyperCoachEngine().generate_program(user)
    print(f"Plan: {program.plan.split_name} ({program.plan.days_per_week()} gun)")
    print(f"Recete: {program.prescription.sets}x{program.prescription.reps} @ {program.prescription.intensity}")
    print(f"Egzersizler: {', '.join(program.prescription.exercises)}")
    print(f"Notlar: {program.prescription.notes}")
    print(f"BMR={program.bmr:.0f} kcal, TDEE={program.tdee:.0f} kcal")

    acts = ActivityAggregator([AppleHealthAdapter(AppleHealthService()),
                               StravaAdapter(StravaService())]).collect()
    for a in acts:
        print(f"Aktivite [{a.source}]: {a.daily_steps} adim, {a.burned_calories} kcal")

    session, vol, orm, adv = WorkoutSession(), VolumeLoadTracker(), OneRepMaxTracker(), OverloadAdvisor()
    for o in (vol, orm, adv):
        session.attach(o)
    session.log_set(SetLog("Bench Press", 80, 8, 6))
    session.log_set(SetLog("Bench Press", 80, 8, 7))
    print(f"Hacim={vol.total:.0f} kg, 1RM~{orm.best['Bench Press']:.1f} kg, "
          f"sonraki yuk carpani={adv.factors['Bench Press']}")

    for r in recommend_supplements(user, dietary_protein_g=110):
        print(f"Takviye: {r.name} - {r.dose} - {r.timing}")


if __name__ == "__main__":
    main()
