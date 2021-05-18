# http://users.atw.hu/sqlnut/sqlnut2-chp-4-sect-4.html

ANSI_FUNCTIONS = {
    # ------------------------------ BUILTIN SCALARS
    'CURRENT_DATE',
    'CURRENT_TIME',
    'CURRENT_TIMESTAMP',
    'CURRENT_USER',
    'SESSION_USER',
    'SYSTEM_USER',
    # ------------------------------ OTHER
    'CAST',
    'COALESCE',
    'NVL',
    'DECODE',
    # ------------------------------ NUMERIC SCALAR
    'ABS',
    'MOD',
    'BIT_LENGTH',
    'CEIL',
    'CHAR_LENGTH',
    'EXP',
    'EXTRACT',
    'FLOOR',
    'LN',
    'OCTET_LENGTH',
    'POSITION',
    'POWER',
    'SQRT',
    'ROUND',
    # ------------------------------ AGG
    'SUM',
    'MIN',
    'MAX',
    'AVG',
    'COUNT',
    # ------------------------------ STRING
    'CONVERT',
    'LOWER',
    'OVERLAY',
    'SUBSTRING',
    'TRANSLATE',
    'TRIM',
    'UPPER'
}
