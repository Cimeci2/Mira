# Skill: takedown_legal_fr — EU/FR legal reporting route

Goal: report non-consensual intimate/deepfake imagery of an ADULT through the official
French / EU legal channels, and — where the content is hosted — send a DSA art. 16
notice to the platform's illegal-content contact.

## Legal basis (do NOT invent, and never state a penalty/fine)
- Code pénal art. 226-8-1 (loi SREN n° 2024-449) — montage à caractère sexuel sans consentement.
- DSA — règlement (UE) 2022/2065, art. 16 — notice-and-action auprès de l'hébergeur.
- LCEN (loi n° 2004-575).

## Channels (in order)
1. PHAROS — https://www.internet-signalement.gouv.fr — official report of illegal content
   to the French authorities.
2. The hosting platform's DSA art. 16 "illegal content" form, on the specific URL.
3. (Optional) CNIL — droit à l'image / données personnelles, if applicable.

## Data to provide (from the case — never the raw image, never more victim PII than mandated)
- Exact URL(s): record.source_url.
- Description: "deepfake sexuel non consenti d'une personne majeure identifiée".
- Evidence block: perceptual hash, discovery timestamp, detector score.
- Notifier identity (the mandataire, DSA art. 16(2)(c)); the victim's identity is NOT disclosed.
- Good-faith declaration (DSA art. 16(2)(d)).

## Steps (Computer Use)
1. Open the channel. Select the category matching "contenu à caractère sexuel / atteinte à la personne".
2. Fill the fields from the data above; paste the prepared notice text verbatim — do NOT
   rewrite the legal citations.
3. Submit; capture the confirmation reference.
4. Report the reference back; the case moves to NOTIFIED.

## Guardrails
- The human confirmation gate passes BEFORE any submission (enforced upstream).
- DEMO mode: target the mock host and the demo inbox ONLY — never submit to the real
  gouv.fr / platform.
- Never invent or state a penalty/fine (G-9) — use only the citations above.
