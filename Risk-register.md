# Risks

| ST | № | Risk | Chance | Impact | Response | Owner |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
|  | R1 | Scope grows (menu, fees, waitlist come back) | High | High | Out-of-scope list in the charter, any addition needs sponsor approval  | Illia Nykytiak |
|  | R2 | Default stay duration still undecided, blocking the allocation engine | High | High | Decision closed in week 6 | Zuzana Rubinova |
|  | R3 | Allocation error at boundaries (one booking ends 20:00, the next starts 20:00) | Medium | High | Edge-case test list written in week 6, before the build | Eman Abdai |
|  | R4 | Two guests book the same table at the same moment | Medium | High | Database-level constraint or transaction plus a dedicated test | Dylan Almeida |
|  | R5 | Integration conflicts between the two developers | Medium | Medium  | Clear split of work, pull-request review before merge | Abdourrahmane Makni |
|  | R6 | A team member is unavailable (exams, illness) | Medium | High | Shared repo and docs, a named backup for each role | Illia Nykytiak |
|  | R7 | Receiving team cannot run the system in week 12 | Medium | High | Simple setup, dry run by someone outside the team in week 11 | Illia Nykytiak |
|  | R8 | No real table layout or input from the restaurant | Low | Medium | Team defines a realistic layout and documents it as an assumption | Zuzana Rubinova |
|  | R9 | AI-generated code or text accepted without checking | Medium | Medium | Review before merge, entries in the AI use log | Illia Nykytiak |
