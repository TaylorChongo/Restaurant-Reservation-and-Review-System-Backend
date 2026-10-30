-- Shows the availability query WITHOUT and WITH the time index.
-- Run: psql -U postgres -d reservation_db -f explain_demo.sql
-- The index is only removed inside a transaction, then put back by ROLLBACK.

BEGIN;
DROP INDEX idx_reservations_time;

\echo '========== WITHOUT the index =========='
EXPLAIN ANALYZE
SELECT table_id
FROM reservations
WHERE status = 'confirmed'
  AND start_time < '2026-12-15 21:00'
  AND end_time > '2026-12-15 19:00';

ROLLBACK;

\echo '========== WITH the index =========='
EXPLAIN ANALYZE
SELECT table_id
FROM reservations
WHERE status = 'confirmed'
  AND start_time < '2026-12-15 21:00'
  AND end_time > '2026-12-15 19:00';
