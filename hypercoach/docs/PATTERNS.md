# Tasarım Kalıpları ve Rol Eşlemesi

Tüm arayüzler `abc.ABC` + `@abstractmethod` ile tanımlıdır. Hiçbir kalıp lambda/hazır dil yapısıyla
karşılanmamıştır; çerçeve veya standart kütüphane kalıbı sayılmamıştır.

| Kalıp (Grup) | Rol | Sınıf | Dosya |
|---|---|---|---|
| **Strategy** (Davranışsal) | Strategy | `TrainingStrategy` | patterns/strategy.py |
| | ConcreteStrategy | `HypertrophyStrategy`, `StrengthStrategy`, `EnduranceStrategy` | |
| | Context | `WorkoutContext` | |
| **Factory Method** (Yaratımsal) | Product | `WorkoutPlan` | patterns/factory_method.py |
| | ConcreteProduct | `BeginnerWorkout`, `IntermediateWorkout`, `AdvancedWorkout` | |
| | Creator | `WorkoutPlanCreator` (`create_plan` = factory method) | |
| | ConcreteCreator | `BeginnerPlanCreator`, `IntermediatePlanCreator`, `AdvancedPlanCreator` | |
| **Singleton** (Yaratımsal) | Singleton | `ConfigurationManager` (çift kontrollü kilit) | config.py |
| **Adapter** (Yapısal) | Target | `FitnessDataTarget`, `SupplementCatalogTarget` | patterns/adapter.py |
| | Adaptee | `AppleHealthService`, `StravaService`, `ExternalSupplementAPI` | |
| | Adapter | `AppleHealthAdapter`, `StravaAdapter`, `SupplementAPIAdapter` | |
| | Client | `ActivityAggregator` | |
| **Decorator** (Yapısal) | Component | `PrescriptionComponent` | patterns/decorator.py |
| | ConcreteComponent | `BasePrescription` | |
| | Decorator | `PrescriptionDecorator` | |
| | ConcreteDecorator | `DeloadDecorator`, `InjuryRestrictionDecorator` | |
| **Observer** (Davranışsal) | Subject | `WorkoutSession` | patterns/observer.py |
| | Observer | `SetLoggedObserver` | |
| | ConcreteObserver | `VolumeLoadTracker`, `OneRepMaxTracker`, `OverloadAdvisor` | |

## "Kaldırılırsa tasarım nasıl bozulur?" (gerçek problem gerekçesi)
- **Strategy:** Kaldırılırsa `HyperCoachEngine` içinde hedefe göre if-elif zinciri oluşur; her yeni hedef motoru değiştirir.
- **Factory Method:** Kaldırılırsa motor üç plan sınıfını doğrudan tanır; yeni seviye motoru değiştirir.
- **Singleton:** Kaldırılırsa her modül kendi eşik kopyasını tutar; `deload_volume_factor` gibi bir ayar değişikliği yalnızca bir modüle yansır.
- **Adapter:** Kaldırılırsa `ActivityAggregator` her servisin alan adını/birimini bilmek zorunda kalır.
- **Decorator:** Kaldırılırsa deload × sakatlık × ... kombinasyonları için alt sınıf patlaması olur.
- **Observer:** Kaldırılırsa `WorkoutSession` hacim/1RM/öneri hesaplayıcılarına sıkı bağlanır; yeni grafik eklemek oturumu değiştirir.

## Kalıpların motorda birleşimi (`engine.py`)
`creator_for_level` (Factory Method) → `WorkoutContext` (Strategy) → `BasePrescription` + dekoratörler (Decorator; kalıplar `ConfigurationManager` Singleton'ını okur). Canlı antrenmanda `WorkoutSession` (Observer) ve dış veride `ActivityAggregator` (Adapter) devreye girer.
