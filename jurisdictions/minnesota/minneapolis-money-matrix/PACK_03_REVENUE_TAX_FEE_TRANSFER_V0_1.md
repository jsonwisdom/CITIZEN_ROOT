# Pack 03 — Revenue / Tax / Fee / Transfer V0.1

Status: TAXONOMY_SPEC
Authority: false

Do not combine unlike money categories.

~~~text
TAX
FEE
FINE
GRANT
INTERGOVERNMENTAL_TRANSFER
SERVICE_CHARGE
BOND_PROCEEDS
ASSET_SALE
OTHER_REVENUE
~~~

Hard separations:

~~~text
TAX != FEE
FEE != FINE
GRANT != TAX_REVENUE
BOND_PROCEEDS != OPERATING_REVENUE
REVENUE != PROFIT
TRANSFER_IN != NEW ECONOMIC OUTPUT
~~~

For category R_i and total R:

~~~text
RevenueShare_i = R_i / R
DeltaShare_i = Share_i,t1 - Share_i,t0
~~~

~~~text
SHARE_CHANGE != POLICY_CAUSE
REVENUE_CHANGE != TAX_RATE_CHANGE
~~~
