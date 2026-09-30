# Pack 04 — Real / Nominal / Inflation V0.1

Status: ECONOMICS_TEACHING_SPEC
Authority: false

Nominal change:

~~~text
NominalDelta = N1 - N0
~~~

With a receipt-bound price index:

~~~text
RealValue1_in_base_period = N1 * (Index0 / Index1)
RealDelta = RealValue1_in_base_period - N0
~~~

Without a documented index:

~~~text
REAL_CHANGE = HOLD
NOMINAL_CHANGE = MAY_BE_COMPUTED
~~~

Hard separations:

~~~text
NOMINAL != REAL
PRICE_LEVEL != PRICE_OF_EVERY_ITEM
INFLATION != COST_OVERRUN
INFLATION_ADJUSTMENT != CAUSAL_EXPLANATION
~~~

Kid line: Bigger dollars do not always mean more stuff.
