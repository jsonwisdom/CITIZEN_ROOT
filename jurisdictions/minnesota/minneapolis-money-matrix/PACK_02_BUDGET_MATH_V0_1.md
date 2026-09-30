# Pack 02 — Budget Math V0.1

Status: TEACHING_SPEC
Authority: false

Let:

~~~text
B0 = earlier amount
B1 = later amount
T0 = earlier total
T1 = later total
~~~

Absolute change:

~~~text
Delta = B1 - B0
~~~

Percent change, for B0 != 0:

~~~text
PctChange = ((B1 - B0) / B0) * 100
~~~

If B0 = 0:

~~~text
PctChange = UNDEFINED
~~~

Share of total:

~~~text
Share0 = B0 / T0
Share1 = B1 / T1
DeltaShare = Share1 - Share0
~~~

Budget versus actual:

~~~text
Variance = Actual - Budget
VariancePct = (Actual - Budget) / Budget * 100
~~~

Daily expression:

~~~text
DailyEquivalent = AnnualAmount / 365
~~~

Boundary:

~~~text
DAILY_EQUIVALENT != OBSERVED_DAILY_SPENDING
BUDGET != ACTUAL
APPROPRIATION != CASH_PAYMENT
NOMINAL_INCREASE != SHARE_INCREASE
~~~

Always show source, period, units, numerator, denominator, equation, machine value, display value, rounding rule, and limits.
