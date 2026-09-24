# Proof and claim audit

- Theorem-like statements: **15**
- Statements with a nearby proof or explicit proof pointer: **15**
- Labels: **54**
- Static references: **54**

## Gates

- PASS: `theorem_manifest_nonempty`
- PASS: `no_empty_theorem_statements`
- PASS: `no_duplicate_labels`
- PASS: `no_unknown_static_refs`
- PASS: `no_author_or_text_placeholders`
- PASS: `no_high_risk_overclaims`
- FAIL: `explicit_common_witness_quantifiers`
- FAIL: `exact_upper_lower_evidence_types_distinguished`
- FAIL: `complexity_encoding_checklist_present`
- FAIL: `reviewer_challenge_matrix_present`
- PASS: `ai_assistance_disclosed_in_paper`
- PASS: `model_nonclaims_present`

## Theorem manifest

- `lem:delay` (lemma, paper/main.tex, Bursts, Service Clocks, and Safety): lem:delay Fix an observation t and a release-oblivious service clock. Moving mass that already arrives by t to later times no greater than t cannot decrease occupancy at t .
- `thm:joint` (theorem, paper/main.tex, Bursts, Service Clocks, and Safety): thm:joint For every t 0 and feasible release vector , Q_i(t; ) F_i(t) simultaneously for all tenants. Equality in every coordinate is attained by the common feasible vector equation _j^t= cases (u_j,t),&l_j t, u_j,&l_j>t. cases eq:witness equation
- `cor:capacity` (corollary, paper/main.tex, Bursts, Service Clocks, and Safety): cor:capacity For nonempty traffic, equation (S)= _ t L _iF_i(t), h_i^ (S)= _ t L F_i(t). eq:thresholds equation The service clocks are safe exactly when B (S) and every imposed private cap satisfies h_i h_i^ (S) .
- `lem:cuts` (lemma, paper/main.tex, Reservation Design Under Buffer Caps): lem:cuts For every lower endpoint t and constant reservation r_i , equation F_i(t)= _ s S _i(t) W_i(s,t)-r_i(t-s) . eq:cuts equation
- `thm:private` (theorem, paper/main.tex, Private-Cap Admission): thm:private For private cap h_i , first require W_i(t,t) h_i at every lower endpoint. If any such test fails, no finite rate suffices. Otherwise define equation R_i(h_i)= ! (0, _ t L , s S _i(t), s<t W_i(s,t)-h_i t-s ). eq:inverse equation Reservations satisfying private caps and
- `prop:lp` (proposition, paper/main.tex, Pooled Design as a Linear Epigraph): prop:lp This linear system is feasible exactly when some fixed reservation vector satisfying the floors is robustly safe for pool B .
- `thm:general-opt` (theorem, paper/main.tex, Convex Structure and General Optimum Certificates): thm:general-opt Let R= r: r_i g_i, _i r_i C . A feasible r^* and value B are globally optimal if (i) the exact envelope at r^* is at most B ; (ii) K n+1 genuine lines L_k from~ eq:general-line are active at value B ; and (iii) there are weights _k 0 summing to one, lower-bound mu
- `thm:optimality` (theorem, paper/main.tex, Two-Tenant Optimality Certificates): thm:optimality A feasible (x,B) is globally optimal if a checker verifies the exact envelope upper bound B and one or two genuine cut lines active at (x,B) whose convex-combination slope is zero in the interior, nonnegative at the left boundary, or nonpositive at the right bounda
- `thm:dp` (theorem, paper/main.tex, Candidate Times and Factorization): thm:dp For any supplied elimination order, max-sum elimination computes B_ phase , a maximizing observation, and a maximizing phase assignment exactly in equation O ! (|T| , poly (m+n+g)2^ w( )+1 ) eq:dpcomplexity equation time and analogous polynomial-times-exponential storage. 
- `thm:hard` (theorem, paper/main.tex, Unbounded-Width Hardness): thm:hard OVERLOAD is NP-complete and SAFE is coNP-complete, even with unit bursts, equal fixed reservations, and arrivals restricted to four epochs. The phase-interaction graph of the construction is the input graph.
- `prop:cornergap` (proposition, paper/main.tex, Sharp Negative Controls): prop:cornergap For one unit-rate queue and m unit bursts with windows [j,j+m] , every vector choosing only interval endpoints has peak one, while the exact robust peak is m .
- `prop:corrgap` (proposition, paper/main.tex, Sharp Negative Controls): prop:corrgap There are schedules whose every burst has marginal window [j,j+m-1] and whose exact peak is one, while the independent rectangular relaxation requires m .
- `prop:privategap` (proposition, paper/main.tex, Sharp Negative Controls): prop:privategap For n tenants, two instances can have the same vector of private maxima, all equal to one, while their exact shared pools are one and n .
- `prop:calendargap` (proposition, paper/main.tex, Sharp Negative Controls): prop:calendargap Two periodic calendars can give every tenant the same number of slots per period and nevertheless require different exact buffers for the same fixed arrivals.
- `prop:setmono` (proposition, paper/main.tex, Refinement, Approximation, and Composition): prop:setmono If U_1 U_2 , then B( U_1) B( U_2) . Consequently, safety proved for an outer approximation U_2 is valid for U_1 , whereas an overload witness found in an inner approximation U_1 is valid for U_2 .
