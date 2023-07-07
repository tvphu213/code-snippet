---get meta data in specific table schema
SELECT 
t.table_name as "Table_Name"
, c.column_name as "Column_Name"
, c.data_type "Data_Type"
, CASE WHEN c.is_nullable = 'NO' THEN 'Y' ELSE 'N' END AS "Required"
, CASE WHEN pk.column_name IS NOT NULL THEN 'Y' ELSE 'N' END AS "Primary_Key"
, CASE WHEN fk.foreign_column IS NOT NULL THEN 'Y' ELSE 'N' END AS "Foreign_Key"
, fk.foreign_table AS "Foreign_Table"
FROM information_schema.tables AS t
JOIN information_schema.columns AS c ON t.table_name = c.table_name
LEFT JOIN (
    SELECT conrelid::regclass AS "FK_Table"
      ,CASE WHEN pg_get_constraintdef(c.oid) LIKE 'FOREIGN KEY %' THEN substring(pg_get_constraintdef(c.oid), 14, position(')' in pg_get_constraintdef(c.oid))-14) END AS "FK_Column"
      ,CASE WHEN pg_get_constraintdef(c.oid) LIKE 'FOREIGN KEY %' THEN substring(pg_get_constraintdef(c.oid), position(' REFERENCES ' in pg_get_constraintdef(c.oid))+12, position('(' in substring(pg_get_constraintdef(c.oid), 14))-position(' REFERENCES ' in pg_get_constraintdef(c.oid))+1) END AS "PK_Table"
      ,CASE WHEN pg_get_constraintdef(c.oid) LIKE 'FOREIGN KEY %' THEN substring(pg_get_constraintdef(c.oid), position('(' in substring(pg_get_constraintdef(c.oid), 14))+14, position(')' in substring(pg_get_constraintdef(c.oid), position('(' in substring(pg_get_constraintdef(c.oid), 14))+14))-1) END AS "PK_Column"
FROM   pg_constraint c
JOIN   pg_namespace n ON n.oid = c.connamespace
WHERE  contype IN ('f', 'p ')
AND pg_get_constraintdef(c.oid) LIKE 'FOREIGN KEY %'
ORDER  BY pg_get_constraintdef(c.oid), conrelid::regclass::text, contype DESC;
) AS fk ON t.table_name = split_part(fk.FK_Table,'.', 2)
   AND c.column_name = fk.FK_Column
LEFT JOIN (
    SELECT conname, split_part(conrelid::regclass::text,'.', 2) AS table, a.attname AS column_name
    FROM pg_constraint
    JOIN pg_attribute a ON a.attnum = ANY(conkey) AND a.attrelid = conrelid
    WHERE contype = 'p'
) AS pk ON t.table_name = pk.table
   AND c.column_name = pk.column_name
WHERE t.table_schema in ('op', 'usr', 'li', 'cs', 'im');


