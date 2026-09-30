# Pack 01 — Jurisdiction and Source V0.1

Status: TEACHING_SPEC
Authority: false

## First question

~~~text
WHOSE MONEY RECORD IS THIS?
~~~

Allowed jurisdiction labels:

~~~text
MINNEAPOLIS_CITY
HENNEPIN_COUNTY
MINNESOTA_STATE
FEDERAL
OTHER
UNKNOWN
~~~

Never infer one from another.

~~~text
PLACE_NAME != GOVERNMENT_LEVEL
MINNEAPOLIS != MINNESOTA_STATE
METRO != CITY
COUNTY != CITY
STATE != FEDERAL
~~~

## Source card

~~~json
{
  "source_id": "MM_MN_SRC_000001",
  "jurisdiction": "UNKNOWN",
  "agency_or_entity": null,
  "document_type": null,
  "fiscal_period": null,
  "published_at": null,
  "captured_at": null,
  "source_uri": null,
  "source_hash": null,
  "source_bytes_preserved": false,
  "authority": false
}
~~~

## Hold law

~~~text
UNKNOWN_JURISDICTION -> HOLD
UNKNOWN_PERIOD -> HOLD
UNKNOWN_DOCUMENT_TYPE -> HOLD
SCREENSHOT_WITHOUT_SOURCE -> HOLD
~~~
