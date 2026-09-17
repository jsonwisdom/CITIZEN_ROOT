# Copilot Discover Stories — External Source Intake Receipt — 2026-09-17

**Class:** external-source pointer / append-only intake  
**Authority created:** FALSE  
**Facts promoted:** 0  
**Existing artifacts overwritten:** NONE  
**Content verification:** HOLD

## Source pointers

### SOURCE_1
URL:
https://copilot.microsoft.com/shares/discover-stories/f3XzuP64A6afDcuTdtxpJ

URL_STRING_SHA256:
11a0e0bb026f9f689674a411955bb14a1c3737faaafb20dd25e10b79fe4e4515

### SOURCE_2
URL:
https://copilot.microsoft.com/shares/discover-stories/gvSE6Ce5qeCj5VLmJBpor

URL_STRING_SHA256:
ec559369389f529e11f02fb8cbccbe1c53e0274ea59231bdc232cd336801e02d

## Retrieval state

The current public-web retrieval attempt did not return the story contents for either Microsoft Copilot share URL. Exact-link web search also returned no indexed result.

Therefore:

```text
URL_OBSERVED = TRUE
URL_STRING_PRESERVED = TRUE
SOURCE_CONTENT_FETCHED = FALSE
SOURCE_CONTENT_HASHED = FALSE
SOURCE_CONTENT_VERIFIED = FALSE
SOURCE_AUTHORSHIP_VERIFIED = FALSE
SOURCE_CLAIMS_PROMOTED = 0
EXTERNAL_BINDING_STATUS = UNBOUND
```

The SHA-256 values above identify the URL strings only. They are not hashes of the remote story bytes.

## Replay boundary

```text
POINTER != CONTENT
CONTENT != FACT
SHARED_LINK != AUTHORSHIP
MICROSOFT_HOST != CLAIM_VERIFICATION
URL_HASH != CONTENT_HASH
FAILED_FETCH != SOURCE_NONEXISTENCE
```

## Append-only state

```text
INTAKE_EVENT_1 = SOURCE_POINTER_ADDED
INTAKE_EVENT_2 = SOURCE_POINTER_ADDED
CLAIM_STATE_CHANGE = NONE
FACTS_PROMOTED = 0
AUTHORITY_CREATED = FALSE
REPLAY = HOLD
```

Next valid promotion requires retrievable source contents or a user-supplied export/screenshot/text that can be bound to one of these pointers.
