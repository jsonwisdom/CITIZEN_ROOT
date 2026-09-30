# Pack 06 — Per-Capita and Unit-Cost Math V0.1

Status: TEACHING_SPEC
Authority: false

With verified amount A and population P:

~~~text
PerCapita = A / P
~~~

Boundary:

~~~text
PER_CAPITA != INDIVIDUAL_PAYMENT
PER_CAPITA != TAX_BILL
~~~

With verified total cost and unit count:

~~~text
CostPerUnit = TotalCost / VerifiedUnits
~~~

Possible units may include lane-mile, park-acre, housing-unit, service-call, student, employee, ride, or project, but the denominator must be typed.

~~~text
AVERAGE_UNIT_COST != EVERY_UNIT_COST
BLENDED_COST != COMPONENT_COST
PROJECT_BUDGET_PER_UNIT != FINAL_DELIVERED_COST_PER_UNIT
~~~

If denominator identity is unclear:

~~~text
UNIT_COST = HOLD
~~~
